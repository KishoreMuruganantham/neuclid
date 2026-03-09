"""Crew 1: The Sanitization Crew — Parser Agent + Intent Router Agent."""

import json
import time
from crewai import Agent, Task, Crew, Process
from config import LLM_MODEL


def create_parser_agent() -> Agent:
    return Agent(
        role="Mathematical Semantic Extractor",
        goal=(
            "Read the raw input text (from OCR, ASR, or direct typing), strip away ALL "
            "narrative fluff, irrelevant context, and noise. Extract pure mathematical "
            "symbols, variables, constraints, and the core question. If the problem is "
            "missing crucial variables or is ambiguous, flag it."
        ),
        backstory=(
            "You are a ruthless mathematical filter. The Apple 'Illusion of Thinking' paper "
            "proved that irrelevant information destroys LLM math accuracy (GSM-NoOp effect). "
            "Your ONLY job is to sanitize input into pure mathematical structure. You never "
            "solve problems — you only extract and structure them. You are paranoid about "
            "ambiguity and would rather flag something as unclear than let a bad interpretation "
            "through."
        ),
        verbose=False,
        allow_delegation=False,
        llm=LLM_MODEL,
    )


def create_router_agent() -> Agent:
    return Agent(
        role="Mathematical Classifier & Router",
        goal=(
            "Read the structured JSON from the Parser. Classify the exact mathematical "
            "sub-domain (e.g., 'Algebra', 'Calculus - Limits', 'Probability'). Determine "
            "which mathematical tools and knowledge areas will be needed."
        ),
        backstory=(
            "You are a mathematical librarian with encyclopedic knowledge of math taxonomy. "
            "You can instantly classify any math problem into its domain and sub-domain. "
            "Your classification drives which knowledge base collections are queried and "
            "which solution strategies are selected."
        ),
        verbose=False,
        allow_delegation=False,
        llm=LLM_MODEL,
    )


def run_sanitization_crew(raw_input: str) -> dict:
    """Run Crew 1: Parse and classify the math problem.

    Returns dict with:
        - parsed_json: structured problem data
        - domain: mathematical classification
        - needs_clarification: bool
        - trace: list of agent execution records
    """
    parser = create_parser_agent()
    router = create_router_agent()

    parse_task = Task(
        description=f"""Analyze this raw math input and extract its mathematical structure.

RAW INPUT:
{raw_input}

You MUST output ONLY a valid JSON object (no markdown, no explanation) with this exact schema:
{{
    "problem_text": "<clean mathematical statement>",
    "topic": "<primary topic>",
    "subtopic": "<specific subtopic>",
    "variables": ["<list of variables>"],
    "constraints": ["<list of constraints like x > 0>"],
    "objective": "<what needs to be found/proved/computed>",
    "needs_clarification": false,
    "clarification_reason": null,
    "ambiguities": []
}}

Rules:
- Strip ALL narrative context that doesn't affect the math
- If a variable is undefined or ambiguous, set needs_clarification to true
- List every mathematical constraint explicitly
- The problem_text should be a clean, unambiguous math statement""",
        expected_output="A valid JSON object with the parsed mathematical structure.",
        agent=parser,
    )

    route_task = Task(
        description="""Read the parsed JSON from the previous task and classify it.

Output ONLY a valid JSON object with this schema:
{
    "domain": "<one of: Algebra, Probability, Calculus - Limits, Calculus - Derivatives, Calculus - Optimization, Linear Algebra, Trigonometry>",
    "difficulty": "<Easy/Medium/Hard>",
    "recommended_approach": "<brief strategy>",
    "tools_needed": ["sympy", "<any other>"],
    "rag_queries": ["<search query 1>", "<search query 2>"]
}""",
        expected_output="A valid JSON object with the mathematical classification and routing.",
        agent=router,
        context=[parse_task],
    )

    crew = Crew(
        agents=[parser, router],
        tasks=[parse_task, route_task],
        process=Process.sequential,
        verbose=False,
    )

    trace = []
    t0 = time.time()

    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = crew.kickoff()
            break
        except Exception as e:
            err_str = str(e).lower()
            if ("429" in err_str or "quota" in err_str or "rate" in err_str or
                    "empty" in err_str or "none" in err_str):
                time.sleep(10 * (attempt + 1))
            else:
                raise
    else:
        return {
            "parsed_json": {"needs_clarification": True, "clarification_reason": "API rate limit reached. Please wait and retry."},
            "route_json": {},
            "domain": "Unknown",
            "needs_clarification": True,
            "trace": [{"agent": "System", "output": "Rate limit error", "duration_ms": 0}],
            "raw_parse": "",
            "raw_route": "",
        }

    total_ms = (time.time() - t0) * 1000

    parse_output = parse_task.output.raw if parse_task.output else ""
    route_output = route_task.output.raw if route_task.output else ""

    trace.append({"agent": "Parser Agent", "output": parse_output, "duration_ms": total_ms * 0.6})
    trace.append({"agent": "Intent Router", "output": route_output, "duration_ms": total_ms * 0.4})

    parsed_json = _safe_parse_json(parse_output)
    route_json = _safe_parse_json(route_output)

    needs_clarification = parsed_json.get("needs_clarification", False)
    domain = route_json.get("domain", "Algebra")

    return {
        "parsed_json": parsed_json,
        "route_json": route_json,
        "domain": domain,
        "needs_clarification": needs_clarification,
        "trace": trace,
        "raw_parse": parse_output,
        "raw_route": route_output,
    }


def _safe_parse_json(text: str) -> dict:
    """Attempt to parse JSON from potentially messy LLM output."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    return {"raw_text": text, "needs_clarification": True, "clarification_reason": "Failed to parse structured output"}
