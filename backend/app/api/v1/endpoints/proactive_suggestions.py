"""
Endpoints para sugerencias proactivas basadas en patrones de usuario.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.auth import require_auth
from app.services.proactive_suggestions_service import (
    proactive_suggestions_service, 
    SuggestionType, 
    SuggestionPriority
)


router = APIRouter()


class SuggestionResponse(BaseModel):
    """Respuesta de sugerencia proactiva."""
    id: str
    type: str
    priority: str
    title: str
    description: str
    action_text: str
    action_data: Dict[str, Any]
    context: Dict[str, Any]
    expires_at: Optional[str] = None
    created_at: str


class SuggestionInteractionRequest(BaseModel):
    """Solicitud de interacción con sugerencia."""
    suggestion_id: str
    action: str  # 'seen', 'acted', 'dismissed'
    action_data: Optional[Dict[str, Any]] = {}


@router.get("/suggestions", response_model=List[SuggestionResponse])
async def get_proactive_suggestions(
    limit: int = Query(10, description="Número máximo de sugerencias"),
    types: Optional[List[str]] = Query(None, description="Filtrar por tipos de sugerencia"),
    priorities: Optional[List[str]] = Query(None, description="Filtrar por prioridades"),
    user_id: str = Depends(require_auth)
):
    """
    Obtiene sugerencias proactivas personalizadas para el usuario actual.
    
    Las sugerencias se generan basándose en:
    - Patrones de conversación del usuario
    - Documentos analizados
    - Alertas y plazos pendientes
    - Comportamiento temporal
    - Historial de éxito en tareas
    """
    try:
        # user_id ya está disponible del parámetro
        
        # Generar sugerencias proactivas
        suggestions = await proactive_suggestions_service.generate_proactive_suggestions(
            user_id=user_id,
            limit=limit
        )
        
        # Filtrar por tipos si se especifican
        if types:
            suggestions = [s for s in suggestions if s.type.value in types]
        
        # Filtrar por prioridades si se especifican
        if priorities:
            suggestions = [s for s in suggestions if s.priority.value in priorities]
        
        # Convertir a formato de respuesta
        response_suggestions = []
        for suggestion in suggestions:
            response_suggestions.append(SuggestionResponse(
                id=suggestion.id,
                type=suggestion.type.value,
                priority=suggestion.priority.value,
                title=suggestion.title,
                description=suggestion.description,
                action_text=suggestion.action_text,
                action_data=suggestion.action_data,
                context=suggestion.context,
                expires_at=suggestion.expires_at.isoformat() if suggestion.expires_at else None,
                created_at=suggestion.created_at.isoformat()
            ))
        
        return response_suggestions
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo sugerencias proactivas: {str(e)}"
        )


@router.post("/suggestions/interact")
async def interact_with_suggestion(
    request: SuggestionInteractionRequest,
    user_id: str = Depends(require_auth)
):
    """
    Registra una interacción del usuario con una sugerencia.
    
    Tipos de interacción:
    - 'seen': El usuario ha visto la sugerencia
    - 'acted': El usuario ha ejecutado la acción sugerida
    - 'dismissed': El usuario ha descartado la sugerencia
    """
    try:
        # user_id ya está disponible del parámetro
        
        if request.action == "seen":
            success = await proactive_suggestions_service.mark_suggestion_as_seen(
                user_id, request.suggestion_id
            )
        elif request.action == "acted":
            success = await proactive_suggestions_service.mark_suggestion_as_acted(
                user_id, request.suggestion_id, request.action_data
            )
        elif request.action == "dismissed":
            # Para dismissed, usamos el mismo método que acted pero con acción diferente
            success = await proactive_suggestions_service.mark_suggestion_as_acted(
                user_id, request.suggestion_id, {"dismissed": True}
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Acción no válida. Debe ser 'seen', 'acted' o 'dismissed'"
            )
        
        if success:
            return {
                "success": True,
                "message": f"Interacción '{request.action}' registrada exitosamente"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Error registrando la interacción"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando interacción: {str(e)}"
        )


@router.get("/suggestions/types")
async def get_suggestion_types():
    """
    Obtiene los tipos de sugerencias disponibles.
    """
    return {
        "suggestion_types": [
            {
                "value": suggestion_type.value,
                "name": suggestion_type.name,
                "description": _get_type_description(suggestion_type)
            }
            for suggestion_type in SuggestionType
        ],
        "priorities": [
            {
                "value": priority.value,
                "name": priority.name,
                "description": _get_priority_description(priority)
            }
            for priority in SuggestionPriority
        ]
    }


@router.get("/suggestions/stats")
async def get_user_suggestion_stats(
    user_id: str = Depends(require_auth)
):
    """
    Obtiene estadísticas de interacción del usuario con sugerencias.
    """
    try:
        from app.core.supabase_client import get_supabase_client
        
        # user_id ya está disponible del parámetro
        supabase = get_supabase_client()
        
        # Usar la función SQL para obtener estadísticas
        result = supabase.rpc(
            "get_user_suggestion_stats",
            {"p_user_id": user_id}
        ).execute()
        
        if result.data:
            stats = result.data[0]
            return {
                "total_suggestions_seen": stats["total_suggestions_seen"],
                "total_suggestions_acted": stats["total_suggestions_acted"],
                "total_suggestions_dismissed": stats["total_suggestions_dismissed"],
                "engagement_rate": stats["engagement_rate"],
                "engagement_level": _calculate_engagement_level(stats["engagement_rate"])
            }
        else:
            return {
                "total_suggestions_seen": 0,
                "total_suggestions_acted": 0,
                "total_suggestions_dismissed": 0,
                "engagement_rate": 0.0,
                "engagement_level": "new_user"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )


@router.post("/suggestions/contextual")
async def get_contextual_suggestions(
    conversation_context: str,
    attachment_ids: Optional[List[str]] = [],
    user_id: str = Depends(require_auth)
):
    """
    Obtiene sugerencias específicas para un contexto dado.
    Útil para mostrar sugerencias relevantes durante una conversación.
    """
    try:
        # user_id ya está disponible del parámetro
        
        # Crear contexto específico
        context = {
            "conversation_context": conversation_context,
            "attachment_ids": attachment_ids or []
        }
        
        # Generar sugerencias contextuales
        suggestions = await proactive_suggestions_service.generate_proactive_suggestions(
            user_id=user_id,
            context=context,
            limit=5  # Limitar para sugerencias contextuales
        )
        
        # Filtrar solo sugerencias altamente relevantes para el contexto
        contextual_suggestions = [
            s for s in suggestions 
            if s.priority in [SuggestionPriority.CRITICAL, SuggestionPriority.HIGH]
        ]
        
        # Convertir a formato de respuesta
        response_suggestions = []
        for suggestion in contextual_suggestions:
            response_suggestions.append(SuggestionResponse(
                id=suggestion.id,
                type=suggestion.type.value,
                priority=suggestion.priority.value,
                title=suggestion.title,
                description=suggestion.description,
                action_text=suggestion.action_text,
                action_data=suggestion.action_data,
                context=suggestion.context,
                expires_at=suggestion.expires_at.isoformat() if suggestion.expires_at else None,
                created_at=suggestion.created_at.isoformat()
            ))
        
        return {
            "suggestions": response_suggestions,
            "context_analyzed": True,
            "total_contextual_suggestions": len(response_suggestions)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo sugerencias contextuales: {str(e)}"
        )


def _get_type_description(suggestion_type: SuggestionType) -> str:
    """Obtiene descripción de un tipo de sugerencia."""
    descriptions = {
        SuggestionType.DOCUMENT_TEMPLATE: "Sugerencias para generar documentos legales",
        SuggestionType.LEGAL_DEADLINE: "Recordatorios de plazos legales importantes",
        SuggestionType.FOLLOW_UP_ACTION: "Acciones de seguimiento recomendadas",
        SuggestionType.DOCUMENT_ANALYSIS: "Análisis adicional de documentos",
        SuggestionType.RELATED_PROCEDURE: "Procedimientos relacionados que podrían interesarte",
        SuggestionType.PREVENTIVE_ACTION: "Acciones preventivas para evitar problemas",
        SuggestionType.OPTIMIZATION_TIP: "Consejos para optimizar tu gestión",
        SuggestionType.REGULATORY_UPDATE: "Actualizaciones normativas relevantes"
    }
    return descriptions.get(suggestion_type, "Sugerencia personalizada")


def _get_priority_description(priority: SuggestionPriority) -> str:
    """Obtiene descripción de una prioridad."""
    descriptions = {
        SuggestionPriority.CRITICAL: "Requiere atención inmediata",
        SuggestionPriority.HIGH: "Alta importancia",
        SuggestionPriority.MEDIUM: "Importancia moderada",
        SuggestionPriority.LOW: "Baja prioridad",
        SuggestionPriority.INFO: "Información útil"
    }
    return descriptions.get(priority, "Prioridad estándar")


def _calculate_engagement_level(engagement_rate: float) -> str:
    """Calcula el nivel de engagement del usuario."""
    if engagement_rate >= 0.8:
        return "very_high"
    elif engagement_rate >= 0.6:
        return "high"
    elif engagement_rate >= 0.4:
        return "medium"
    elif engagement_rate >= 0.2:
        return "low"
    else:
        return "very_low"