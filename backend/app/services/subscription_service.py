from datetime import date, datetime, timezone
from app.core.supabase_client import get_supabase_client
from app.core.cache import cached, invalidate_cache_pattern
from app.core.rate_limit import FREE_DAILY_LIMIT, get_remaining_chats as rate_limit_remaining


@cached(ttl=300, key_prefix="user_plan")
def get_user_plan(user_id: str) -> str:
    """Get user plan from profiles. Defaults to 'free'. Cached for 5 minutes."""
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("plan").eq("id", user_id).execute()
    if result.data and len(result.data) > 0:
        return result.data[0].get("plan", "free")
    return "free"


def has_document_access(user_id: str, conversation_id: str | None = None) -> bool:
    """
    True si el usuario puede generar modelos de escritos.
    PRO/document: siempre. Free: requiere document_unlock por conversación (futuro).
    """
    plan = get_user_plan(user_id)
    if plan in ("pro", "premium", "document"):
        return True
    # TODO: comprobar document_unlock para conversation_id cuando exista la tabla
    return False


@cached(ttl=300, key_prefix="user_profile")
def get_profile(user_id: str) -> dict | None:
    """Get full profile. Creates one if missing. Cached for 5 minutes."""
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]
    return None


def ensure_profile(user_id: str, email: str | None = None) -> dict:
    """Upsert profile. Returns profile dict."""
    supabase = get_supabase_client()
    today = date.today().isoformat()

    result = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if result.data and len(result.data) > 0:
        profile = result.data[0]
        last_reset = profile.get("last_reset_date")
        if last_reset and str(last_reset) != today:
            # Reset daily counts
            supabase.table("profiles").update({
                "documents_used_today": 0,
                "last_reset_date": today,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }).eq("id", user_id).execute()
            profile["documents_used_today"] = 0
            profile["last_reset_date"] = today
        return profile

    # Create new profile
    supabase.table("profiles").insert({
        "id": user_id,
        "email": email,
        "plan": "free",
        "documents_used_today": 0,
        "last_reset_date": today,
    }).execute()
    return {
        "id": user_id,
        "email": email,
        "plan": "free",
        "documents_used_today": 0,
        "last_reset_date": today,
    }


def get_remaining_chats(user_id: str) -> int:
    """-1 = unlimited, else count."""
    plan = get_user_plan(user_id)
    return rate_limit_remaining(user_id, plan)
