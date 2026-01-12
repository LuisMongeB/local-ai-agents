from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
import structlog
from fastapi import FastAPI

from src.config import settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler."""
    logger.info(
        "application_starting",
        ollama_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL,
    )
    yield
    logger.info("application_shutdown")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Local AI Agents",
        description="Local agentic system using LangGraph and Ollama",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health() -> dict:
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.get("/health/ollama")
    async def health_ollama() -> dict:
        """Check Ollama connectivity."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.OLLAMA_BASE_URL}/api/tags",
                    timeout=5.0,
                )
                response.raise_for_status()
                models = response.json().get("models", [])
                return {
                    "status": "healthy",
                    "ollama_url": settings.OLLAMA_BASE_URL,
                    "models_available": len(models),
                }
        except httpx.RequestError as e:
            logger.error("ollama_health_check_failed", error=str(e))
            return {
                "status": "unhealthy",
                "ollama_url": settings.OLLAMA_BASE_URL,
                "error": str(e),
            }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
