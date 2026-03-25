"""
TramitUp Marketing — Claude API helper.
Centraliza las llamadas a la API de Anthropic para todos los bots.
"""

import os
import anthropic

MODEL = "claude-sonnet-4-20250514"
_client = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY no configurada. "
                "Exporta la variable de entorno antes de ejecutar."
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def ask(prompt: str, system: str = "", max_tokens: int = 2048) -> str:
    """Envía un prompt a Claude y devuelve el texto de respuesta."""
    client = get_client()
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": MODEL, "max_tokens": max_tokens, "messages": messages}
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text
