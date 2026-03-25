"""
Claude API helper centralizado.
"""

import json
import time
import anthropic
from marketing.core.config_loader import get_api_key, get
from marketing.core.logger import get_logger
from marketing.core.database import log_operation

log = get_logger("llm")


def get_client() -> anthropic.Anthropic:
    api_key = get_api_key("anthropic")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no configurada.")
    return anthropic.Anthropic(api_key=api_key)


def ask(prompt: str, system: str = "", max_tokens: int = 4096,
        temperature: float = 0.7) -> str:
    """Envía prompt a Claude y devuelve texto."""
    client = get_client()
    model = get("apis.anthropic.model", "claude-sonnet-4-20250514")

    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if system:
        kwargs["system"] = system

    start = time.time()
    try:
        response = client.messages.create(**kwargs)
        text = response.content[0].text
        duration = int((time.time() - start) * 1000)
        log.info(f"LLM call: {len(prompt)} chars → {len(text)} chars ({duration}ms)")
        log_operation("llm_call", "core.llm", "success",
                      f"model={model} tokens_out={response.usage.output_tokens}", duration)
        return text
    except Exception as e:
        duration = int((time.time() - start) * 1000)
        log.error(f"LLM error: {e}")
        log_operation("llm_call", "core.llm", "error", str(e), duration)
        raise


def ask_json(prompt: str, system: str = "", max_tokens: int = 4096) -> dict:
    """Envía prompt y parsea JSON de la respuesta."""
    raw = ask(prompt, system, max_tokens)
    # Strip markdown code blocks if present
    if "```" in raw:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            raw = raw[start:end]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        log.warning(f"JSON parse failed, raw: {raw[:200]}...")
        return {"error": "json_parse_failed", "raw": raw[:1000]}
