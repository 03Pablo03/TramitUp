"""
Servicio del dashboard.
Agrega datos de alertas, expedientes, conversaciones y calendario legal
para presentar al usuario un resumen accionable de su situación.
"""
import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any

from app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

# ── Calendario legal español (fechas recurrentes) ─────────────────────────────
LEGAL_CALENDAR = [
    {
        "month": 4, "day": 1, "end_month": 6, "end_day": 30,
        "title": "Campaña de la Renta (IRPF)",
        "category": "fiscal",
        "description": "Plazo para presentar la declaración del IRPF del ejercicio anterior.",
        "icon": "📋",
    },
    {
        "month": 1, "day": 1, "end_month": 1, "end_day": 31,
        "title": "Actualización IPC alquileres",
        "category": "vivienda",
        "description": "Los alquileres pueden actualizarse según el IPC u otro índice pactado.",
        "icon": "🏠",
    },
    {
        "month": 1, "day": 1, "end_month": 1, "end_day": 31,
        "title": "Renovación tácita de contratos de alquiler",
        "category": "vivienda",
        "description": "Los contratos de alquiler pueden renovarse tácitamente si no se notifica con antelación.",
        "icon": "📝",
    },
    {
        "month": 6, "day": 1, "end_month": 6, "end_day": 25,
        "title": "Presentación Impuesto de Sociedades",
        "category": "fiscal",
        "description": "Plazo para la declaración del Impuesto de Sociedades (modelo 200).",
        "icon": "🏢",
    },
    {
        "month": 10, "day": 1, "end_month": 10, "end_day": 20,
        "title": "Pago fraccionado IRPF (3T)",
        "category": "fiscal",
        "description": "Tercer pago fraccionado del IRPF para autónomos (modelo 130).",
        "icon": "💰",
    },
    {
        "month": 3, "day": 15, "end_month": 3, "end_day": 15,
        "title": "Día Mundial de los Derechos del Consumidor",
        "category": "consumo",
        "description": "Buen momento para revisar reclamaciones pendientes de consumo.",
        "icon": "🛒",
    },
]


def _get_relevant_legal_calendar(today: date) -> list[dict]:
    """Devuelve eventos del calendario legal relevantes en los próximos 30 días."""
    events = []
    for event in LEGAL_CALENDAR:
        start = date(today.year, event["month"], event["day"])
        end_month = event.get("end_month", event["month"])
        end_day = event.get("end_day", event["day"])
        end = date(today.year, end_month, end_day)

        # Si el evento ya pasó este año, mirar el año siguiente
        if end < today:
            start = date(today.year + 1, event["month"], event["day"])
            end = date(today.year + 1, end_month, end_day)

        # Mostrar si empieza en los próximos 30 días o si estamos dentro del período
        days_to_start = (start - today).days
        if days_to_start <= 30 or (start <= today <= end):
            events.append({
                "title": event["title"],
                "category": event["category"],
                "description": event["description"],
                "icon": event["icon"],
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "active": start <= today <= end,
                "days_until_start": max(0, days_to_start),
            })
    return events


