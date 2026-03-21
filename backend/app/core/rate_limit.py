from datetime import date
from zoneinfo import ZoneInfo
from collections import defaultdict
from typing import Dict

from app.core.config import get_settings

# In-memory fallback when Supabase daily_usage not available
_rate_limit_store: Dict[str, dict] = defaultdict(lambda: {"count": 0, "date": None})

FREE_DAILY_LIMIT = 2

_MADRID = ZoneInfo("Europe/Madrid")


def _get_today() -> str:
    """Returns today's date in Spain timezone (resets at midnight Madrid time)."""
    from datetime import datetime
    return datetime.now(tz=_MADRID).date().isoformat()


def _use_daily_usage_table() -> bool:
    """Use Supabase daily_usage if configured."""
    s = get_settings()
    return bool(s.supabase_url and s.supabase_service_role_key)


def check_rate_limit(user_id: str, plan: str) -> tuple[bool, int]:
    """
    Returns (allowed, remaining).
    Free users: 2 requests/day. Document/Pro: unlimited.
    """
    if plan in ("document", "pro"):
        return True, -1

    if _use_daily_usage_table():
        try:
            from app.core.supabase_client import get_supabase_client
            supabase = get_supabase_client()
            today = _get_today()
            r = supabase.table("daily_usage").select("message_count").eq("user_id", user_id).eq("date", today).execute()
            count = r.data[0]["message_count"] if r.data else 0
            if count >= FREE_DAILY_LIMIT:
                return False, 0
            return True, FREE_DAILY_LIMIT - count - 1
        except Exception:
            pass  # fallback to in-memory

    from datetime import datetime
    today = datetime.now(tz=_MADRID).date()
    data = _rate_limit_store[user_id]
    if data["date"] != today:
        data["date"] = today
        data["count"] = 0
    if data["count"] >= FREE_DAILY_LIMIT:
        return False, 0
    return True, FREE_DAILY_LIMIT - data["count"] - 1


def consume_rate_limit(user_id: str, plan: str) -> None:
    """Consume one request from rate limit."""
    if plan in ("document", "pro"):
        return
    if _use_daily_usage_table():
        try:
            from app.core.supabase_client import get_supabase_client
            supabase = get_supabase_client()
            today = _get_today()
            r = supabase.table("daily_usage").select("message_count").eq("user_id", user_id).eq("date", today).execute()
            if r.data:
                new_count = r.data[0]["message_count"] + 1
                supabase.table("daily_usage").update({"message_count": new_count}).eq("user_id", user_id).eq("date", today).execute()
            else:
                supabase.table("daily_usage").insert({"user_id": user_id, "date": today, "message_count": 1}).execute()
            return
        except Exception:
            pass
    from datetime import datetime
    today = datetime.now(tz=_MADRID).date()
    data = _rate_limit_store[user_id]
    if data["date"] != today:
        data["date"] = today
        data["count"] = 0
    data["count"] += 1


def get_remaining_chats(user_id: str, plan: str) -> int:
    """Returns -1 for unlimited, else count remaining today."""
    if plan in ("document", "pro"):
        return -1
    if _use_daily_usage_table():
        try:
            from app.core.supabase_client import get_supabase_client
            supabase = get_supabase_client()
            today = _get_today()
            r = supabase.table("daily_usage").select("message_count").eq("user_id", user_id).eq("date", today).execute()
            count = r.data[0]["message_count"] if r.data else 0
            return max(0, FREE_DAILY_LIMIT - count)
        except Exception:
            pass
    from datetime import datetime
    today = datetime.now(tz=_MADRID).date()
    data = _rate_limit_store[user_id]
    if data["date"] != today:
        return FREE_DAILY_LIMIT
    return max(0, FREE_DAILY_LIMIT - data["count"])
