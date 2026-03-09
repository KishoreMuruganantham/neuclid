"""Sandboxed Python REPL tool for deterministic math solving via SymPy."""

import io
import contextlib
import traceback
from crewai.tools import tool


ALLOWED_MODULES = {
    "sympy": __import__("sympy"),
    "math": __import__("math"),
}

_ALLOWED_IMPORT_NAMES = {"sympy", "math", "fractions", "decimal", "itertools", "functools", "collections"}


def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Allow importing only from approved math-related modules."""
    base = name.split(".")[0]
    if base not in _ALLOWED_IMPORT_NAMES:
        raise ImportError(f"Import of '{name}' is not allowed. Only math-related modules: {_ALLOWED_IMPORT_NAMES}")
    return __import__(name, globals, locals, fromlist, level)


def _execute_code(code: str) -> str:
    """Execute Python code in a restricted namespace with sympy and math available."""
    import builtins as _builtins

    safe_builtins = {
        "__import__": _safe_import,
        "print": print,
        "range": range,
        "len": len,
        "int": int,
        "float": float,
        "str": str,
        "list": list,
        "tuple": tuple,
        "dict": dict,
        "set": set,
        "bool": bool,
        "abs": abs,
        "round": round,
        "sum": sum,
        "min": min,
        "max": max,
        "enumerate": enumerate,
        "zip": zip,
        "sorted": sorted,
        "map": map,
        "filter": filter,
        "isinstance": isinstance,
        "type": type,
        "True": True,
        "False": False,
        "None": None,
        "complex": complex,
        "pow": pow,
        "reversed": reversed,
        "repr": repr,
    }

    namespace = {"__builtins__": safe_builtins}
    for name, mod in ALLOWED_MODULES.items():
        namespace[name] = mod

    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(code, namespace)
        output = stdout_capture.getvalue()
        if not output.strip():
            last_line = code.strip().split("\n")[-1]
            try:
                result = eval(last_line, namespace)
                if result is not None:
                    output = str(result)
            except Exception:
                pass
        return output.strip() if output.strip() else "Code executed successfully (no output)."
    except Exception:
        return f"EXECUTION ERROR:\n{traceback.format_exc()}"


@tool("PythonCalculator")
def python_calculator(code: str) -> str:
    """Execute Python/SymPy code for deterministic math computation.
    You MUST use this tool for ALL calculations. Never do mental math.
    Import sympy functions directly: from sympy use symbols, solve, limit, diff, integrate, simplify, etc.
    Always print() your final results.

    Example:
    ```
    from sympy import symbols, solve, sqrt
    x = symbols('x')
    eq = 3*x**2 + 7*x - 5
    solutions = solve(eq, x)
    for s in solutions:
        print(f"x = {s} = {float(s):.6f}")
    ```
    """
    return _execute_code(code)
