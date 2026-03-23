import stripe
from app.core.config import get_settings
from app.core.supabase_client import get_supabase_client


def _init_stripe():
    settings = get_settings()
    stripe.api_key = settings.stripe_secret_key
    return settings


def get_stripe_customer_id(user_id: str, email: str | None) -> str | None:
    """Get or create Stripe customer for user."""
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("stripe_customer_id").eq("id", user_id).execute()
    if result.data and result.data[0].get("stripe_customer_id"):
        return result.data[0]["stripe_customer_id"]
    if not email:
        return None
    _init_stripe()
    customer = stripe.Customer.create(email=email)
    supabase.table("profiles").update({"stripe_customer_id": customer.id}).eq("id", user_id).execute()
    return customer.id


def create_checkout_session(
    user_id: str,
    price_type: str,  # "document" | "pro"
    email: str | None,
    success_url: str,
    cancel_url: str,
    trial_days: int | None = None,
) -> str:
    """Create Stripe Checkout session. Returns session URL."""
    settings = _init_stripe()
    price_id = settings.stripe_price_id_document if price_type == "document" else settings.stripe_price_id_pro
    customer_id = get_stripe_customer_id(user_id, email)
    mode = "payment" if price_type == "document" else "subscription"
    kwargs: dict = {
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
    # Add free trial for subscriptions — requires card upfront,
    # auto-charges after trial_days if not canceled.
    if mode == "subscription" and trial_days and trial_days > 0:
        kwargs["subscription_data"] = {"trial_period_days": trial_days}
        kwargs["payment_method_collection"] = "always"
    session = stripe.checkout.Session.create(**kwargs)
    return session.url


def get_subscription_info(user_id: str) -> dict | None:
    """Get active Stripe subscription details for a user.

    Returns dict with status, current_period_end, cancel_at_period_end,
    trial_end, or None if no subscription found.
    """
    _init_stripe()
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("stripe_customer_id").eq("id", user_id).execute()
    if not result.data or not result.data[0].get("stripe_customer_id"):
        return None

    customer_id = result.data[0]["stripe_customer_id"]
    subscriptions = stripe.Subscription.list(customer=customer_id, status="all", limit=1)
    if not subscriptions.data:
        return None

    sub = subscriptions.data[0]
    return {
        "subscription_id": sub.id,
        "status": sub.status,  # active, trialing, canceled, past_due, etc.
        "current_period_end": sub.current_period_end,  # unix timestamp
        "cancel_at_period_end": sub.cancel_at_period_end,
        "trial_end": sub.trial_end,  # unix timestamp or None
        "canceled_at": sub.canceled_at,  # unix timestamp or None
    }


def cancel_subscription(user_id: str) -> dict:
    """Cancel user's Stripe subscription at end of current period.

    Returns updated subscription info or raises ValueError.
    """
    _init_stripe()
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("stripe_customer_id").eq("id", user_id).execute()
    if not result.data or not result.data[0].get("stripe_customer_id"):
        raise ValueError("No se encontró cliente de Stripe asociado a tu cuenta.")

    customer_id = result.data[0]["stripe_customer_id"]
    subscriptions = stripe.Subscription.list(customer=customer_id, status="active", limit=1)

    # Also check trialing subscriptions
    if not subscriptions.data:
        subscriptions = stripe.Subscription.list(customer=customer_id, status="trialing", limit=1)

    if not subscriptions.data:
        raise ValueError("No tienes una suscripción activa.")

    sub = subscriptions.data[0]
    if sub.cancel_at_period_end:
        raise ValueError("Tu suscripción ya está programada para cancelarse.")

    # Cancel at period end — user keeps access until the period/trial ends
    updated = stripe.Subscription.modify(sub.id, cancel_at_period_end=True)
    return {
        "subscription_id": updated.id,
        "status": updated.status,
        "current_period_end": updated.current_period_end,
        "cancel_at_period_end": updated.cancel_at_period_end,
        "trial_end": updated.trial_end,
    }


def reactivate_subscription(user_id: str) -> dict:
    """Reactivate a subscription that was set to cancel at period end.

    Returns updated subscription info or raises ValueError.
    """
    _init_stripe()
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("stripe_customer_id").eq("id", user_id).execute()
    if not result.data or not result.data[0].get("stripe_customer_id"):
        raise ValueError("No se encontró cliente de Stripe asociado a tu cuenta.")

    customer_id = result.data[0]["stripe_customer_id"]
    # Look for subscriptions that are still active but set to cancel
    subscriptions = stripe.Subscription.list(customer=customer_id, status="active", limit=1)
    if not subscriptions.data:
        subscriptions = stripe.Subscription.list(customer=customer_id, status="trialing", limit=1)

    if not subscriptions.data:
        raise ValueError("No tienes una suscripción que reactivar.")

    sub = subscriptions.data[0]
    if not sub.cancel_at_period_end:
        raise ValueError("Tu suscripción ya está activa.")

    updated = stripe.Subscription.modify(sub.id, cancel_at_period_end=False)
    return {
        "subscription_id": updated.id,
        "status": updated.status,
        "current_period_end": updated.current_period_end,
        "cancel_at_period_end": updated.cancel_at_period_end,
        "trial_end": updated.trial_end,
    }


def handle_webhook(payload: bytes, sig: str) -> bool:
    """Process Stripe webhook. Returns True if handled."""
    settings = _init_stripe()
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
        # Activate plan immediately (including during trial — user gets access right away)
        if price_type == "pro":
            supabase.table("profiles").update({"plan": "pro"}).eq("id", user_id).execute()
        else:
            supabase.table("profiles").update({"plan": "document"}).eq("id", user_id).execute()
    elif event["type"] == "customer.subscription.deleted":
        # Subscription canceled or trial ended without payment
        subscription = event["data"]["object"]
        customer_id = subscription.get("customer")
        if customer_id:
            supabase = get_supabase_client()
            result = supabase.table("profiles").select("id").eq("stripe_customer_id", customer_id).execute()
            if result.data:
                user_id = result.data[0]["id"]
                supabase.table("profiles").update({"plan": "free"}).eq("id", user_id).execute()
    return True
