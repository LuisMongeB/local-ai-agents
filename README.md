# Local AI Agents

A local-first agentic system that runs entirely on your machine using Ollama for LLM inference. The system features an intelligent agent capable of reasoning, planning, and executing tasks using tools like web search, calculations, and code execution. Built with a focus on privacy and independence from cloud APIs, while maintaining the option to integrate with external providers when needed.

The tech stack combines **FastAPI** for the backend API, **LangGraph** for agent orchestration and state management, **Ollama** for local LLM inference, and **Gradio** for the chat interface. Additional tooling includes **pydantic-settings** for configuration management, **structlog** for structured logging, and **httpx** for async HTTP operations. The project uses **uv** for fast, modern Python package management and **Docker Compose** for container orchestration.
