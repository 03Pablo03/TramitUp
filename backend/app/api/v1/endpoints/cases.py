"""
Endpoints para gestión de expedientes de caso.
Todos los endpoints requieren autenticación y verifican propiedad del recurso.
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth import require_auth
from app.core.supabase_client import get_supabase_client
from app.services.case_service import (
    create_case,
    list_cases,
    get_case,
    update_case,
    delete_case,
    link_conversation,
    unlink_conversation,
    update_step_status,
    update_document_check,
    create_case_from_conversation,
    VALID_CATEGORIES,
    VALID_STATUSES,
)

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── Schemas ──────────────────────────────────────────────────────────────────

class CreateCaseRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    category: Optional[str] = Field(None)
    subcategory: Optional[str] = Field(None, max_length=50)
    summary: Optional[str] = Field(None, max_length=1000)


class UpdateCaseRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    status: Optional[str] = Field(None)
    summary: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None)


class CreateFromConversationRequest(BaseModel):
    conversation_id: str
    title: str = Field(..., min_length=1, max_length=120)
    category: Optional[str] = Field(None)
    subcategory: Optional[str] = Field(None, max_length=50)


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

# NOTE: /from-conversation must be registered BEFORE /{case_id} to avoid
# FastAPI routing /{case_id} capturing the literal "from-conversation" string.
@router.post("/from-conversation")
def api_create_from_conversation(
    request: CreateFromConversationRequest,
    user_id: str = Depends(require_auth),
):
    """Crea un expediente desde una conversación, auto-vinculando y aplicando workflow."""
    _validate_category(request.category)
    try:
        case = create_case_from_conversation(
            user_id=user_id,
            conversation_id=request.conversation_id,
            title=request.title.strip(),
            category=request.category,
            subcategory=request.subcategory,
        )
    except Exception as e:
        logger.error("Error creating case from conversation: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error creando el expediente.")

    if not case:
        raise HTTPException(status_code=404, detail="Conversación no encontrada.")
    return case


@router.post("")
def api_create_case(
    request: CreateCaseRequest,
    user_id: str = Depends(require_auth),
):
    """Crea un nuevo expediente."""
    _validate_category(request.category)

    try:
        case = create_case(
            user_id=user_id,
            title=request.title.strip(),
            category=request.category,
            summary=request.summary,
            subcategory=request.subcategory,
        )
    except Exception as e:
        logger.error("Error creating case for user %s: %s", user_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error creando el expediente. Inténtalo de nuevo.")

    return case


@router.get("")
def api_list_cases(user_id: str = Depends(require_auth)):
    """Lista todos los expedientes del usuario."""
    try:
        return {"cases": list_cases(user_id)}
    except Exception as e:
        logger.error("Error listing cases for user %s: %s", user_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los expedientes.")


@router.get("/{case_id}")
def api_get_case(case_id: str, user_id: str = Depends(require_auth)):
    """Devuelve el detalle de un expediente."""
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
    """Actualiza un expediente."""
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
    """Elimina un expediente."""
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
    """Vincula una conversación al expediente."""
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


# ─── Workflow endpoints ──────────────────────────────────────────────────────


class UpdateStepRequest(BaseModel):
    status: str = Field(..., description="pending | in_progress | completed | skipped")


class UpdateDocCheckRequest(BaseModel):
    checked: bool


class CreateFromConversationRequest(BaseModel):
    conversation_id: str
    title: str = Field(..., min_length=1, max_length=120)
    category: Optional[str] = None
    subcategory: Optional[str] = None


@router.patch("/{case_id}/steps/{step_index}")
def api_update_step(
    case_id: str,
    step_index: int,
    request: UpdateStepRequest,
    user_id: str = Depends(require_auth),
):
    """Actualiza el estado de un paso del workflow."""
    try:
        result = update_step_status(user_id, case_id, step_index, request.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error updating step %d for case %s: %s", step_index, case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error actualizando el paso.")

    if result is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return result


@router.get("/{case_id}/generated-documents")
def api_get_case_generated_documents(
    case_id: str,
    user_id: str = Depends(require_auth),
):
    """Devuelve los documentos generados (modelos de escritos) vinculados a las conversaciones del expediente."""
    try:
        supabase = get_supabase_client()
        # Verificar que el expediente pertenece al usuario
        case = get_case(user_id, case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Expediente no encontrado.")

        # Obtener IDs de conversaciones vinculadas al expediente
        conv_links = supabase.table("case_conversations").select("conversation_id").eq(
            "case_id", case_id
        ).execute()
        conversation_ids = [row["conversation_id"] for row in (conv_links.data or [])]

        if not conversation_ids:
            return {"documents": []}

        # Obtener documentos generados de esas conversaciones
        docs_result = supabase.table("generated_documents").select(
            "id, conversation_id, document_type, pdf_path, docx_path, created_at"
        ).eq("user_id", user_id).in_("conversation_id", conversation_ids).order(
            "created_at", desc=True
        ).execute()

        def _to_item(d: dict) -> dict:
            ca = d.get("created_at")
            return {
                "document_id": d["id"],
                "conversation_id": d.get("conversation_id"),
                "document_type": d.get("document_type", "Modelo de escrito"),
                "created_at": ca.isoformat() if hasattr(ca, "isoformat") else str(ca) if ca else "",
                "has_pdf": bool(d.get("pdf_path")),
                "has_docx": bool(d.get("docx_path")),
            }

        return {"documents": [_to_item(d) for d in (docs_result.data or [])]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error fetching generated docs for case %s: %s", case_id, e, exc_info=True)
        return {"documents": []}


@router.patch("/{case_id}/documents/{doc_index}")
def api_update_doc_check(
    case_id: str,
    doc_index: int,
    request: UpdateDocCheckRequest,
    user_id: str = Depends(require_auth),
):
    """Marca o desmarca un documento de la checklist."""
    try:
        result = update_document_check(user_id, case_id, doc_index, request.checked)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error updating doc %d for case %s: %s", doc_index, case_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error actualizando el documento.")

    if result is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return {"ok": True}
