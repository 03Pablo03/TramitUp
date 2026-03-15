from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.services.subscription_service import get_user_plan, has_document_access
from app.services.document_pipeline_service import (
    run_document_pipeline,
    get_document_download_urls,
    get_document_history,
)
from app.schemas.document import (
    DocumentGenerateV2Request,
    DocumentGenerateV2Response,
    DocumentDownloadResponse,
    DocumentHistoryItem,
)

router = APIRouter()


@router.post("/generate", response_model=DocumentGenerateV2Response)
def api_generate_document(
    request: DocumentGenerateV2Request,
    user_id: str = Depends(require_auth),
):
    """
    Genera un modelo de escrito personalizado a partir de la conversación.
    Requiere plan PRO o document_unlock para la conversación.
    """
    if not has_document_access(user_id, request.conversation_id):
        raise HTTPException(
            status_code=403,
            detail="Necesitas plan PRO o desbloquear el documento para generar modelos de escritos",
        )
    try:
        result = run_document_pipeline(
            user_id=user_id,
            conversation_id=request.conversation_id,
            format_request=request.format,
        )
        return DocumentGenerateV2Response(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", response_model=list[DocumentHistoryItem])
def api_document_history(user_id: str = Depends(require_auth)):
    """Lista todos los modelos de escritos generados por el usuario. Solo PRO."""
    if not has_document_access(user_id, None):
        raise HTTPException(
            status_code=403,
            detail="Los modelos de escritos son exclusivos del plan PRO",
        )
    items = get_document_history(user_id)
    return [DocumentHistoryItem(**d) for d in items]


@router.get("/{document_id}/download", response_model=DocumentDownloadResponse)
def api_document_download(
    document_id: str,
    user_id: str = Depends(require_auth),
):
    """Obtiene URLs firmadas frescas para descargar el documento. Solo PRO."""
    if not has_document_access(user_id, None):
        raise HTTPException(
            status_code=403,
            detail="Los modelos de escritos son exclusivos del plan PRO",
        )
    try:
        urls = get_document_download_urls(document_id, user_id)
        return DocumentDownloadResponse(**urls)
    except ValueError:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
