from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.auth import require_auth
from app.core.config import get_settings
from app.services.subscription_service import ensure_profile
from app.services.stripe_service import (
    create_checkout_session,
    handle_webhook,
    get_subscription_info,
    cancel_subscription,
    reactivate_subscription,
)

router = APIRouter()


class StripeCheckoutRequest(BaseModel):
    price_type: str = "document"  # document | pro
    trial_days: int | None = None  # e.g. 3 for 3-day free trial


@router.post("/checkout")
def stripe_checkout(
    body: StripeCheckoutRequest,
    user_id: str = Depends(require_auth),
):
    """Crea sesión de pago Stripe y devuelve URL de redirect."""
    price_type = body.price_type
    if price_type not in ("document", "pro"):
        price_type = "document"
    profile = ensure_profile(user_id)
    settings = get_settings()
    success_url = f"{settings.frontend_url}/account?success=1"
    cancel_url = f"{settings.frontend_url}/account?canceled=1"
    trial_days = body.trial_days if price_type == "pro" and body.trial_days and body.trial_days > 0 else None
    url = create_checkout_session(
        user_id, price_type, profile.get("email"), success_url, cancel_url, trial_days=trial_days
    )
    return {"url": url}


@router.get("/subscription")
def get_subscription(user_id: str = Depends(require_auth)):
    """Devuelve info de la suscripción activa del usuario."""
    info = get_subscription_info(user_id)
    if not info:
        return {"subscription": None}
    return {"subscription": info}


@router.post("/subscription/cancel")
def cancel_sub(user_id: str = Depends(require_auth)):
    """Cancela la suscripción al final del periodo actual."""
    try:
        result = cancel_subscription(user_id)
        return {"ok": True, "subscription": result}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


@router.post("/subscription/reactivate")
def reactivate_sub(user_id: str = Depends(require_auth)):
    """Reactiva una suscripción programada para cancelarse."""
    try:
        result = reactivate_subscription(user_id)
        return {"ok": True, "subscription": result}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


@router.post("/webhook")
async def stripe_webhook(req: Request):
    """Webhook de Stripe - no requiere auth."""
    payload = await req.body()
    sig = req.headers.get("stripe-signature", "")
    if handle_webhook(payload, sig):
        return {"received": True}
    return JSONResponse(content={"received": False}, status_code=400)
