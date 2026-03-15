import json
from langchain_core.prompts import PromptTemplate

from app.ai.llm_client import get_llm
from app.ai.prompts.document_generate import GENERATE_DOCUMENT_PROMPT
from app.ai.prompts.document_templates import DOCUMENT_TEMPLATES


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


def generate_document_content(extracted_data: dict) -> dict:
    """Genera el contenido del documento a partir de datos extraídos."""
    doc_type = extracted_data.get("document_type", "solicitud_informacion_administrativa")
    template = DOCUMENT_TEMPLATES.get(doc_type, {})
    normativa = template.get("normativa", "legislación aplicable")
    normativas = extracted_data.get("normativa_aplicable") or [normativa]
    normativa_str = "; ".join(normativas)

    llm = get_llm(temperature=0.3, max_output_tokens=4096)
    prompt = PromptTemplate.from_template(GENERATE_DOCUMENT_PROMPT)
    chain = prompt | llm
    result = chain.invoke({
        "extracted_data": json.dumps(extracted_data, ensure_ascii=False, indent=2),
        "normativa_sugerida": normativa_str,
    })
    return _parse_json(result.content if hasattr(result, "content") else str(result))
