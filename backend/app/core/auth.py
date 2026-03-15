from typing import Optional
import logging
import jwt
import base64
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import get_settings

security = HTTPBearer(auto_error=False)
logger = logging.getLogger(__name__)


def _verify_jwt_local(token: str) -> Optional[str]:
    """
    Fast local JWT verification. Tries the secret both as a raw string
    and as base64-decoded bytes (Supabase stores it base64-encoded).
    Returns user_id (sub) if valid, None otherwise.
    """
    settings = get_settings()
    secret_raw = settings.supabase_jwt_secret.strip()
    if not secret_raw:
        logger.warning("SUPABASE_JWT_SECRET is empty — skipping local JWT verification")
        return None

    candidates: list[str | bytes] = [secret_raw]
    try:
        candidates.append(base64.b64decode(secret_raw))
    except Exception:
        pass

    for key in candidates:
        try:
            payload = jwt.decode(
                token,
                key,
                audience="authenticated",
                algorithms=["HS256"],
            )
            return payload.get("sub")
        except jwt.PyJWTError:
            continue

    return None


def _verify_jwt_supabase(token: str) -> Optional[str]:
    """
    Fallback: verify token against the Supabase Auth API.
    Slower (network call) but always correct regardless of secret format.
    """
    try:
        from app.core.supabase_client import get_supabase_client
        supabase = get_supabase_client()
        response = supabase.auth.get_user(token)
        if response.user:
            return response.user.id
    except Exception as e:
        logger.debug("Supabase token verification failed: %s", e)
    return None


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[str]:
    """
    Validates JWT from Supabase and returns user_id.
    Returns None if no token provided (for optional auth routes).
    """
    if not credentials or not credentials.credentials:
        return None

    token = credentials.credentials

    user_id = _verify_jwt_local(token)
    if user_id:
        return user_id

    # Local verification failed — fall back to Supabase API
    logger.debug("Local JWT verification failed, trying Supabase API")
    return _verify_jwt_supabase(token)


async def require_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> str:
    """
    Requires valid JWT. Raises 401 if missing or invalid.
    """
    user_id = await get_current_user_id(credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado. Inicia sesión para continuar.",
        )
    return user_id
