from dataclasses import dataclass


@dataclass
class ToolResult:
    """Structured result from tool execution."""

    success: bool
    output: str
    error: str | None = None
