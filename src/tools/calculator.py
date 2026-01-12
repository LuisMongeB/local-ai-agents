import math
from typing import Any

from langchain_core.tools import tool

# Safe functions for math evaluation
SAFE_FUNCTIONS: dict[str, Any] = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
}


def safe_eval(expression: str) -> float | int:
    """Safely evaluate a mathematical expression."""
    allowed_names = {**SAFE_FUNCTIONS}
    code = compile(expression, "<string>", "eval")

    for name in code.co_names:
        if name not in allowed_names:
            raise ValueError(f"Use of '{name}' is not allowed")

    return eval(expression, {"__builtins__": {}}, allowed_names)


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.

    Use this tool for any mathematical calculations. Supports basic arithmetic
    (+, -, *, /, //, %, **) and functions like sqrt, sin, cos, tan, log, exp, abs, round.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)", "sin(pi/2)")

    Returns:
        The result of the calculation as a string.
    """
    try:
        result = safe_eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Error: {e}"
    except SyntaxError:
        return "Error: Invalid expression syntax"
    except Exception as e:
        return f"Error: {e}"
