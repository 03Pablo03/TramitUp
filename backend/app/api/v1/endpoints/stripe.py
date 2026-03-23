from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.core.auth import require_auth
from app.core.config import get_settings
from app.services.subscription_service import ensure_profile
from app.services.stripe_service import create_checkout_session, handle_webhook

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


@router.post("/webhook")
async def stripe_webhook(req: Request):
    """Webhook de Stripe - no requiere auth."""
    from fastapi.responses import JSONResponse
    payload = await req.body()
    sig = req.headers.get("stripe-signature", "")
    if handle_webhook(payload, sig):
        return {"received": True}
    return JSONResponse(content={"received": False}, status_code=400)
