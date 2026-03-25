from app.ai.chains.classify_chain import classify_tramite
from app.ai.chains.chat_chain import stream_chat_response, build_chat_prompt
from app.ai.rag.retriever import retrieve_context
from app.ai.bots.selector import select_bot
from app.core.supabase_client import get_supabase_client
from app.services.personalization_service import personalization_service
from app.services.document_analysis_service import document_analysis_service
from app.ai.llm_client import get_llm

_PRO_PLANS = {"pro", "premium", "document"}


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


def get_conversation_messages(conversation_id: str, user_id: str, limit: int = 20) -> list[dict]:
    """Get recent messages for a conversation. Verifies ownership via conversation."""
    supabase = get_supabase_client()
    # Verify ownership before fetching messages
    conv = supabase.table("conversations").select("id").eq(
        "id", conversation_id
    ).eq("user_id", user_id).execute()
    if not conv.data:
        return []
    result = supabase.table("messages").select("role, content").eq(
        "conversation_id", conversation_id
    ).order("created_at", desc=False).limit(limit).execute()
    return [{"role": r["role"], "content": r["content"]} for r in (result.data or [])]


def save_message(conversation_id: str, role: str, content: str, user_id: str | None = None) -> None:
    """Save a message to the conversation."""
    supabase = get_supabase_client()
    # Verify ownership if user_id provided
    if user_id:
        conv = supabase.table("conversations").select("id").eq(
            "id", conversation_id
        ).eq("user_id", user_id).execute()
        if not conv.data:
            return
    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
    }).execute()


def update_conversation_title(conversation_id: str, title: str, user_id: str | None = None) -> None:
    supabase = get_supabase_client()
    query = supabase.table("conversations").update({"title": title}).eq("id", conversation_id)
    if user_id:
        query = query.eq("user_id", user_id)
    query.execute()


def get_or_create_conversation(
    user_id: str,
    conversation_id: str | None,
    first_message: str,
    classification: dict | None,
) -> str:
    """Get existing conversation or create new one. Update title, category, subcategory if new."""
    if conversation_id:
        # Verify ownership — never trust a caller-supplied conversation_id
        supabase = get_supabase_client()
        conv = supabase.table("conversations").select("id").eq(
            "id", conversation_id
        ).eq("user_id", user_id).execute()
        if conv.data:
            return conversation_id
        # If not owned by user, create a new one instead
    c = classification or {}
    title = c.get("titulo_resumen", first_message[:60] or "Nueva conversación")[:80]
    return create_conversation(
        user_id,
        title,
        category=c.get("category"),
        subcategory=c.get("subcategory"),
    )


def _format_contract_analysis_for_chat(analysis: dict) -> str:
    """Formatea el análisis de contrato como contexto de texto para el LLM."""
    tipo = analysis.get("tipo_contrato", "contrato")
    resumen = analysis.get("resumen", "")
    clausulas = analysis.get("clausulas", [])
    recomendacion = analysis.get("recomendacion_general", "")

    lines = [
        "=== ANÁLISIS JURÍDICO DEL CONTRATO ADJUNTO ===",
        f"Tipo: {tipo.upper()}",
    ]
    if resumen:
        lines.append(f"Resumen: {resumen}")
    if clausulas:
        lines.append("\nCLÁUSULAS PROBLEMÁTICAS DETECTADAS:")
        risk_icons = {"alto": "🔴", "medio": "🟡", "bajo": "🔵"}
        for c in clausulas:
            icon = risk_icons.get(c.get("riesgo", ""), "⚠️")
            lines.append(f"\n{icon} [{c.get('riesgo', '').upper()}] {c.get('titulo', '')}")
            if c.get("fragmento"):
                lines.append(f'   Cláusula: "{c["fragmento"][:200]}"')
            if c.get("problema"):
                lines.append(f"   Problema: {c['problema']}")
            if c.get("base_legal"):
                lines.append(f"   Base legal: {c['base_legal']}")
            if c.get("accion"):
                lines.append(f"   Acción recomendada: {c['accion']}")
    if recomendacion:
        lines.append(f"\nRecomendación general: {recomendacion}")
    lines.append("=== FIN ANÁLISIS DE CONTRATO ===")
    return "\n".join(lines)


def _get_contract_analysis_context(attachment_ids: list[str], user_id: str) -> str:
    """
    Si los adjuntos contienen contratos de alquiler/laboral, devuelve análisis jurídico
    estructurado para incluir en el contexto del LLM.
    """
    try:
        from app.services.contract_analysis_service import analyze_contract_from_text
        texts = document_analysis_service.get_attachment_texts(attachment_ids, user_id)
        if not texts:
            return ""
        results = []
        for texto in texts:
            analysis = analyze_contract_from_text(texto)
            if analysis:
                results.append(_format_contract_analysis_for_chat(analysis))
        return "\n\n".join(results)
    except Exception:
        return ""


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

    # Análisis especializado de contratos (alquiler/laboral) para usuarios PRO
    contract_analysis_context = ""
    if attachment_ids:
        from app.services.subscription_service import get_user_plan
        if get_user_plan(user_id) in _PRO_PLANS:
            contract_analysis_context = _get_contract_analysis_context(attachment_ids, user_id)

    # Combinar mensaje con contexto de documentos para clasificación
    full_message = message
    if attachment_context:
        full_message = f"{message}\n\n{attachment_context}"
    if contract_analysis_context:
        full_message = f"{full_message}\n\n{contract_analysis_context}"

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
    # Añadir análisis de contrato al RAG (con máxima prioridad para el LLM)
    if contract_analysis_context:
        rag_context = f"{contract_analysis_context}\n\n{rag_context}"
    
    conv_id = get_or_create_conversation(user_id, conversation_id, message, classification)
    history = get_conversation_messages(conv_id, user_id) if conv_id else []
    save_message(conv_id, "user", message, user_id=user_id)

    # Si hay documentos adjuntos, incluir su contenido en el mensaje al LLM
    message_for_ai = full_message if attachment_context else message
    stream = stream_chat_response_personalized(message_for_ai, rag_context, classification, history, user_context)
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
    Selecciona un bot especializado si la clasificación lo requiere.
    """
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

    # Construir prompt personalizado
    personalized_additions = personalization_service.get_contextual_prompt_additions(user_context)
    base_prompt = build_chat_prompt(rag_context, classification)
    personalized_prompt = base_prompt + personalized_additions

    # Select specialized bot and extend prompt
    bot = select_bot(classification, message)
    if bot:
        bot_extension = bot.get_prompt_extension(classification, message)
        personalized_prompt = personalized_prompt + "\n" + bot_extension

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

    # Configure LLM: bot settings take priority, then user type
    if bot:
        temperature = bot.get_temperature()
        max_tokens = bot.get_max_tokens()
    else:
        user_type = user_context.get("usage_patterns", {}).get("user_type", "casual_user")
        if user_type == "power_user":
            temperature, max_tokens = 0.2, 6000
        elif user_type == "casual_user":
            temperature, max_tokens = 0.4, 3000
        else:
            temperature, max_tokens = 0.3, 4096

    llm = get_llm(temperature=temperature, max_output_tokens=max_tokens, streaming=True)

    # Generar respuesta streaming
    return llm.stream(messages)
