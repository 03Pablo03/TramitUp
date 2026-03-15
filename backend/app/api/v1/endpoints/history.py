from fastapi import APIRouter, Depends

from app.core.auth import require_auth
from app.core.supabase_client import get_supabase_client

router = APIRouter()


@router.get("")
def get_history(user_id: str = Depends(require_auth)):
    """Historial de conversaciones y documentos del usuario."""
    supabase = get_supabase_client()
    convs = supabase.table("conversations").select("id, title, category, created_at").eq(
        "user_id", user_id
    ).order("created_at", desc=True).limit(50).execute()
    docs = supabase.table("documents").select("id, title, category, created_at").eq(
        "user_id", user_id
    ).order("created_at", desc=True).limit(50).execute()
    return {
        "conversations": convs.data or [],
        "documents": docs.data or [],
    }
