from app.ai.chains.classify_chain import classify_tramite
from app.ai.chains.chat_chain import stream_chat_response, build_chat_prompt
from app.ai.rag.retriever import retrieve_context
from app.core.supabase_client import get_supabase_client
from app.services.personalization_service import personalization_service
from app.services.document_analysis_service import document_analysis_service
from app.ai.llm_client import get_llm


def create_conversation(
    user_id: str,
    title: str = "Nueva conversación",
    category: str | None = None,
    subcategory: str | None = None,
) -> str:
    """Create conversation and return id."""
    supabase = get_supabase_client()
    data = {"user_id": user_id, "title": title}
    if category:
        data["category"] = category
    if subcategory:
        data["subcategory"] = subcategory
    result = supabase.table("conversations").insert(data).execute()
    return result.data[0]["id"]


def get_conversation_messages(conversation_id: str, limit: int = 20) -> list[dict]:
    """Get recent messages for a conversation."""
    supabase = get_supabase_client()
    result = supabase.table("messages").select("role, content").eq(
        "conversation_id", conversation_id
    ).order("created_at", desc=False).limit(limit).execute()
    return [{"role": r["role"], "content": r["content"]} for r in (result.data or [])]


def save_message(conversation_id: str, role: str, content: str) -> None:
    """Save a message to the conversation."""
    supabase = get_supabase_client()
    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
    }).execute()


def update_conversation_title(conversation_id: str, title: str) -> None:
    supabase = get_supabase_client()
    supabase.table("conversations").update({"title": title}).eq(
        "id", conversation_id
    ).execute()


def get_or_create_conversation(
    user_id: str,
    conversation_id: str | None,
    first_message: str,
    classification: dict | None,
) -> str:
    """Get existing conversation or create new one. Update title, category, subcategory if new."""
    if conversation_id:
        return conversation_id
    c = classification or {}
    title = c.get("titulo_resumen", first_message[:60] or "Nueva conversación")[:80]
    return create_conversation(
        user_id,
        title,
        category=c.get("category"),
        subcategory=c.get("subcategory"),
    )


def run_chat(user_id: str, message: str, conversation_id: str | None = None, attachment_ids: list[str] | None = None) -> tuple[str, dict, object]:
    """
    Run chat pipeline: classify, RAG, stream with personalization.
    Returns (conversation_id, classification, stream_generator).
    The caller must consume the stream and call save_message(conv_id, "assistant", full_content) when done.
    """
    # Obtener contexto de personalización del usuario
    user_context = personalization_service.get_user_context(user_id)
    
    # Obtener contexto enriquecido de archivos adjuntos con entidades legales
    attachment_context = ""
    if attachment_ids:
        attachment_context = document_analysis_service.get_enhanced_document_context(attachment_ids, user_id)
    
    # Combinar mensaje con contexto de documentos para clasificación
    full_message = message
    if attachment_context:
        full_message = f"{message}\n\n{attachment_context}"
    
    try:
        classification = classify_tramite(full_message)
    except Exception:
        classification = {
            "category": "otro", "subcategory": "general",
            "urgency": "media", "keywords": [],
            "needs_more_info": False, "titulo_resumen": message[:60],
        }
    
    # RAG contextual basado en intereses del usuario (incluye contexto de documentos)
    rag_context_chunks = retrieve_context_personalized(full_message, user_context)
    rag_context = "\n\n---\n\n".join(c["content"] for c in rag_context_chunks)
    
    # Añadir contexto de documentos adjuntos al RAG
    if attachment_context:
        rag_context = f"{rag_context}\n\n{attachment_context}"
    
    conv_id = get_or_create_conversation(user_id, conversation_id, message, classification)
    history = get_conversation_messages(conv_id) if conv_id else []
    save_message(conv_id, "user", message)
    
    # Stream con personalización (usar mensaje original, no el full_message)
    stream = stream_chat_response_personalized(message, rag_context, classification, history, user_context)
    return conv_id, classification, stream


def retrieve_context_personalized(message: str, user_context: dict) -> list[dict]:
    """
    Recupera contexto RAG personalizado basado en el perfil del usuario.
    """
    # Obtener contexto base
    base_chunks = retrieve_context(message)
    
    # Priorizar contenido basado en intereses del usuario
    interest_categories = user_context.get("interest_categories", [])
    primary_category = user_context.get("conversation_history", {}).get("primary_category")
    
    # Si el usuario tiene categorías de interés, priorizar ese contenido
    if interest_categories or primary_category:
        prioritized_chunks = []
        other_chunks = []
        
        for chunk in base_chunks:
            chunk_category = chunk.get("metadata", {}).get("category", "")
            
            # Priorizar si coincide con intereses o categoría principal
            if (chunk_category in interest_categories or 
                chunk_category == primary_category):
                prioritized_chunks.append(chunk)
            else:
                other_chunks.append(chunk)
        
        # Combinar: primero los priorizados, luego los otros
        return prioritized_chunks + other_chunks[:max(0, 5 - len(prioritized_chunks))]
    
    return base_chunks


def stream_chat_response_personalized(message: str, rag_context: str, classification: dict, 
                                    history: list[dict], user_context: dict):
    """
    Genera respuesta de chat con personalización basada en el contexto del usuario.
    """
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    
    # Construir prompt personalizado
    personalized_additions = personalization_service.get_contextual_prompt_additions(user_context)
    base_prompt = build_chat_prompt(rag_context, classification)
    personalized_prompt = base_prompt + personalized_additions
    
    # Preparar mensajes con contexto personalizado
    messages = [SystemMessage(content=personalized_prompt)]
    
    # Añadir historial (limitado según experiencia del usuario)
    is_experienced = user_context.get("profile", {}).get("is_experienced_user", False)
    history_limit = 10 if is_experienced else 5  # Usuarios experimentados ven más contexto
    
    for m in history[-history_limit:]:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))
    
    # Añadir mensaje actual
    messages.append(HumanMessage(content=message))
    
    # Configurar LLM según tipo de usuario
    user_type = user_context.get("usage_patterns", {}).get("user_type", "casual_user")
    
    if user_type == "power_user":
        # Usuarios avanzados: respuestas más detalladas
        llm = get_llm(temperature=0.2, max_output_tokens=6000, streaming=True)
    elif user_type == "casual_user":
        # Usuarios casuales: respuestas más concisas
        llm = get_llm(temperature=0.4, max_output_tokens=3000, streaming=True)
    else:
        # Configuración estándar
        llm = get_llm(temperature=0.3, max_output_tokens=4096, streaming=True)
    
    # Generar respuesta streaming
    return llm.stream(messages)
