"""
Cliente LLM centralizado. Usa Google AI (Gemini) para abaratar costes.
"""
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings

# gemini-2.0-flash: sustituto actual de 1.5-flash (rápido, gratuito, v1beta)
DEFAULT_MODEL = "gemini-2.0-flash"


def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = 0.3,
    max_output_tokens: int = 4096,
    streaming: bool = False,
) -> ChatGoogleGenerativeAI:
    """Devuelve el LLM configurado con Google AI (Gemini)."""
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=settings.google_api_key,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        streaming=streaming,
    )
