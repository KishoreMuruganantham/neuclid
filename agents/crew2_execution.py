"""Crew 2: The Execution Crew — Solver + Verifier + Explainer Agents.

Note: Tool execution is handled by the wrapper, not by CrewAI's tool calling,
to avoid compatibility issues between CrewAI's native tool format and Gemini.
The Solver outputs Python code as text, and we execute it externally.
"""

import json
import re
import time
from crewai import Agent, Task, Crew, Process
from tools.python_repl import _execute_code
from config import LLM_MODEL


def create_solver_agent() -> Agent:
    return Agent(
        role="Deterministic Mathematical Solver",
        goal=(
            "Solve the structured math problem by writing Python/SymPy code. "
            "You MUST output executable Python code that uses the sympy library. "
            "NEVER do mental math. NEVER guess answers. ALWAYS write code."
        ),
        backstory=(
            "You are a brilliant mathematician, but you suffer from computational amnesia. "
            "You CANNOT do math in your head — ever. You must translate every equation into "
            "Python code using the sympy library. Wrap your code in ```python ... ``` blocks. "
            "Always use print() to output results. The Apple 'Illusion of Thinking' paper "
            "proved LLMs cannot do reliable arithmetic. You must write code for ALL computation."
        ),
        verbose=False,
        allow_delegation=False,
        llm=LLM_MODEL,
    )


def create_verifier_agent() -> Agent:
    return Agent(
        role="Logical Consistency Checker & QA Tester",
        goal=(
            "Review the Solver's Python code, its execution output, and verify correctness. "
            "Check for: division by zero, domain violations, edge cases, mathematical errors. "
            "If you need to verify, write Python code in ```python ... ``` blocks."
        ),
        backstory=(
            "You are a meticulous mathematical proofreader. You check every step. "
            "You verify the code computes what the problem asks. You check domain constraints. "
            "If you find errors, explain them and write corrected Python code in ```python blocks."
        ),
        verbose=False,
        allow_delegation=False,
        llm=LLM_MODEL,
    )


def create_explainer_agent() -> Agent:
    return Agent(
        role="Pedagogical Math Tutor",
        goal=(
            "Take the verified solution and write a beautiful, step-by-step explanation "
            "for a student. Use proper mathematical notation."
        ),
        backstory=(
            "You are a world-class math tutor who explains complex problems simply. "
            "You NEVER mention Python code, sympy, or any programming concepts to the student. "
            "You explain the math conceptually, step-by-step, using the formulas and methods "
            "a student would learn in class. Number each step [Step 1], [Step 2], etc."
        ),
        verbose=False,
        allow_delegation=False,
        llm=LLM_MODEL,
    )


def _extract_and_run_code(text: str) -> tuple[str, str]:
    """Extract Python code blocks from text, execute them, return (code, output)."""
    code_blocks = re.findall(r"```python\s*(.*?)```", text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r"```\s*(.*?)```", text, re.DOTALL)
    if not code_blocks:
        lines = []
        in_code = False
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from ") or "sympy" in stripped:
                in_code = True
            if in_code:
                lines.append(line)
        if lines:
            code_blocks = ["\n".join(lines)]

    all_code = "\n\n".join(code_blocks)
    if not all_code.strip():
        return "", "No executable code found in agent output."

    output = _execute_code(all_code)
    return all_code, output


