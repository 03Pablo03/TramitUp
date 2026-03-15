from fastapi import APIRouter, Depends

from app.core.auth import require_auth
from app.schemas.me import UserProfile
from app.services.subscription_service import ensure_profile, get_user_plan, get_remaining_chats

router = APIRouter()


@router.get("", response_model=UserProfile)
def get_me(user_id: str = Depends(require_auth)):
    """Perfil y estado de suscripción del usuario."""
    profile = ensure_profile(user_id)
    if not profile:
        profile = {"id": user_id, "email": None, "plan": "free", "documents_used_today": 0}

    plan = get_user_plan(user_id)
    remaining = get_remaining_chats(user_id)
    return UserProfile(
        id=str(profile["id"]),
        email=profile.get("email"),
        plan=plan,
        documents_used_today=profile.get("documents_used_today", 0),
        remaining_chats_today=remaining,
    )
