from fastapi import APIRouter, Depends

from app.ai.chains.classify_chain import classify_tramite
from app.core.auth import require_auth
from app.schemas.chat import ClassifyRequest, ClassifyResponse

router = APIRouter()


@router.post("", response_model=ClassifyResponse)
def classify(request: ClassifyRequest, user_id: str = Depends(require_auth)):
    """Clasifica un texto libre en categoría, subcategoría, urgencia y keywords."""
    result = classify_tramite(request.message)
    return ClassifyResponse(**result)
