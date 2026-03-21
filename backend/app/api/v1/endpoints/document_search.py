"""
Endpoints para búsqueda avanzada de documentos por entidades legales.
"""

import logging
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.auth import require_auth
from app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)
router = APIRouter()

# Whitelist of allowed entity types (prevents injection and limits surface area)
_ALLOWED_ENTITY_TYPES = frozenset({
    "fecha", "importe", "dni", "nie", "nif", "cif",
    "factura", "referencia", "iban", "plazo", "direccion",
    "nombre", "empresa", "contrato", "matricula",
})

def _validate_entity_type(entity_type: str) -> str:
    """Validates entity_type against whitelist. Returns the value or raises 400."""
    cleaned = entity_type.strip().lower()
    if cleaned not in _ALLOWED_ENTITY_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de entidad no válido. Valores admitidos: {', '.join(sorted(_ALLOWED_ENTITY_TYPES))}",
        )
    return cleaned


class DocumentSearchResult(BaseModel):
    """Resultado de búsqueda de documentos."""
    attachment_id: str
    filename: str
    entity_value: str
    confidence: float
    created_at: str
    entity_type: str


class EntityStatsResult(BaseModel):
    """Estadísticas de entidades por usuario."""
    entity_type: str
    total_count: int
    avg_confidence: float


@router.get("/search/by-entity", response_model=List[DocumentSearchResult])
async def search_documents_by_entity(
    entity_type: str = Query(..., description="Tipo de entidad a buscar (fecha, importe, dni, etc.)"),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0, description="Confianza mínima (0-1)"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de resultados"),
    user_id: str = Depends(require_auth)
):
    """
    Busca documentos que contengan un tipo específico de entidad legal.

    Valores válidos para entity_type: fecha, importe, dni, nie, nif, cif,
    factura, referencia, iban, plazo, direccion, nombre, empresa, contrato, matricula.
    """
    validated_type = _validate_entity_type(entity_type)
    try:
        supabase = get_supabase_client()
        result = supabase.rpc(
            "search_documents_by_entity_type",
            {"p_user_id": user_id, "p_entity_type": validated_type}
        ).limit(limit).execute()

        filtered_results = []
        for row in result.data or []:
            if row.get("confidence", 0) >= min_confidence:
                filtered_results.append(DocumentSearchResult(
                    attachment_id=row["attachment_id"],
                    filename=row["filename"],
                    entity_value=row["entity_value"],
                    confidence=row["confidence"],
                    created_at=row["created_at"],
                    entity_type=validated_type,
                ))

        return filtered_results

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error searching documents by entity type: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error buscando documentos. Inténtalo de nuevo.")


@router.get("/search/entity-stats", response_model=List[EntityStatsResult])
async def get_user_entity_statistics(
    user_id: str = Depends(require_auth)
):
    """
    Obtiene estadísticas de entidades legales extraídas para el usuario actual.
    Útil para entender qué tipos de documentos maneja más frecuentemente.
    """
    try:
        supabase = get_supabase_client()
        
        # Usar la función SQL para obtener estadísticas
        result = supabase.rpc(
            "get_user_entity_stats",
            {"p_user_id": user_id}
        ).execute()
        
        return [
            EntityStatsResult(
                entity_type=row["entity_type"],
                total_count=row["total_count"],
                avg_confidence=row["avg_confidence"]
            )
            for row in result.data or []
        ]
        
    except Exception as e:
        logger.error("Error getting entity stats: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas. Inténtalo de nuevo.")


