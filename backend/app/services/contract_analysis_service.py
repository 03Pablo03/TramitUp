"""
Servicio de análisis de cláusulas contractuales.
Detecta el tipo de contrato (alquiler/laboral/otro) y aplica la normativa española correspondiente.
"""
import json
import re
from typing import Any, Dict

from app.ai.llm_client import get_llm
from app.ai.prompts.contract_analysis import (
    ALQUILER_ANALYSIS_PROMPT,
    DETECT_CONTRACT_TYPE_PROMPT,
    GENERIC_ANALYSIS_PROMPT,
    LABORAL_ANALYSIS_PROMPT,
)
from app.services.document_analysis_service import document_analysis_service


_PROMPT_MAP = {
    "alquiler": ALQUILER_ANALYSIS_PROMPT,
    "laboral": LABORAL_ANALYSIS_PROMPT,
}

# Caracteres máximos del texto del contrato que se envían al LLM
_MAX_CONTRACT_CHARS = 12_000


def _extract_json(text: str) -> Dict[str, Any]:
    """Extrae el primer bloque JSON válido del texto del LLM."""
    # Intentar parsear directo
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Buscar bloque JSON entre ```json ... ``` o ``` ... ```
    match = re.search(r"```(?:json)?\s*(\{[\s\S]+?\})\s*```", text, re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Buscar el primer { ... } que sea JSON válido
    match = re.search(r"\{[\s\S]+\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("No se encontró JSON válido en la respuesta del modelo")


def analyze_contract_from_text(texto: str) -> Dict[str, Any] | None:
    """
    Analiza texto ya extraído de un documento para detectar si es un contrato
    de alquiler o laboral y devuelve cláusulas problemáticas.

    Returns None si no es un contrato alquiler/laboral reconocible.
    Solo para contratos con prompts especializados (no genérico).
    """
    if not texto or len(texto.strip()) < 100:
        return None

    texto_truncado = texto[:_MAX_CONTRACT_CHARS]
    llm = get_llm(temperature=0.1, max_output_tokens=4096)

    # Detectar tipo de contrato
    tipo_prompt = DETECT_CONTRACT_TYPE_PROMPT.format(texto=texto_truncado[:1500])
    tipo_response = llm.invoke(tipo_prompt)
    tipo_raw = (tipo_response.content if hasattr(tipo_response, "content") else str(tipo_response)).strip().lower()

    tipo_contrato = None
    for key in _PROMPT_MAP:
        if key in tipo_raw:
            tipo_contrato = key
            break

    # Solo analizar contratos con prompt especializado (alquiler o laboral)
    if not tipo_contrato:
        return None

    # Analizar con prompt especializado
    full_prompt = _PROMPT_MAP[tipo_contrato].format(texto=texto_truncado)
    analysis_response = llm.invoke(full_prompt)
    analysis_text = (
        analysis_response.content if hasattr(analysis_response, "content") else str(analysis_response)
    )

    try:
        result = _extract_json(analysis_text)
    except ValueError:
        return None

    result.setdefault("tipo_contrato", tipo_contrato)
    result.setdefault("resumen", "")
    result.setdefault("clausulas", [])
    result.setdefault("recomendacion_general", "")
    return result


async def analyze_contract(
    file_content: bytes,
    content_type: str,
    filename: str,
) -> Dict[str, Any]:
    """
    Analiza un contrato y devuelve cláusulas problemáticas categorizadas por riesgo.

    Args:
        file_content: Bytes del archivo (PDF, DOCX, imagen)
        content_type: MIME type del archivo
        filename: Nombre del archivo (para mensajes de error)

    Returns:
        Dict con tipo_contrato, resumen, clausulas[], recomendacion_general
    """
    # 1. Extraer texto del documento
    texto = document_analysis_service._extract_text_from_file(file_content, content_type)

    if not texto or len(texto.strip()) < 50:
        return {
            "tipo_contrato": "desconocido",
            "resumen": "No se pudo extraer texto del documento. Asegúrate de que el archivo contiene texto seleccionable.",
            "clausulas": [],
            "recomendacion_general": "Prueba a subir el documento en formato PDF o DOCX con texto seleccionable.",
        }

    texto_truncado = texto[:_MAX_CONTRACT_CHARS]

    llm = get_llm(temperature=0.1, max_output_tokens=4096)

    # 2. Detectar tipo de contrato
    tipo_prompt = DETECT_CONTRACT_TYPE_PROMPT.format(texto=texto_truncado[:1500])
    tipo_response = llm.invoke(tipo_prompt)
    tipo_raw = (tipo_response.content if hasattr(tipo_response, "content") else str(tipo_response)).strip().lower()

    tipo_contrato = "otro"
    for key in _PROMPT_MAP:
        if key in tipo_raw:
            tipo_contrato = key
            break

    # 3. Analizar con el prompt especializado
    analysis_prompt = _PROMPT_MAP.get(tipo_contrato, GENERIC_ANALYSIS_PROMPT)
    full_prompt = analysis_prompt.format(texto=texto_truncado)

    analysis_response = llm.invoke(full_prompt)
    analysis_text = (
        analysis_response.content if hasattr(analysis_response, "content") else str(analysis_response)
    )

    # 4. Parsear respuesta JSON
    try:
        result = _extract_json(analysis_text)
    except ValueError:
        result = {
            "tipo_contrato": tipo_contrato,
            "resumen": "El análisis se completó pero no se pudo estructurar el resultado. Consulta con un abogado.",
            "clausulas": [],
            "recomendacion_general": "Recomendamos revisar el contrato con un profesional jurídico.",
        }

    # Garantizar campos mínimos
    result.setdefault("tipo_contrato", tipo_contrato)
    result.setdefault("resumen", "")
    result.setdefault("clausulas", [])
    result.setdefault("recomendacion_general", "")

    return result
