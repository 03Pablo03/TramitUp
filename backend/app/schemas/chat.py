from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    attachment_ids: List[str] = []


class CompensationEstimate(BaseModel):
    """Esquema para estimaciones de compensación."""
    amount_eur: Optional[int] = None
    applies: bool = False
    reason: str = ""


class ClassifyRequest(BaseModel):
    message: str


class ClassifyResponse(BaseModel):
    category: str
    subcategory: str
    urgency: str
    keywords: list[str] = []
    needs_more_info: bool = False
    titulo_resumen: str = ""

