from typing import Literal
from pydantic import BaseModel


class DocumentGenerateRequest(BaseModel):
    case_description: str
    conversation_id: str | None = None
    doc_type: str = "modelo de reclamación"


class DocumentGenerateV2Request(BaseModel):
    """Request para el pipeline de generación (modelos de escritos)."""
    conversation_id: str
    format: Literal["pdf", "docx", "both"] = "both"


class DocumentGenerateV2Response(BaseModel):
    document_id: str
    pdf_url: str | None
    docx_url: str | None
    document_type: str
    generated_at: str


class DocumentDownloadResponse(BaseModel):
    pdf_url: str | None
    docx_url: str | None


class DocumentHistoryItem(BaseModel):
    document_id: str
    conversation_id: str | None
    document_type: str
    created_at: str
    has_pdf: bool
    has_docx: bool


class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
