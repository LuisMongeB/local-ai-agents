import structlog
from ddgs import DDGS
from langchain_core.tools import tool

logger = structlog.get_logger(__name__)


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for current information.

    Use this tool when you need to find up-to-date information, facts, news,
    or anything that might have changed after your training data.

    Args:
        query: The search query to look up.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        Search results as formatted text with titles, URLs, and snippets.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r['title']}\n   URL: {r['href']}\n   {r['body']}")

        return "\n\n".join(formatted)

    except Exception as e:
        logger.error("web_search_failed", query=query, error=str(e))
        return f"Error performing search: {e}"
