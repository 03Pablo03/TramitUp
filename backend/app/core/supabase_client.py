from functools import lru_cache

from supabase import create_client, Client
from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """Returns a singleton Supabase client. Reuses the HTTP connection pool."""
    settings = get_settings()
    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )
