import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.ai.llm_client import get_llm
from app.ai.prompts.classification import CLASSIFICATION_PROMPT


def _parse_classification(text: str) -> dict:
    """Extract JSON from LLM response."""
    # Find outermost {...} block
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
    # Fallback
    return {
        "category": "otro",
        "subcategory": "general",
        "urgency": "media",
        "keywords": [],
        "needs_more_info": False,
        "titulo_resumen": "Consulta general",
    }


def _normalize_classification(data: dict) -> dict:
    """Normalize keys (categoria→category, etc) for backwards compat."""
    return {
        "category": data.get("category", data.get("categoria", "otro")),
        "subcategory": data.get("subcategory", data.get("subcategoria", "general")),
        "urgency": data.get("urgency", data.get("urgencia", "media")),
        "keywords": data.get("keywords", data.get("datos_clave", [])),
        "needs_more_info": data.get("needs_more_info", False),
        "titulo_resumen": data.get("titulo_resumen", "Consulta general"),
    }


def get_classify_chain():
    llm = get_llm(temperature=0, max_output_tokens=1024)
    prompt = PromptTemplate.from_template(CLASSIFICATION_PROMPT)
    chain = prompt | llm | StrOutputParser()
    return chain


def classify_tramite(text: str) -> dict:
    """Classify user message into category, subcategory, urgency, keywords, needs_more_info."""
    chain = get_classify_chain()
    result = chain.invoke({"text": text})
    parsed = _parse_classification(result)
    return _normalize_classification(parsed)
