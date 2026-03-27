from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.ai.llm_client import get_llm
from app.ai.prompts.system_base import SYSTEM_BASE


def build_chat_prompt(rag_context: str, classification: dict | None) -> str:
    """Build system prompt with RAG context."""
    extra = ""
    if classification:
        # Nota interna para el LLM — NO debe repetirse ni mencionarse en la respuesta al usuario
        extra = f"\n\n[CONTEXTO INTERNO — no mencionar al usuario: categoría={classification.get('category', '')}, subcategoría={classification.get('subcategory', '')}, urgencia={classification.get('urgency', 'media')}]"

    has_documents = "DOCUMENTOS ADJUNTOS POR EL USUARIO" in (rag_context or "")
    doc_instruction = ""
    if has_documents:
        doc_instruction = """

IMPORTANTE — DOCUMENTOS ADJUNTOS:
El usuario ha adjuntado uno o más documentos. Su contenido está incluido en el contexto a continuación.
NUNCA digas que no puedes leer o acceder a archivos adjuntos — ya tienes el contenido extraído.
Responde directamente usando la información del documento."""

    return f"""{SYSTEM_BASE}{doc_instruction}

Contexto normativo relevante y documentos adjuntos (usa esta información para fundamentar tu respuesta):
{rag_context or 'No hay contexto específico. Responde de forma general sobre procedimientos en España.'}
{extra}

Responde en español. Sé conciso pero completo. Si faltan datos del usuario para dar una guía precisa, pregunta de forma clara."""


def get_chat_chain():
    return get_llm(temperature=0.3, max_output_tokens=4096, streaming=True)


def format_messages(history: list[dict], user_message: str, system_prompt: str) -> list:
    """Format LangChain messages from history + new user message."""
    messages = [SystemMessage(content=system_prompt)]
    for m in history:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))
    messages.append(HumanMessage(content=user_message))
    return messages


def stream_chat_response(
    user_message: str,
    rag_context: str,
    classification: dict | None,
    history: list[dict],
):
    """
    Generator that yields chunks of the AI response.
    """
    llm = get_chat_chain()
    prompt = build_chat_prompt(rag_context, classification)
    messages = format_messages(history, user_message, prompt)
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content
