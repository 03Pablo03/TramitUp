import json
import logging
import re
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from app.core.auth import require_auth
from app.core.rate_limit import check_rate_limit, consume_rate_limit
from app.services.subscription_service import get_user_plan
from app.services.chat_service import run_chat, save_message
from app.ai.chains.deadline_extract_chain import extract_deadlines_from_response
from app.schemas.chat import ChatRequest, CompensationEstimate
from app.config.portals import get_portal, get_portal_summary
from app.ai.prompts.follow_up_suggestions import (
    FOLLOW_UP_PROMPT, DEFAULT_SUGGESTIONS, GENERIC_SUGGESTIONS,
)

logger = logging.getLogger(__name__)

router = APIRouter()


def extract_portal_key(text: str) -> str | None:
    """Extract portal key from LLM response."""
    match = re.search(r'\[PORTAL_KEY:\s*([^\]]+)\]', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_compensation_info(text: str) -> CompensationEstimate | None:
    """Extract compensation information from LLM response."""
    match = re.search(r'\[COMPENSATION:\s*([^\]]+)\]', text, re.IGNORECASE)
    if not match:
        return None
    
    comp_str = match.group(1).strip()
    
    # Parse compensation string: applies=true/false, amount=250/400/600, reason="explicación"
    applies = False
    amount = None
    reason = ""
    
    # Extract applies
    applies_match = re.search(r'applies=(true|false)', comp_str, re.IGNORECASE)
    if applies_match:
        applies = applies_match.group(1).lower() == 'true'
    
    # Extract amount
    amount_match = re.search(r'amount=(\d+)', comp_str)
    if amount_match:
        amount = int(amount_match.group(1))
    
    # Extract reason — accept single or double quotes, and unquoted text
    reason_match = re.search(r'reason=["\']([^"\']+)["\']', comp_str)
    if not reason_match:
        # Fallback: unquoted reason after last comma
        reason_match = re.search(r'reason=([^,\]]+)', comp_str)
    if reason_match:
        reason = reason_match.group(1).strip().strip("\"'")
    
    return CompensationEstimate(
        amount_eur=amount,
        applies=applies,
        reason=reason or "Información de compensación disponible"
    )


def clean_response_text(text: str, final: bool = False) -> str:
    """Remove special markers and any leaked internal metadata from response text for display."""
    # Markers de datos extraídos (portal, compensación, contactos) — procesados aparte
    text = re.sub(r'\[PORTAL_KEY:[^\]]+\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[COMPENSATION:[^\]]+\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[SPECIFIC_EMAIL:[^\]]+\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[SPECIFIC_URL:[^\]]+\]', '', text, flags=re.IGNORECASE)
    # Markers de contexto/instrucciones internas que nunca deben llegar al usuario
    text = re.sub(r'\[INSTRUCCIONES INTERNAS[^\]]*\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[CONTEXTO INTERNO[^\]]*\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[SISTEMA[^\]]*\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[DEBUG[^\]]*\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[INFO[^\]]*\]', '', text, flags=re.IGNORECASE)
    # Solo hacer strip en el texto final completo, nunca en chunks individuales
    # (strip en chunks elimina espacios entre palabras al concatenar)
    if final:
        return text.strip()
    return text


def _generate_follow_up_suggestions(
    classification: dict | None,
    user_message: str,
    assistant_text: str,
) -> list[str]:
    """Generate follow-up suggestions using LLM, with fallback to defaults."""
    category = (classification or {}).get("category", "")
    subcategory = (classification or {}).get("subcategory", "")

    try:
        from app.ai.llm_client import get_llm
        llm = get_llm(temperature=0.4, max_output_tokens=256, streaming=False)
        prompt = FOLLOW_UP_PROMPT.format(
            category=category or "general",
            subcategory=subcategory or "general",
            user_message=user_message[:300],
            assistant_summary=assistant_text[-500:] if len(assistant_text) > 500 else assistant_text,
        )
        response = llm.invoke(prompt)
        content = getattr(response, "content", str(response))
        lines = [line.strip() for line in content.strip().split("\n") if line.strip()]
        # Filtrar líneas demasiado largas o vacías
        suggestions = [l for l in lines if 5 <= len(l) <= 80][:3]
        if len(suggestions) >= 2:
            return suggestions
    except Exception as e:
        logger.debug("Follow-up suggestion generation failed: %s", e)

    # Fallback: try bot-specific suggestions first, then defaults
    try:
        from app.ai.bots.selector import select_bot
        bot = select_bot(classification or {}, user_message)
        if bot:
            bot_suggestions = bot.get_follow_up_suggestions(classification or {}, user_message)
            if bot_suggestions:
                return bot_suggestions[:3]
    except Exception:
        pass

    return DEFAULT_SUGGESTIONS.get(category, GENERIC_SUGGESTIONS)


async def generate_sse(user_id: str, request: ChatRequest):
    """SSE generator: yields chunks and saves full response when done."""
    user_plan = get_user_plan(user_id)
    allowed, _ = check_rate_limit(user_id, user_plan)
    if not allowed:
        yield {"data": json.dumps([{"type": "error", "message": "Has usado tus 2 consultas gratuitas de hoy. Con PRO tienes consultas ilimitadas."}])}
        return
    
    try:
        conv_id, classification, stream = run_chat(user_id, request.message, request.conversation_id, request.attachment_ids)
    except Exception as e:
        yield {"data": json.dumps([{"type": "error", "message": f"Error al iniciar el chat: {str(e)}"}])}
        return

    full = []
    success = False
    try:
        yield {"data": json.dumps([{"type": "conversation_id", "id": conv_id}])}
        # Emitir clasificación para que el frontend muestre badge de categoría
        if classification:
            logger.debug(
                "Classification: category=%s subcategory=%s urgency=%s keywords=%s",
                classification.get("category"),
                classification.get("subcategory"),
                classification.get("urgency"),
                classification.get("keywords"),
            )
            yield {"data": json.dumps([{
                "type": "classification",
                "category": classification.get("category", ""),
                "subcategory": classification.get("subcategory", ""),
            }])}
        for chunk in stream:
            # LangChain stream yields AIMessageChunk; extract .content (str)
            content = getattr(chunk, "content", chunk)
            if isinstance(content, list):
                text = "".join(str(c) for c in content if c)
            else:
                text = content if isinstance(content, str) else str(content or "")
            full.append(text)
            clean_chunk = clean_response_text(text)  # sin strip, preserva espacios
            yield {"data": json.dumps([{"type": "chunk", "content": clean_chunk}])}
        success = True
    except Exception as e:
        yield {"data": json.dumps([{"type": "error", "message": f"Error procesando respuesta: {str(e)}"}])}
    finally:
        if full and success:
            # Solo consumir rate limit si la respuesta fue exitosa
            consume_rate_limit(user_id, user_plan)
            full_text = "".join(full)
            
            # Extract portal and compensation information
            portal_key = extract_portal_key(full_text)
            compensation = extract_compensation_info(full_text)
            
            # Clean the text for storage (remove markers, strip solo en texto final)
            clean_text = clean_response_text(full_text, final=True)
            save_message(conv_id, "assistant", clean_text, user_id=user_id)
            
            # Send additional information
            deadlines = extract_deadlines_from_response(clean_text)
            if deadlines:
                yield {"data": json.dumps([{"type": "detected_deadlines", "deadlines": deadlines}])}
            
            if portal_key:
                portal_summary = get_portal_summary(portal_key)
                if portal_summary:
                    yield {"data": json.dumps([{"type": "portal_info", "portal_key": portal_key, "portal_summary": portal_summary}])}
            
            if compensation:
                yield {"data": json.dumps([{"type": "compensation_estimate", "compensation": {
                    "amount_eur": compensation.amount_eur,
                    "applies": compensation.applies,
                    "reason": compensation.reason
                }}])}

            # Generate follow-up suggestions
            try:
                suggestions = _generate_follow_up_suggestions(
                    classification, request.message, clean_text,
                )
                if suggestions:
                    yield {"data": json.dumps([{
                        "type": "follow_up_suggestions",
                        "suggestions": suggestions,
                    }])}
            except Exception as e:
                logger.debug("Failed to yield follow-up suggestions: %s", e)


@router.post("")
async def chat(
    request: ChatRequest,
    user_id: str = Depends(require_auth),
):
    """
    Mensaje al asistente. Respuesta por SSE streaming.
    Requiere autenticación. Rate limit: 2/día para plan free.
    """
    return EventSourceResponse(
        generate_sse(user_id, request),
        media_type="text/event-stream",
    )


@router.get("/portals/{category}")
async def get_portal_info(category: str):
    """
    Devuelve el portal oficial para una categoría.
    Útil para mostrar el botón "Ir al portal oficial" en el frontend.
    """
    portal = get_portal(category)
    if not portal:
        raise HTTPException(status_code=404, detail="Portal no encontrado")
    
    return {
        "name": portal.name,
        "url": portal.url,
        "needs_digital_cert": portal.needs_digital_cert,
        "also_by_post": portal.also_by_post,
        "notes": portal.notes,
        "last_verified": portal.last_verified,
    }
