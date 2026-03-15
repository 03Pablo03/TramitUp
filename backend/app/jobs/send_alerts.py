"""
Cron job diario: envía emails de alerta para plazos que vencen en X días.
Ejecutar: python -m app.jobs.send_alerts
"""
from datetime import date, datetime
from app.core.supabase_client import get_supabase_client
from app.services.email_service import send_deadline_alert


def run_send_alerts():
    """Sincrónico para Railway cron."""
    today = date.today()
    supabase = get_supabase_client()

    expired = (
        supabase.table("alerts")
        .select("id")
        .eq("status", "active")
        .lt("deadline_date", today.isoformat())
        .execute()
    )
    for row in (expired.data or []):
        supabase.table("alerts").update({"status": "expired"}).eq(
            "id", row["id"]
        ).execute()

    alerts = (
        supabase.table("alerts")
        .select("id, user_id, description, deadline_date, law_reference, notify_days_before")
        .eq("status", "active")
        .execute()
    )

    sent_count = 0
    for row in (alerts.data or []):
        dd_str = row.get("deadline_date")
        try:
            dd = datetime.strptime(dd_str[:10], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            continue
        days_remaining = (dd - today).days

        if days_remaining < 0:
            continue

        notify_days = row.get("notify_days_before") or [7, 3, 1]
        if days_remaining not in notify_days:
            continue

        notif = (
            supabase.table("alert_notifications")
            .select("id")
            .eq("alert_id", row["id"])
            .eq("days_before", days_remaining)
            .execute()
        )
        if notif.data:
            continue

        profile = supabase.table("profiles").select("email, name").eq(
            "id", row["user_id"]
        ).execute()
        prof = (profile.data or [{}])[0] if profile.data else {}
        email = prof.get("email")
        if not email:
            continue
        user_name = prof.get("name")

        email_id = send_deadline_alert(
            to_email=email,
            user_name=user_name,
            description=row["description"],
            deadline_date=dd,
            days_remaining=days_remaining,
            law_reference=row.get("law_reference") or "",
            alert_id=row["id"],
        )
        if email_id:
            supabase.table("alert_notifications").insert({
                "alert_id": row["id"],
                "days_before": days_remaining,
                "email_id": email_id,
            }).execute()
            sent_count += 1

    return sent_count


if __name__ == "__main__":
    n = run_send_alerts()
    print(f"Enviadas {n} notificaciones de alerta")