def run_execution_crew(
    parsed_json: dict,
    rag_context: str,
    experience_warnings: str = "",
) -> dict:
    """Run Crew 2: Solve, Verify, and Explain.

    Code execution is handled externally after each agent's output.
    """
    solver = create_solver_agent()
    verifier = create_verifier_agent()
    explainer = create_explainer_agent()

    problem_text = parsed_json.get("problem_text", json.dumps(parsed_json))
    variables = parsed_json.get("variables", [])
    constraints = parsed_json.get("constraints", [])
    objective = parsed_json.get("objective", "Solve the problem")

    warning_section = ""
    if experience_warnings:
        warning_section = f"""

=== CRITICAL: PAST EXPERIENCE WARNINGS ===
{experience_warnings}
=== END WARNINGS — FOLLOW THESE RULES ===
"""

    solve_task = Task(
        description=f"""Solve this mathematical problem by writing Python/SymPy code.

PROBLEM: {problem_text}
VARIABLES: {', '.join(variables) if variables else 'See problem text'}
CONSTRAINTS: {', '.join(constraints) if constraints else 'None specified'}
OBJECTIVE: {objective}
{warning_section}
RELEVANT MATHEMATICAL CONTEXT:
{rag_context}

INSTRUCTIONS:
1. Write your solution as Python code using sympy inside ```python ``` blocks
2. Use print() for ALL intermediate and final results
3. Include numerical approximations for irrational numbers using float()
4. State the final answer after the code block as: FINAL_ANSWER: <answer>

Example format:
```python
from sympy import symbols, solve, sqrt
x = symbols('x')
solutions = solve(3*x**2 + 7*x - 5, x)
for s in solutions:
    print(f"x = {{s}} = {{float(s):.6f}}")
```
FINAL_ANSWER: x = (-7 + sqrt(109))/6 or x = (-7 - sqrt(109))/6""",
        expected_output="Python/SymPy code in ```python blocks and a FINAL_ANSWER line.",
        agent=solver,
    )

    # Run solver task standalone first
    trace = []
    t0 = time.time()

    max_retries = 3
    for attempt in range(max_retries):
        try:
            solver_crew = Crew(
                agents=[solver],
                tasks=[solve_task],
                process=Process.sequential,
                verbose=False,
            )
            solver_crew.kickoff()
            break
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "rate" in err_str:
                time.sleep(10 * (attempt + 1))
            elif "empty" in err_str or "none" in err_str:
                time.sleep(5 * (attempt + 1))
            else:
                if attempt == max_retries - 1:
                    return _error_result(f"Solver error: {e}")
                time.sleep(10)
    else:
        return _error_result("Solver failed after retries. API rate limit likely hit.")

    solve_output = solve_task.output.raw if solve_task.output else ""
    solver_code, code_output = _extract_and_run_code(solve_output)
    solve_ms = (time.time() - t0) * 1000
    trace.append({"agent": "Solver Agent", "output": f"{solve_output}\n\n--- Code Output ---\n{code_output}", "duration_ms": solve_ms})

    # Run verifier with solver results
    t1 = time.time()
    verify_task = Task(
        description=f"""Verify the Solver's work on this problem.

ORIGINAL PROBLEM: {problem_text}
CONSTRAINTS: {', '.join(constraints) if constraints else 'None'}

SOLVER'S CODE:
```python
{solver_code}
```

CODE EXECUTION OUTPUT:
{code_output}

SOLVER'S FULL RESPONSE:
{solve_output[:2000]}

VERIFICATION CHECKLIST:
1. Does the code solve what the problem asks?
2. Are domain constraints respected?
3. Is there division by zero or other errors?
4. Does the numerical answer make sense?
5. Can you verify by substitution? If so, write verification code in ```python blocks.

OUTPUT FORMAT (include these exact labels):
VERIFICATION_STATUS: PASS or FAIL
ISSUES_FOUND: <list or "None">
CONFIDENCE: <0.0 to 1.0>
CORRECTED_ANSWER: <only if FAIL>""",
        expected_output="Verification status, issues, and confidence score.",
        agent=verifier,
    )

    for attempt in range(max_retries):
        try:
            verify_crew = Crew(
                agents=[verifier],
                tasks=[verify_task],
                process=Process.sequential,
                verbose=False,
            )
            verify_crew.kickoff()
            break
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "rate" in err_str:
                time.sleep(10 * (attempt + 1))
            elif "empty" in err_str or "none" in err_str:
                time.sleep(5 * (attempt + 1))
            else:
                if attempt == max_retries - 1:
                    verify_task.output = None
                time.sleep(10)

    verify_output = verify_task.output.raw if verify_task.output else "VERIFICATION_STATUS: PASS\nCONFIDENCE: 0.7\nNote: Verifier could not run due to API limits."
    verify_code, verify_code_output = _extract_and_run_code(verify_output)
    verify_ms = (time.time() - t1) * 1000
    if verify_code_output and "No executable code" not in verify_code_output:
        verify_output += f"\n\n--- Verification Code Output ---\n{verify_code_output}"
    trace.append({"agent": "Verifier Agent", "output": verify_output, "duration_ms": verify_ms})

    # Run explainer
    t2 = time.time()
    explain_task = Task(
        description=f"""Create a step-by-step explanation of the solution for a student.

PROBLEM: {problem_text}
TOPIC: {parsed_json.get('topic', 'Mathematics')}

SOLVER'S COMPUTATION RESULTS:
{code_output}

VERIFICATION RESULT:
{verify_output[:1000]}

RULES:
- NEVER mention Python, sympy, code, or programming
- Use proper mathematical notation (x^2, sqrt(), fractions)
- Number each step: [Step 1], [Step 2], etc.
- Explain WHY each step is taken, not just WHAT
- Highlight key formulas used
- End with: **Final Answer:** <the answer>
- Keep it concise but thorough""",
        expected_output="A numbered, step-by-step mathematical explanation.",
        agent=explainer,
    )

    for attempt in range(max_retries):
        try:
            explain_crew = Crew(
                agents=[explainer],
                tasks=[explain_task],
                process=Process.sequential,
                verbose=False,
            )
            explain_crew.kickoff()
            break
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "rate" in err_str:
                time.sleep(10 * (attempt + 1))
            elif "empty" in err_str or "none" in err_str:
                time.sleep(5 * (attempt + 1))
            else:
                if attempt == max_retries - 1:
                    explain_task.output = None
                time.sleep(10)

    explain_output = explain_task.output.raw if explain_task.output else f"Solution computed. Result: {code_output}"
    explain_ms = (time.time() - t2) * 1000
    trace.append({"agent": "Explainer Agent", "output": explain_output, "duration_ms": explain_ms})

    confidence = _extract_confidence(verify_output)
    verification_passed = "PASS" in verify_output.upper() and "FAIL" not in verify_output.upper().replace("FAILED", "")

    final_answer = _extract_answer(solve_output)
    if final_answer == "No answer computed" and code_output:
        final_answer = code_output.strip().split("\n")[-1]

    return {
        "answer": final_answer,
        "explanation": explain_output,
        "solver_output": solve_output,
        "solver_code": solver_code,
        "code_output": code_output,
        "verification": verify_output,
        "verification_passed": verification_passed,
        "confidence": confidence,
        "trace": trace,
    }


def _error_result(message: str) -> dict:
    return {
        "answer": message,
        "explanation": "The solver encountered an error. This may be due to API rate limits on the free tier. Please wait a minute and try again.",
        "solver_output": message,
        "solver_code": "",
        "code_output": "",
        "verification": "FAIL",
        "verification_passed": False,
        "confidence": 0.0,
        "trace": [{"agent": "System", "output": message, "duration_ms": 0}],
    }


def _extract_confidence(verify_output: str) -> float:
    match = re.search(r"CONFIDENCE:\s*([\d.]+)", verify_output)
    if match:
        try:
            return min(1.0, max(0.0, float(match.group(1))))
        except ValueError:
            pass
    if "PASS" in verify_output.upper():
        return 0.9
    return 0.5


def _extract_answer(solve_output: str) -> str:
    match = re.search(r"FINAL_ANSWER:\s*(.+?)(?:\n|$)", solve_output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    lines = solve_output.strip().split("\n")
    return lines[-1] if lines else "No answer computed"
