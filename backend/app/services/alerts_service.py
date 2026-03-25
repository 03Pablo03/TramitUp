"""
Servicio de alertas de plazos legales.
"""
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from app.core.supabase_client import get_supabase_client

MAX_ALERTS_PER_USER = 50


def _compute_deadline(reference_date: Optional[str], days: int, business_days: bool) -> Optional[date]:
    """Calcula fecha límite desde reference_date + days."""
    if not reference_date:
        return None
    try:
        start = datetime.strptime(reference_date[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None
    if business_days:
        d = start
        remaining = days
        while remaining > 0:
            d += timedelta(days=1)
            if d.weekday() < 5:
                remaining -= 1
        return d
    return start + timedelta(days=days)


def create_alert(
    user_id: str,
    conversation_id: Optional[str],
    description: str,
    deadline_date: date,
    law_reference: Optional[str] = None,
    notify_days_before: Optional[list[int]] = None,
) -> dict:
    """Crea una alerta. Raises ValueError si no válida."""
    if deadline_date <= date.today():
        raise ValueError("La fecha límite debe ser futura")
    supabase = get_supabase_client()
    rcount = supabase.table("alerts").select("id", count="exact", head=True).eq(
        "user_id", user_id
    ).eq("status", "active").execute()
    n = getattr(rcount, "count", None) or 0
    if n >= MAX_ALERTS_PER_USER:
        raise ValueError(f"Máximo {MAX_ALERTS_PER_USER} alertas activas por usuario")
    notify = notify_days_before or [7, 3, 1]
    row = {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "description": description,
        "deadline_date": deadline_date.isoformat(),
        "law_reference": law_reference,
        "notify_days_before": notify,
        "status": "active",
    }
    r = supabase.table("alerts").insert(row).execute()
    inserted = r.data[0]
    scheduled = [(deadline_date - timedelta(days=d)).isoformat() for d in sorted(notify, reverse=True)]
    inserted["notifications_scheduled"] = scheduled
    return inserted


def list_alerts(user_id: str, status_filter: Optional[str] = None) -> list[dict]:
    """Lista alertas del usuario ordenadas por deadline_date."""
    supabase = get_supabase_client()
    q = supabase.table("alerts").select(
        "id, conversation_id, description, deadline_date, law_reference, "
        "status, notify_days_before, created_at"
    ).eq("user_id", user_id).order("deadline_date", desc=False)
    if status_filter:
        q = q.eq("status", status_filter)
    r = q.execute()
    alerts = r.data or []
    if not alerts:
        return []

    # Fetch ALL notifications in one query to avoid N+1
    alert_ids = [a["id"] for a in alerts]
    notif_r = supabase.table("alert_notifications").select("alert_id, sent_at").in_(
        "alert_id", alert_ids
    ).execute()
    notif_by_alert: dict[str, list[str]] = {}
    for n in (notif_r.data or []):
        aid = n["alert_id"]
        notif_by_alert.setdefault(aid, []).append(str(n.get("sent_at", ""))[:10])

    today = date.today()
    result = []
    for row in alerts:
        dd = row.get("deadline_date")
        if isinstance(dd, str):
            try:
                d = datetime.strptime(dd[:10], "%Y-%m-%d").date()
            except ValueError:
                d = today
        else:
            d = dd if hasattr(dd, "year") else today
        days_remaining = (d - today).days
        urgency = "high" if days_remaining <= 3 else "medium" if days_remaining <= 7 else "low"
        result.append({
            "alert_id": row["id"],
            "conversation_id": row.get("conversation_id"),
            "description": row["description"],
            "deadline_date": dd,
            "law_reference": row.get("law_reference"),
            "days_remaining": max(0, days_remaining),
            "urgency": urgency,
            "status": row.get("status", "active"),
            "notifications_sent": notif_by_alert.get(row["id"], []),
            "created_at": row.get("created_at"),
        })
    return result


def update_alert(alert_id: str, user_id: str, status: Optional[str] = None, deadline_date: Optional[date] = None) -> dict:
    """Actualiza o descarta una alerta."""
    supabase = get_supabase_client()
    existing = supabase.table("alerts").select("*").eq("id", alert_id).eq("user_id", user_id).execute()
    if not existing.data:
        raise ValueError("Alerta no encontrada")
    updates = {"updated_at": datetime.now(timezone.utc).isoformat()}
    if status is not None:
        updates["status"] = status
    if deadline_date is not None:
        if deadline_date <= date.today():
            raise ValueError("La fecha límite debe ser futura")
        updates["deadline_date"] = deadline_date.isoformat()
    supabase.table("alerts").update(updates).eq("id", alert_id).eq("user_id", user_id).execute()
    return {**existing.data[0], **updates}


def delete_alert(alert_id: str, user_id: str) -> None:
    supabase = get_supabase_client()
    r = supabase.table("alerts").delete().eq("id", alert_id).eq("user_id", user_id).execute()
    if not r.data:
        raise ValueError("Alerta no encontrada")


def compute_deadline_from_detected(detected: dict, fallback_reference: Optional[date] = None) -> Optional[date]:
    """Calcula deadline_date desde un detected_deadline."""
    ref = detected.get("reference_date")
    days = detected.get("days") or 0
    business = detected.get("business_days", True)
    if ref:
        return _compute_deadline(ref, days, business)
    if fallback_reference and days:
        start_str = fallback_reference.isoformat()
        return _compute_deadline(start_str, days, business)
    return None
