import stripe
from app.core.config import get_settings
from app.core.supabase_client import get_supabase_client


def get_stripe_customer_id(user_id: str, email: str | None) -> str | None:
    """Get or create Stripe customer for user."""
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("stripe_customer_id").eq("id", user_id).execute()
    if result.data and result.data[0].get("stripe_customer_id"):
        return result.data[0]["stripe_customer_id"]
    if not email:
        return None
    customer = stripe.Customer.create(email=email)
    supabase.table("profiles").update({"stripe_customer_id": customer.id}).eq("id", user_id).execute()
    return customer.id


def create_checkout_session(
    user_id: str,
    price_type: str,  # "document" | "pro"
    email: str | None,
    success_url: str,
    cancel_url: str,
) -> str:
    """Create Stripe Checkout session. Returns session URL."""
    settings = get_settings()
    stripe.api_key = settings.stripe_secret_key
    price_id = settings.stripe_price_id_document if price_type == "document" else settings.stripe_price_id_pro
    customer_id = get_stripe_customer_id(user_id, email)
    mode = "payment" if price_type == "document" else "subscription"
    kwargs = {
        "mode": mode,
        "line_items": [{"price": price_id, "quantity": 1}],
        "success_url": success_url,
        "cancel_url": cancel_url,
        "metadata": {"user_id": user_id, "price_type": price_type},
    }
    if customer_id:
        kwargs["customer"] = customer_id
    elif email:
        kwargs["customer_email"] = email
    session = stripe.checkout.Session.create(**kwargs)
    return session.url


def handle_webhook(payload: bytes, sig: str) -> bool:
    """Process Stripe webhook. Returns True if handled."""
    settings = get_settings()
    stripe.api_key = get_settings().stripe_secret_key
    try:
        event = stripe.Webhook.construct_event(payload, sig, settings.stripe_webhook_secret)
    except Exception:
        return False
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")
        price_type = session.get("metadata", {}).get("price_type", "document")
        if not user_id:
            return True
        supabase = get_supabase_client()
        if price_type == "pro":
            supabase.table("profiles").update({"plan": "pro"}).eq("id", user_id).execute()
        else:
            supabase.table("profiles").update({"plan": "document"}).eq("id", user_id).execute()
    return True
