"""
Endpoints para gestión de expedientes de caso.
Todos los endpoints requieren autenticación y verifican propiedad del recurso.
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth import require_auth
from app.services.case_service import (
    create_case,
    count_open_cases,
    list_cases,
    get_case,
    update_case,
    delete_case,
    link_conversation,
    unlink_conversation,
    VALID_CATEGORIES,
    VALID_STATUSES,
)
from app.services.subscription_service import get_user_plan

logger = logging.getLogger(__name__)
router = APIRouter()

FREE_OPEN_CASE_LIMIT = 1


# ─── Schemas ──────────────────────────────────────────────────────────────────

class CreateCaseRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    category: Optional[str] = Field(None)
    summary: Optional[str] = Field(None, max_length=1000)


class UpdateCaseRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    status: Optional[str] = Field(None)
    summary: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _validate_category(category: Optional[str]) -> Optional[str]:
    if category is None:
        return None
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Categoría no válida. Valores admitidos: {', '.join(sorted(VALID_CATEGORIES))}",
        )
    return category


def _validate_status(status: Optional[str]) -> Optional[str]:
    if status is None:
        return None
    if status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Estado no válido. Valores admitidos: {', '.join(sorted(VALID_STATUSES))}",
        )
    return status


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("")
def api_create_case(
    request: CreateCaseRequest,
    user_id: str = Depends(require_auth),
):
    """
    Crea un nuevo expediente de caso.
    Plan gratuito: máximo 1 caso abierto simultáneo.
    Plan PRO: sin límite.
    """
    _validate_category(request.category)

    plan = get_user_plan(user_id)
    if plan == "free":
        open_count = count_open_cases(user_id)
        if open_count >= FREE_OPEN_CASE_LIMIT:
            raise HTTPException(
                status_code=403,
                detail=(
                    "El plan gratuito permite 1 caso activo a la vez. "
                    "Archiva o elimina el actual para crear uno nuevo, "
                    "o actualiza a PRO para casos ilimitados."
                ),
            )

    try:
        case = create_case(
            user_id=user_id,
            title=request.title.strip(),
            category=request.category,
            summary=request.summary,
        )
    except Exception as e:
        logger.error("Error creating case for user %s: %s", user_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error creando el expediente. Inténtalo de nuevo.")

    return case


@router.get("")
def api_list_cases(user_id: str = Depends(require_auth)):
    """Lista todos los expedientes del usuario con contadores."""
    try:
        return {"cases": list_cases(user_id)}
    except Exception as e:
        logger.error("Error listing cases for user %s: %s", user_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los expedientes.")


@router.get("/{case_id}")
def api_get_case(case_id: str, user_id: str = Depends(require_auth)):
    """Devuelve el detalle de un expediente con conversaciones y alertas vinculadas."""
    try:
        case = get_case(user_id, case_id)
    except Exception as e:
        logger.error("Error fetching case %s: %s", case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando el expediente.")

    if not case:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return case


@router.patch("/{case_id}")
def api_update_case(
    case_id: str,
    request: UpdateCaseRequest,
    user_id: str = Depends(require_auth),
):
    """Actualiza título, estado, resumen o categoría de un expediente."""
    _validate_category(request.category)
    _validate_status(request.status)

    try:
        ok = update_case(user_id, case_id, request.model_dump(exclude_none=True))
    except Exception as e:
        logger.error("Error updating case %s: %s", case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error actualizando el expediente.")

    if not ok:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return {"ok": True}


@router.delete("/{case_id}")
def api_delete_case(case_id: str, user_id: str = Depends(require_auth)):
    """Elimina un expediente y desvincula sus conversaciones y alertas."""
    try:
        ok = delete_case(user_id, case_id)
    except Exception as e:
        logger.error("Error deleting case %s: %s", case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error eliminando el expediente.")

    if not ok:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return {"ok": True}


@router.post("/{case_id}/conversations/{conversation_id}")
def api_link_conversation(
    case_id: str,
    conversation_id: str,
    user_id: str = Depends(require_auth),
):
    """Vincula una conversación al expediente. Ambos deben pertenecer al usuario."""
    try:
        ok = link_conversation(user_id, case_id, conversation_id)
    except Exception as e:
        logger.error("Error linking conversation %s to case %s: %s", conversation_id, case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error vinculando la conversación.")

    if not ok:
        raise HTTPException(status_code=404, detail="Expediente o conversación no encontrada.")
    return {"ok": True}


@router.delete("/{case_id}/conversations/{conversation_id}")
def api_unlink_conversation(
    case_id: str,
    conversation_id: str,
    user_id: str = Depends(require_auth),
):
    """Desvincula una conversación del expediente."""
    try:
        ok = unlink_conversation(user_id, case_id, conversation_id)
    except Exception as e:
        logger.error("Error unlinking conversation %s from case %s: %s", conversation_id, case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error desvinculando la conversación.")

    if not ok:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return {"ok": True}
