import sys
from io import StringIO

import structlog
from langchain_core.tools import tool

logger = structlog.get_logger(__name__)

# Restricted builtins for sandboxed execution
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "print": print,
    "range": range,
    "reversed": reversed,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "type": type,
    "zip": zip,
}

# Blocked patterns that could be dangerous
BLOCKED_PATTERNS = [
    "import ",
    "__import__",
    "exec(",
    "eval(",
    "open(",
    "file(",
    "os.",
    "sys.",
    "subprocess",
    "__builtins__",
    "__class__",
    "__bases__",
    "__subclasses__",
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "vars",
    "compile",
]


def is_safe_code(code: str) -> tuple[bool, str | None]:
    """Check if code contains any dangerous patterns."""
    code_lower = code.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in code_lower:
            return False, f"Blocked pattern detected: {pattern}"
    return True, None


@tool
def python_repl(code: str) -> str:
    """Execute Python code and return the output.

    Use this tool to run Python code for data manipulation, calculations,
    string processing, or any computation that benefits from Python.

    The execution is sandboxed with limited builtins. You cannot:
    - Import modules
    - Access the file system
    - Execute system commands
    - Access dangerous attributes

    Args:
        code: Python code to execute.

    Returns:
        The printed output from the code, or the result of the last expression.
    """
    is_safe, error = is_safe_code(code)
    if not is_safe:
        return f"Error: {error}"

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        restricted_globals = {"__builtins__": SAFE_BUILTINS}
        exec(code, restricted_globals)
        output = sys.stdout.getvalue()
        return output if output else "Code executed successfully (no output)"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
    finally:
        sys.stdout = old_stdout
