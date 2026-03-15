from fastapi import APIRouter, Body, Depends, HTTPException

from app.core.auth import require_auth
from app.core.supabase_client import get_supabase_client

router = APIRouter()


@router.get("/{conversation_id}/messages")
def get_messages(conversation_id: str, user_id: str = Depends(require_auth)):
    """Obtiene los mensajes de una conversación."""
    supabase = get_supabase_client()
    conv = supabase.table("conversations").select("id").eq("id", conversation_id).eq("user_id", user_id).execute()
    if not conv.data:
        raise HTTPException(404, "Conversación no encontrada")
    result = supabase.table("messages").select("role, content, created_at").eq(
        "conversation_id", conversation_id
    ).order("created_at", desc=False).execute()
    return {"messages": result.data or []}


@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str, user_id: str = Depends(require_auth)):
    """Elimina una conversación y sus mensajes."""
    supabase = get_supabase_client()
    conv = supabase.table("conversations").select("id").eq("id", conversation_id).eq("user_id", user_id).execute()
    if not conv.data:
        raise HTTPException(404, "Conversación no encontrada")
    supabase.table("messages").delete().eq("conversation_id", conversation_id).execute()
    supabase.table("conversations").delete().eq("id", conversation_id).eq("user_id", user_id).execute()
    return {"ok": True}


@router.patch("/{conversation_id}")
def update_conversation(
    conversation_id: str,
    body: dict = Body(default={}),
    user_id: str = Depends(require_auth),
):
    """Actualiza una conversación (ej. título)."""
    supabase = get_supabase_client()
    conv = supabase.table("conversations").select("id").eq("id", conversation_id).eq("user_id", user_id).execute()
    if not conv.data:
        raise HTTPException(404, "Conversación no encontrada")
    updates = {}
    if "title" in body:
        updates["title"] = str(body["title"])[:120]
    if not updates:
        return {"ok": True}
    supabase.table("conversations").update(updates).eq("id", conversation_id).eq("user_id", user_id).execute()
    return {"ok": True}
