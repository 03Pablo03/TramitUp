"""
User profile and activity endpoints.
"""
import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.core.supabase_client import get_supabase_client
from app.services.subscription_service import get_user_subscription

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stats")
async def get_user_stats(user_id: str = Depends(require_auth)):
    """
    Get user activity statistics for dashboard.
    Includes: conversations this month, active cases, upcoming alerts, legal calendar.
    """
    supabase = get_supabase_client()
    now = datetime.utcnow()
    month_ago = now - timedelta(days=30)

    try:
        # 1. Conversaciones este mes
        conv_result = supabase.table("conversations").select("id").eq(
            "user_id", user_id
        ).gte("created_at", month_ago.isoformat()).execute()
        
        conversations_this_month = len(conv_result.data or [])

        # 2. Últimas 3 conversaciones
        recent_conv_result = supabase.table("conversations").select(
            "id, title, created_at"
        ).eq("user_id", user_id).order("created_at", desc=True).limit(3).execute()
        
        recent_conversations = [
            {
                "id": c["id"],
                "title": c["title"],
                "updated_at": c["created_at"],
            }
            for c in (recent_conv_result.data or [])
        ]

        # 3. Expedientes activos
        cases_result = supabase.table("cases").select(
            "id, title, status, category"
        ).eq("user_id", user_id).eq("status", "active").execute()
        
        active_cases = cases_result.data or []
        active_cases_count = len(active_cases)

        # 4. Alertas próximas (próximos 7 días)
        alerts_result = supabase.table("alerts").select(
            "id, description, deadline_date, status"
        ).eq("user_id", user_id).eq(
            "status", "pending"
        ).gte(
            "deadline_date", (now - timedelta(days=1)).isoformat()
        ).lte(
            "deadline_date", (now + timedelta(days=7)).isoformat()
        ).order("deadline_date", desc=False).limit(5).execute()
        
        upcoming_alerts = []
        for alert in (alerts_result.data or []):
            try:
                deadline = datetime.fromisoformat(alert["deadline_date"].replace("Z", "+00:00"))
                days_until = max(0, (deadline.date() - now.date()).days)
                upcoming_alerts.append({
                    "id": alert["id"],
                    "description": alert["description"],
                    "deadline_date": alert["deadline_date"],
                    "days_remaining": days_until,
                })
            except Exception:
                pass

        # 5. Calendario legal (eventos próximos)
        # Hardcoded para ahora - en futuro, consultar tabla de eventos
        today = now.date()
        legal_events = []
        
        # Ejemplos de eventos legales relevantes en España
        events_data = [
            {
                "title": "Campaña de la Renta (Inicio)",
                "start_date": datetime(now.year, 4, 1).date(),
                "description": "Inicio de la campaña de declaración de impuestos",
            },
            {
                "title": "Campaña de la Renta (Fin)",
                "start_date": datetime(now.year, 6, 30).date(),
                "description": "Final del plazo para presentar la Renta 2023",
            },
            {
                "title": "Plazo renovación ITV",
                "start_date": datetime(now.year, 6, 1).date(),
                "description": "Plazo típico para renovar ITV (verificar según tu vehículo)",
            },
        ]
        
        for event in events_data:
            event_date = event["start_date"]
            if event_date >= today - timedelta(days=1):
                days_until = (event_date - today).days
                if days_until <= 90:  # Mostrar eventos próximos 3 meses
                    legal_events.append({
                        "title": event["title"],
                        "description": event["description"],
                        "start_date": event_date.isoformat(),
                        "active": days_until <= 0,
                        "days_until_start": max(0, days_until),
                    })

        return {
            "conversations_this_month": conversations_this_month,
            "active_cases": {
                "count": active_cases_count,
                "cases": [
                    {
                        "id": c["id"],
                        "title": c["title"],
                        "status": c["status"],
                        "category": c.get("category"),
                    }
                    for c in active_cases[:5]
                ],
            },
            "recent_conversations": recent_conversations,
            "upcoming_alerts": upcoming_alerts,
            "legal_calendar": legal_events,
        }

    except Exception as e:
        logger.error("Error getting user stats: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas")