def get_dashboard_data(user_id: str) -> dict[str, Any]:
    """Agrega todos los datos necesarios para el dashboard del usuario."""
    supabase = get_supabase_client()
    today = date.today()
    three_days = (today + timedelta(days=3)).isoformat()
    seven_days = (today + timedelta(days=7)).isoformat()

    # ── Alertas urgentes (≤3 días) ────────────────────────────────────────────
    urgent_alerts = []
    try:
        result = (
            supabase.table("alerts")
            .select("id, description, deadline_date, law_reference, status")
            .eq("user_id", user_id)
            .eq("status", "active")
            .lte("deadline_date", three_days)
            .gte("deadline_date", today.isoformat())
            .order("deadline_date")
            .limit(10)
            .execute()
        )
        for row in (result.data or []):
            try:
                dd = datetime.strptime(row["deadline_date"][:10], "%Y-%m-%d").date()
                days_remaining = (dd - today).days
            except (ValueError, TypeError):
                days_remaining = 0
            urgent_alerts.append({
                **row,
                "days_remaining": max(0, days_remaining),
                "urgency": "high" if days_remaining <= 1 else "medium",
            })
    except Exception as e:
        logger.error("Dashboard: error fetching urgent alerts: %s", e)

    # ── Próximos plazos (7 días) ──────────────────────────────────────────────
    upcoming_deadlines = []
    try:
        result = (
            supabase.table("alerts")
            .select("id, description, deadline_date, law_reference, status")
            .eq("user_id", user_id)
            .eq("status", "active")
            .gte("deadline_date", today.isoformat())
            .lte("deadline_date", seven_days)
            .order("deadline_date")
            .limit(10)
            .execute()
        )
        for row in (result.data or []):
            try:
                dd = datetime.strptime(row["deadline_date"][:10], "%Y-%m-%d").date()
                days_remaining = (dd - today).days
            except (ValueError, TypeError):
                days_remaining = 0
            upcoming_deadlines.append({
                **row,
                "days_remaining": max(0, days_remaining),
            })
    except Exception as e:
        logger.error("Dashboard: error fetching upcoming deadlines: %s", e)

    # ── Expedientes activos (top 5 abiertos) ──────────────────────────────────
    active_cases = []
    try:
        result = (
            supabase.table("cases")
            .select("id, title, category, status, created_at, updated_at")
            .eq("user_id", user_id)
            .eq("status", "open")
            .order("updated_at", desc=True)
            .limit(5)
            .execute()
        )
        for case in (result.data or []):
            # Contar conversaciones y alertas vinculadas
            conv_count = 0
            alert_count = 0
            try:
                cr = supabase.table("conversations").select("id", count="exact").eq("case_id", case["id"]).execute()
                conv_count = cr.count or 0
            except Exception:
                pass
            try:
                ar = supabase.table("alerts").select("id", count="exact").eq("case_id", case["id"]).eq("status", "active").execute()
                alert_count = ar.count or 0
            except Exception:
                pass
            active_cases.append({
                **case,
                "conversation_count": conv_count,
                "alert_count": alert_count,
            })
    except Exception as e:
        logger.error("Dashboard: error fetching active cases: %s", e)

    # ── Conversaciones recientes (últimas 3) ──────────────────────────────────
    recent_conversations = []
    try:
        result = (
            supabase.table("conversations")
            .select("id, title, category, subcategory, created_at, updated_at")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .limit(3)
            .execute()
        )
        recent_conversations = result.data or []
    except Exception as e:
        logger.error("Dashboard: error fetching recent conversations: %s", e)

    # ── Estadísticas rápidas ──────────────────────────────────────────────────
    stats = {"total_cases": 0, "total_alerts_active": 0, "total_conversations": 0}
    try:
        tc = supabase.table("cases").select("id", count="exact").eq("user_id", user_id).execute()
        stats["total_cases"] = tc.count or 0
    except Exception:
        pass
    try:
        ta = supabase.table("alerts").select("id", count="exact").eq("user_id", user_id).eq("status", "active").execute()
        stats["total_alerts_active"] = ta.count or 0
    except Exception:
        pass
    try:
        tconv = supabase.table("conversations").select("id", count="exact").eq("user_id", user_id).execute()
        stats["total_conversations"] = tconv.count or 0
    except Exception:
        pass

    # ── Calendario legal ──────────────────────────────────────────────────────
    legal_calendar = _get_relevant_legal_calendar(today)

    return {
        "urgent_alerts": urgent_alerts,
        "upcoming_deadlines": upcoming_deadlines,
        "active_cases": active_cases,
        "recent_conversations": recent_conversations,
        "stats": stats,
        "legal_calendar": legal_calendar,
    }
