"""
Extrae plazos legales mencionados en la respuesta del asistente.
"""
import json
import logging
from langchain_core.prompts import PromptTemplate

from app.ai.llm_client import get_llm

logger = logging.getLogger(__name__)

PROMPT = """
Analiza el siguiente texto de una respuesta del asistente Tramitup.
Extrae TODOS los plazos legales mencionados (ej: "20 días hábiles para recurrir", "1 año desde el hecho", etc).

Devuelve ÚNICAMENTE un JSON válido con esta estructura (sin markdown, sin texto adicional):
{{
  "detected_deadlines": [
    {{
      "description": "descripción breve del plazo",
      "days": número_entero,
      "reference_date": "YYYY-MM-DD" si el usuario mencionó una fecha concreta de inicio, o null,
      "law_reference": "Art. X Ley Y" o referencia normativa
    }}
  ]
}}

Si NO hay plazos legales relevantes, devuelve: {{"detected_deadlines": []}}

Texto a analizar:
{text}
"""


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
    return {"detected_deadlines": []}


def extract_deadlines_from_response(response_text: str) -> list[dict]:
    """Extrae plazos detectados del texto de la respuesta."""
    if not response_text or len(response_text.strip()) < 50:
        return []
    from app.core.config import get_settings
    if not get_settings().google_api_key:
        return []
    llm = get_llm(temperature=0, max_output_tokens=1024)
    prompt = PromptTemplate.from_template(PROMPT)
    chain = prompt | llm
    # Truncate from the END: deadlines/plazos are typically mentioned at the end of responses
    result = chain.invoke({"text": response_text[-4000:]})
    content = result.content if hasattr(result, "content") else str(result)
    data = _parse_json(content)
    deadlines = data.get("detected_deadlines", [])
    if not isinstance(deadlines, list):
        return []
    
    # Log urgency internally (internal metric, not sent to user)
    for deadline in deadlines:
        days = deadline.get("days", 0)
        urgency = "high" if days < 10 else "medium" if days <= 30 else "low"
        logger.debug(
            "Deadline extracted: description=%s days=%d urgency=%s law=%s",
            deadline.get("description", "")[:50],
            days,
            urgency,
            deadline.get("law_reference", "")[:30]
        )
    
    return deadlines
