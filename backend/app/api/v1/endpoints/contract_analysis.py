"""
Endpoint para análisis de cláusulas contractuales.
POST /contract-analysis  — recibe un archivo, devuelve JSON con cláusulas problemáticas.
"""
import logging
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.auth import require_auth
from app.services.contract_analysis_service import analyze_contract

logger = logging.getLogger(__name__)

router = APIRouter()

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/jpg",
    "image/png",
}

MAX_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("")
async def contract_analysis(
    file: UploadFile = File(...),
    _user_id: str = Depends(require_auth),
):
    """
    Analiza un contrato (PDF/DOCX/imagen) e identifica cláusulas problemáticas según derecho español.
    Requiere autenticación.
    """
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo de archivo no soportado: {content_type}. Usa PDF, DOCX o imagen.",
        )

    file_content = await file.read()
    if len(file_content) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="El archivo supera el tamaño máximo permitido (10 MB).",
        )

    try:
        result = await analyze_contract(
            file_content=file_content,
            content_type=content_type,
            filename=file.filename or "contrato",
        )
    except Exception as e:
        logger.error("Contract analysis error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error analizando el contrato. Inténtalo de nuevo.")

    return result
