"""
Endpoints para trámites guiados (wizards).
Permite listar templates, iniciar wizards, enviar pasos y consultar progreso.
"""
import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth import require_auth
from app.services.tramite_wizard_service import (
    get_templates,
    get_template_detail,
    start_wizard,
    get_wizard_status,
    submit_step,
    link_wizard_to_case,
    list_user_wizards,
)

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── Schemas ─────────────────────────────────────────────────────────────────

class StartWizardRequest(BaseModel):
    template_id: str = Field(..., min_length=1, max_length=100)


class SubmitStepRequest(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class LinkCaseRequest(BaseModel):
    case_id: str = Field(..., min_length=1)


# ─── Templates ───────────────────────────────────────────────────────────────

@router.get("/templates")
async def list_templates(user_id: str = Depends(require_auth)):
    """Lista todos los templates de trámites disponibles."""
    return {"success": True, "data": get_templates()}


@router.get("/templates/{template_id}")
async def get_template(template_id: str, user_id: str = Depends(require_auth)):
    """Obtiene un template completo con sus pasos."""
    template = get_template_detail(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template no encontrado")
    return {"success": True, "data": template}


# ─── Wizard lifecycle ────────────────────────────────────────────────────────

@router.post("/start")
async def start_new_wizard(
    body: StartWizardRequest,
    user_id: str = Depends(require_auth),
):
    """Inicia un nuevo trámite guiado."""
    try:
        result = start_wizard(user_id, body.template_id)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my")
async def my_wizards(user_id: str = Depends(require_auth)):
    """Lista los trámites guiados del usuario."""
    return {"success": True, "data": list_user_wizards(user_id)}


@router.get("/{wizard_id}")
async def wizard_status(
    wizard_id: str,
    user_id: str = Depends(require_auth),
):
    """Obtiene el estado actual de un wizard."""
    try:
        result = get_wizard_status(user_id, wizard_id)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{wizard_id}/step/{step_id}")
async def wizard_submit_step(
    wizard_id: str,
    step_id: str,
    body: SubmitStepRequest,
    user_id: str = Depends(require_auth),
):
    """Envía datos de un paso del wizard."""
    try:
        result = submit_step(user_id, wizard_id, step_id, body.data)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{wizard_id}/link-case")
async def wizard_link_case(
    wizard_id: str,
    body: LinkCaseRequest,
    user_id: str = Depends(require_auth),
):
    """Vincula un wizard a un expediente."""
    try:
        result = link_wizard_to_case(user_id, wizard_id, body.case_id)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
