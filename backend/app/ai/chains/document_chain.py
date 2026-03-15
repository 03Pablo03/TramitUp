from langchain_core.prompts import PromptTemplate

from app.ai.llm_client import get_llm
from app.ai.prompts.document import DOCUMENT_PROMPT
from app.ai.prompts.system_base import AVISO_LEGAL_UI


def get_document_chain():
    llm = get_llm(temperature=0.3, max_output_tokens=4096)
    prompt = PromptTemplate.from_template(DOCUMENT_PROMPT)
    return prompt | llm


def generate_document(
    context: str,
    case_info: str,
    doc_type: str = "modelo de reclamación",
) -> str:
    """Generate document text from RAG context and case info."""
    chain = get_document_chain()
    result = chain.invoke({
        "context": context,
        "case_info": case_info,
        "doc_type": doc_type,
    })
    content = result.content if hasattr(result, "content") else str(result)
    return content + f"\n\n---\n\n{AVISO_LEGAL_UI}"
