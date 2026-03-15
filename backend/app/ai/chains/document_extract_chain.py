import json
from langchain_core.prompts import PromptTemplate

from app.ai.llm_client import get_llm
from app.ai.prompts.document_extract import EXTRACT_DATA_PROMPT


def _parse_json(text: str) -> dict:
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i, c in enumerate(text[start:], start):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break
    return {}


def extract_document_data(conversation_messages: list[dict]) -> dict:
    """Extrae datos estructurados de la conversación para el documento."""
    from datetime import datetime
    conv_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in conversation_messages
    )
    llm = get_llm(temperature=0, max_output_tokens=4096)
    prompt = PromptTemplate.from_template(EXTRACT_DATA_PROMPT)
    chain = prompt | llm
    result = chain.invoke({"conversation": conv_text})
    data = _parse_json(result.content if hasattr(result, "content") else str(result))
    if not data.get("lugar_fecha", {}).get("fecha"):
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        data.setdefault("lugar_fecha", {})
        data["lugar_fecha"]["fecha"] = f"{data['lugar_fecha'].get('lugar') or 'A'}, a {ahora.day} de {meses[ahora.month-1]} de {ahora.year}"
    return data
