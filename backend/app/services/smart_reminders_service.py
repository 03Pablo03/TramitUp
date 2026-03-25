"""
Servicio de recordatorios inteligentes.
Genera recordatorios proactivos basados en:
- Alertas próximas a vencer
- Contratos de alquiler que se renuevan
- Reclamaciones pendientes de respuesta
- Eventos del calendario legal
"""
import logging
from datetime import date, timedelta
from typing import Any, Dict, List

from app.core.supabase_client import get_supabase_client
from app.config.legal_calendar import get_upcoming_legal_events

logger = logging.getLogger(__name__)


def get_smart_reminders(user_id: str) -> List[Dict[str, Any]]:
    """
    Genera recordatorios inteligentes para el usuario.
    Combina alertas urgentes, wizards pendientes y eventos legales.
    """
    reminders = []

    # 1. Alertas próximas (≤3 días)
    reminders.extend(_get_urgent_alert_reminders(user_id))

    # 2. Wizards en progreso abandonados
    reminders.extend(_get_abandoned_wizard_reminders(user_id))

    # 3. Eventos del calendario legal relevantes
    reminders.extend(_get_legal_calendar_reminders(user_id))

    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    reminders.sort(key=lambda r: priority_order.get(r.get("priority", "low"), 3))

    return reminders[:10]  # Max 10 reminders


def _get_urgent_alert_reminders(user_id: str) -> List[Dict[str, Any]]:
    """Alertas que vencen en ≤3 días."""
    supabase = get_supabase_client()
    today = date.today()
    threshold = (today + timedelta(days=3)).isoformat()

    try:
        result = (
            supabase.table("alerts")
            .select("id, description, deadline_date, law_reference")
            .eq("user_id", user_id)
            .eq("status", "active")
            .lte("deadline_date", threshold)
            .gte("deadline_date", today.isoformat())
            .order("deadline_date")
            .limit(5)
            .execute()
        )

        reminders = []
        for alert in result.data or []:
            deadline = date.fromisoformat(alert["deadline_date"])
            days_left = (deadline - today).days
            reminders.append({
                "type": "urgent_alert",
                "priority": "critical" if days_left <= 1 else "high",
                "title": f"⏰ Plazo en {days_left} día{'s' if days_left != 1 else ''}",
                "description": alert["description"],
                "action_url": "/alerts",
                "action_label": "Ver alertas",
                "metadata": {"alert_id": alert["id"], "days_left": days_left},
            })
        return reminders
    except Exception as e:
        logger.warning("Error fetching urgent alerts: %s", e)
        return []


def _get_abandoned_wizard_reminders(user_id: str) -> List[Dict[str, Any]]:
    """Wizards iniciados pero no completados en los últimos 7 días."""
    supabase = get_supabase_client()
    threshold = (date.today() - timedelta(days=7)).isoformat()

    try:
        result = (
            supabase.table("tramite_wizards")
            .select("id, template_id, current_step, updated_at")
            .eq("user_id", user_id)
            .eq("status", "in_progress")
            .gte("created_at", threshold)
            .order("updated_at", desc=True)
            .limit(3)
            .execute()
        )

        reminders = []
        for wizard in result.data or []:
            from app.config.tramite_templates import get_tramite_template
            template = get_tramite_template(wizard["template_id"])
            title = template["title"] if template else wizard["template_id"]

            reminders.append({
                "type": "abandoned_wizard",
                "priority": "medium",
                "title": f"📋 Trámite pendiente: {title}",
                "description": "Tienes un trámite guiado sin terminar. Continúa donde lo dejaste.",
                "action_url": f"/wizard/{wizard['template_id']}",
                "action_label": "Continuar trámite",
                "metadata": {"wizard_id": wizard["id"], "template_id": wizard["template_id"]},
            })
        return reminders
    except Exception as e:
        logger.warning("Error fetching abandoned wizards: %s", e)
        return []


def _get_legal_calendar_reminders(user_id: str) -> List[Dict[str, Any]]:
    """Eventos del calendario legal en los próximos 14 días."""
    try:
        # Get user's interest categories from profile
        supabase = get_supabase_client()
        profile = (
            supabase.table("profiles")
            .select("categories_interest")
            .eq("id", user_id)
            .single()
            .execute()
        )
        user_categories = (profile.data or {}).get("categories_interest") or []

        events = get_upcoming_legal_events(days_ahead=14, categories=user_categories if user_categories else None)

        reminders = []
        for event in events[:3]:
            days = event["days_until"]
            reminders.append({
                "type": "legal_calendar",
                "priority": "medium" if days <= 3 else "low",
                "title": f"📅 {event['title']}",
                "description": event["description"],
                "action_url": "/dashboard",
                "action_label": "Ver calendario",
                "metadata": {"event_date": event["date"], "days_until": days},
            })
        return reminders
    except Exception as e:
        logger.warning("Error fetching legal calendar reminders: %s", e)
        return []
