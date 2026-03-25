"""
Endpoint del dashboard: agrega datos para la vista principal del usuario.
"""
from fastapi import APIRouter, Depends

from app.core.auth import require_auth
from app.services.dashboard_service import get_dashboard_data
from app.services.smart_reminders_service import get_smart_reminders
from app.services.recommendations_service import get_personalized_recommendations

router = APIRouter()


@router.get("")
async def dashboard(user_id: str = Depends(require_auth)):
    """Retorna datos agregados para el dashboard del usuario."""
    data = get_dashboard_data(user_id)
    data["reminders"] = get_smart_reminders(user_id)
    data["recommendations"] = get_personalized_recommendations(user_id)
    return {"success": True, "data": data}


@router.get("/reminders")
async def reminders(user_id: str = Depends(require_auth)):
    """Retorna recordatorios inteligentes para el usuario."""
    return {"success": True, "data": get_smart_reminders(user_id)}
