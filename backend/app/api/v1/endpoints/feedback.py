"""
Endpoints para feedback de mensajes (thumbs up/down).
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth import require_auth
from app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)
router = APIRouter()


class FeedbackRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1)
    message_index: int = Field(..., ge=0)
    rating: str = Field(..., pattern="^(positive|negative)$")
    comment: str | None = Field(None, max_length=500)


@router.post("")
async def submit_feedback(
    body: FeedbackRequest,
    user_id: str = Depends(require_auth),
):
    """Envía feedback sobre un mensaje del asistente."""
    supabase = get_supabase_client()

    # Check if feedback already exists for this message
    existing = (
        supabase.table("message_feedback")
        .select("id")
        .eq("conversation_id", body.conversation_id)
        .eq("message_index", body.message_index)
        .eq("user_id", user_id)
        .execute()
    )

    if existing.data:
        # Update existing feedback
        supabase.table("message_feedback").update({
            "rating": body.rating,
            "comment": body.comment,
        }).eq("id", existing.data[0]["id"]).execute()
        return {"success": True, "action": "updated"}

    # Create new feedback
    supabase.table("message_feedback").insert({
        "conversation_id": body.conversation_id,
        "message_index": body.message_index,
        "user_id": user_id,
        "rating": body.rating,
        "comment": body.comment,
    }).execute()
    return {"success": True, "action": "created"}


@router.get("/{conversation_id}")
async def get_feedback(
    conversation_id: str,
    user_id: str = Depends(require_auth),
):
    """Obtiene feedback del usuario para una conversación."""
    supabase = get_supabase_client()
    result = (
        supabase.table("message_feedback")
        .select("message_index, rating, comment")
        .eq("conversation_id", conversation_id)
        .eq("user_id", user_id)
        .execute()
    )
    # Return as map: {message_index: rating}
    feedback_map = {r["message_index"]: r["rating"] for r in (result.data or [])}
    return {"success": True, "data": feedback_map}