@router.get("/search/similar-documents")
async def find_similar_documents(
    attachment_id: str = Query(..., description="ID del documento de referencia"),
    similarity_threshold: float = Query(0.7, description="Umbral de similitud (0-1)"),
    limit: int = Query(10, description="Número máximo de resultados"),
    user_id: str = Depends(require_auth)
):
    """
    Encuentra documentos similares basándose en las entidades legales extraídas.
    Útil para encontrar documentos relacionados (ej: facturas del mismo proveedor).
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener entidades del documento de referencia
        reference_doc = supabase.table("conversation_attachments").select(
            "legal_entities, filename"
        ).eq("id", attachment_id).eq("user_id", user_id).execute()
        
        if not reference_doc.data:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        reference_entities = reference_doc.data[0].get("legal_entities", {})
        reference_filename = reference_doc.data[0]["filename"]
        
        if not reference_entities or not reference_entities.get("entities"):
            return {
                "reference_document": reference_filename,
                "similar_documents": [],
                "message": "No se encontraron entidades en el documento de referencia"
            }
        
        # Extraer valores de entidades de referencia para comparación
        reference_values = set()
        for entity in reference_entities.get("entities", []):
            if entity.get("confidence", 0) > 0.6:  # Solo entidades con alta confianza
                reference_values.add(entity.get("value", "").lower().strip())
        
        # Buscar documentos similares
        all_docs = supabase.table("conversation_attachments").select(
            "id, filename, legal_entities, created_at"
        ).eq("user_id", user_id).neq("id", attachment_id).execute()
        
        similar_docs = []
        
        for doc in all_docs.data or []:
            doc_entities = doc.get("legal_entities", {})
            if not doc_entities or not doc_entities.get("entities"):
                continue
            
            # Calcular similitud basada en entidades compartidas
            doc_values = set()
            for entity in doc_entities.get("entities", []):
                if entity.get("confidence", 0) > 0.6:
                    doc_values.add(entity.get("value", "").lower().strip())
            
            # Calcular Jaccard similarity
            if reference_values and doc_values:
                intersection = len(reference_values.intersection(doc_values))
                union = len(reference_values.union(doc_values))
                similarity = intersection / union if union > 0 else 0
                
                if similarity >= similarity_threshold:
                    similar_docs.append({
                        "attachment_id": doc["id"],
                        "filename": doc["filename"],
                        "similarity_score": round(similarity, 3),
                        "shared_entities": list(reference_values.intersection(doc_values)),
                        "created_at": doc["created_at"]
                    })
        
        # Ordenar por similitud descendente
        similar_docs.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return {
            "reference_document": reference_filename,
            "similar_documents": similar_docs[:limit],
            "total_found": len(similar_docs)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error finding similar documents: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error buscando documentos similares. Inténtalo de nuevo.")


@router.get("/search/entity-timeline")
async def get_entity_timeline(
    entity_type: str = Query(..., description="Tipo de entidad (fecha, importe, etc.)"),
    start_date: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    user_id: str = Depends(require_auth)
):
    """
    Obtiene una línea temporal de entidades específicas.
    Útil para ver evolución de importes, fechas de vencimiento, etc.
    """
    validated_type = _validate_entity_type(entity_type)
    try:
        supabase = get_supabase_client()
        
        # Obtener documentos del usuario
        query = supabase.table("conversation_attachments").select(
            "id, filename, legal_entities, created_at"
        ).eq("user_id", user_id)
        
        if start_date:
            query = query.gte("created_at", start_date)
        if end_date:
            query = query.lte("created_at", end_date)
        
        result = query.order("created_at", desc=False).execute()
        
        timeline_data = []
        
        for doc in result.data or []:
            doc_entities = doc.get("legal_entities", {})
            if not doc_entities or not doc_entities.get("entities"):
                continue
            
            # Buscar entidades del tipo solicitado
            matching_entities = []
            for entity in doc_entities.get("entities", []):
                if validated_type in entity.get("type", "").lower():
                    matching_entities.append({
                        "value": entity.get("value"),
                        "confidence": entity.get("confidence"),
                        "context": entity.get("context", "")
                    })
            
            if matching_entities:
                timeline_data.append({
                    "date": doc["created_at"],
                    "document": doc["filename"],
                    "attachment_id": doc["id"],
                    "entities": matching_entities
                })
        
        return {
            "entity_type": validated_type,
            "timeline": timeline_data,
            "total_documents": len(timeline_data),
            "date_range": {
                "start": start_date,
                "end": end_date
            }
        }
        
    except Exception as e:
        logger.error("Error generating entity timeline: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error generando la línea temporal. Inténtalo de nuevo.")