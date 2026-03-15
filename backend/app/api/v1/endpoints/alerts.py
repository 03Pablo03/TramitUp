from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import require_auth
from app.services.subscription_service import get_user_plan
from app.services.alerts_service import (
    create_alert,
    list_alerts,
    update_alert,
    delete_alert,
    compute_deadline_from_detected,
)
from app.schemas.alerts import (
    CreateAlertRequest,
    CreateAlertResponse,
    UpdateAlertRequest,
)

router = APIRouter()


def _require_pro(user_id: str) -> None:
    plan = get_user_plan(user_id)
    if plan not in ("pro", "document"):
        raise HTTPException(
            status_code=403,
            detail="Las alertas son exclusivas del plan PRO",
        )


@router.post("/create", response_model=CreateAlertResponse)
def api_create_alert(
    request: CreateAlertRequest,
    user_id: str = Depends(require_auth),
):
    """Crea una alerta de plazo. Solo PRO."""
    _require_pro(user_id)
    from datetime import datetime
    try:
        dd = datetime.strptime(request.deadline_date[:10], "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Fecha límite inválida")
    try:
        result = create_alert(
            user_id=user_id,
            conversation_id=request.conversation_id,
            description=request.description,
            deadline_date=dd,
            law_reference=request.law_reference,
            notify_days_before=request.notify_days_before,
            manual_priority=request.manual_priority,
        )
        return CreateAlertResponse(
            alert_id=result["id"],
            deadline_date=result["deadline_date"],
            notifications_scheduled=result.get("notifications_scheduled", []),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def api_list_alerts(
    user_id: str = Depends(require_auth),
    status: str | None = Query(None, description="active | expired | dismissed"),
):
    """Lista alertas del usuario. Solo PRO."""
    _require_pro(user_id)
    items = list_alerts(user_id, status_filter=status)
    return items


@router.patch("/{alert_id}")
def api_update_alert(
    alert_id: str,
    request: UpdateAlertRequest,
    user_id: str = Depends(require_auth),
):
    """Actualiza o descarta una alerta."""
    _require_pro(user_id)
    from datetime import datetime
    dd = None
    if request.deadline_date:
        try:
            dd = datetime.strptime(request.deadline_date[:10], "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Fecha inválida")
    try:
        update_alert(alert_id, user_id, status=request.status, deadline_date=dd)
        return {"ok": True}
    except ValueError:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")


@router.delete("/{alert_id}")
def api_delete_alert(
    alert_id: str,
    user_id: str = Depends(require_auth),
):
    """Elimina una alerta."""
    _require_pro(user_id)
    try:
        delete_alert(alert_id, user_id)
        return {"ok": True}
    except ValueError:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
