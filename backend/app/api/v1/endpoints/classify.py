from fastapi import APIRouter

from app.ai.chains.classify_chain import classify_tramite
from app.schemas.chat import ClassifyRequest, ClassifyResponse

router = APIRouter()


@router.post("", response_model=ClassifyResponse)
def classify(request: ClassifyRequest):
    """Clasifica un texto libre en categoría, subcategoría, urgencia y keywords."""
    result = classify_tramite(request.message)
    return ClassifyResponse(**result)
