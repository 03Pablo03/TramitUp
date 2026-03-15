"""
Endpoints para plantillas inteligentes con generación condicional.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.auth import require_auth
from app.services.intelligent_template_service import intelligent_template_service
from app.services.personalization_service import personalization_service
from app.services.document_analysis_service import document_analysis_service


router = APIRouter()


class TemplateGenerationRequest(BaseModel):
    """Solicitud de generación de documento con plantilla inteligente."""
    template_id: str
    conversation_context: str
    attachment_ids: Optional[List[str]] = []
    custom_fields: Optional[Dict[str, Any]] = {}


class TemplatePreviewRequest(BaseModel):
    """Solicitud de vista previa de plantilla."""
    template_id: str
    sample_fields: Dict[str, Any]


@router.get("/templates", response_model=List[Dict[str, Any]])
async def get_available_templates(
    user_id: str = Depends(require_auth)
):
    """
    Obtiene lista de plantillas inteligentes disponibles.
    """
    try:
        templates = intelligent_template_service.get_available_templates()
        return templates
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo plantillas: {str(e)}"
        )


@router.post("/templates/preview")
async def preview_template(
    request: TemplatePreviewRequest,
    user_id: str = Depends(require_auth)
):
    """
    Genera vista previa de una plantilla con campos de ejemplo.
    """
    try:
        preview = intelligent_template_service.get_template_preview(
            request.template_id,
            request.sample_fields
        )
        return preview
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando vista previa: {str(e)}"
        )


@router.post("/templates/generate")
async def generate_intelligent_document(
    request: TemplateGenerationRequest,
    user_id: str = Depends(require_auth)
):
    """
    Genera un documento usando plantillas inteligentes con análisis contextual.
    
    El sistema:
    1. Analiza el contexto de la conversación
    2. Extrae entidades de documentos adjuntos
    3. Aplica personalización del usuario
    4. Evalúa condiciones de la plantilla
    5. Genera documento adaptativo
    """
    try:
        # user_id ya está disponible del parámetro
        
        # 1. Obtener contexto de personalización del usuario
        user_context = personalization_service.get_user_context(user_id)
        
        # 2. Extraer entidades de documentos adjuntos
        extracted_entities = {"entities": [], "specific_data": {}}
        
        if request.attachment_ids:
            # Combinar entidades de todos los documentos adjuntos
            all_entities = []
            all_specific_data = {}
            
            for attachment_id in request.attachment_ids:
                attachment_info = document_analysis_service.get_attachment_info(
                    attachment_id, user_id
                )
                
                if attachment_info and attachment_info.get("legal_entities"):
                    legal_entities = attachment_info["legal_entities"]
                    
                    # Añadir entidades
                    entities = legal_entities.get("entities", [])
                    all_entities.extend(entities)
                    
                    # Combinar datos específicos
                    specific_data = legal_entities.get("specific_data", {})
                    all_specific_data.update(specific_data)
            
            extracted_entities = {
                "entities": all_entities,
                "specific_data": all_specific_data
            }
        
        # 3. Añadir campos personalizados
        if request.custom_fields:
            extracted_entities["specific_data"].update(request.custom_fields)
        
        # 4. Generar documento adaptativo
        result = intelligent_template_service.generate_adaptive_document(
            template_id=request.template_id,
            user_context=user_context,
            extracted_entities=extracted_entities,
            conversation_context=request.conversation_context,
            user_id=user_id
        )
        
        return {
            "success": True,
            "document_path": result["document_path"],
            "template_used": result["template_used"],
            "sections_included": result["sections_included"],
            "fields_populated": result["fields_populated"],
            "ai_enhanced": result["ai_enhanced"],
            "generation_metadata": result["generation_metadata"],
            "message": f"Documento generado exitosamente usando {result['template_used']}"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando documento inteligente: {str(e)}"
        )


@router.post("/templates/analyze-context")
async def analyze_context_for_template(
    conversation_context: str,
    attachment_ids: Optional[List[str]] = [],
    user_id: str = Depends(require_auth)
):
    """
    Analiza el contexto y sugiere la mejor plantilla y campos.
    """
    try:
        # user_id ya está disponible del parámetro
        
        # Obtener contexto del usuario
        user_context = personalization_service.get_user_context(user_id)
        
        # Extraer entidades de documentos adjuntos
        extracted_entities = {"entities": [], "specific_data": {}}
        
        if attachment_ids:
            all_entities = []
            all_specific_data = {}
            
            for attachment_id in attachment_ids:
                attachment_info = document_analysis_service.get_attachment_info(
                    attachment_id, user_id
                )
                
                if attachment_info and attachment_info.get("legal_entities"):
                    legal_entities = attachment_info["legal_entities"]
                    
                    entities = legal_entities.get("entities", [])
                    all_entities.extend(entities)
                    
                    specific_data = legal_entities.get("specific_data", {})
                    all_specific_data.update(specific_data)
            
            extracted_entities = {
                "entities": all_entities,
                "specific_data": all_specific_data
            }
        
        # Analizar contexto para sugerir plantilla
        suggested_template = _suggest_template_from_context(
            conversation_context, extracted_entities
        )
        
        # Extraer campos sugeridos
        suggested_fields = _extract_suggested_fields(
            conversation_context, extracted_entities, user_context
        )
        
        return {
            "suggested_template": suggested_template,
            "suggested_fields": suggested_fields,
            "entities_found": len(extracted_entities["entities"]),
            "confidence_score": _calculate_suggestion_confidence(
                conversation_context, extracted_entities
            ),
            "analysis_summary": _generate_analysis_summary(
                conversation_context, extracted_entities
            )
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando contexto: {str(e)}"
        )


def _suggest_template_from_context(
    conversation_context: str, 
    extracted_entities: Dict[str, Any]
) -> Dict[str, Any]:
    """Sugiere la mejor plantilla basándose en el contexto."""
    
    context_lower = conversation_context.lower()
    
    # Palabras clave para diferentes tipos de documentos
    template_keywords = {
        "reclamacion_factura_smart": [
            "factura", "reclamación", "cobro", "importe", "facturación",
            "electricidad", "gas", "agua", "telefono", "internet"
        ],
        "recurso_multa_smart": [
            "multa", "sanción", "recurso", "infracción", "expediente",
            "tráfico", "ayuntamiento", "denuncia"
        ]
    }
    
    # Calcular puntuaciones
    scores = {}
    for template_id, keywords in template_keywords.items():
        score = sum(1 for keyword in keywords if keyword in context_lower)
        
        # Bonus por entidades específicas
        entities = extracted_entities.get("entities", [])
        for entity in entities:
            entity_type = entity.get("type", "").lower()
            if template_id == "reclamacion_factura_smart" and "factura" in entity_type:
                score += 2
            elif template_id == "recurso_multa_smart" and "multa" in entity_type:
                score += 2
        
        scores[template_id] = score
    
    # Seleccionar mejor opción
    if scores:
        best_template = max(scores.items(), key=lambda x: x[1])
        if best_template[1] > 0:
            return {
                "template_id": best_template[0],
                "confidence": min(best_template[1] / 10, 1.0),
                "reason": f"Detectadas {best_template[1]} coincidencias relevantes"
            }
    
    return {
        "template_id": "reclamacion_factura_smart",  # Por defecto
        "confidence": 0.3,
        "reason": "Plantilla por defecto - no se detectó contexto específico"
    }


def _extract_suggested_fields(
    conversation_context: str,
    extracted_entities: Dict[str, Any],
    user_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Extrae campos sugeridos del contexto."""
    
    fields = {}
    
    # Campos del perfil de usuario
    user_profile = user_context.get("profile", {})
    if user_profile.get("full_name"):
        fields["nombre_completo"] = user_profile["full_name"]
    if user_profile.get("email"):
        fields["email"] = user_profile["email"]
    
    # Campos de entidades extraídas
    entities = extracted_entities.get("entities", [])
    for entity in entities:
        entity_type = entity.get("type", "").lower()
        entity_value = entity.get("value", "")
        
        if "dni" in entity_type:
            fields["dni"] = entity_value
        elif "factura" in entity_type:
            fields["numero_factura"] = entity_value
        elif "euros" in entity_type or "importe" in entity_type:
            fields["importe_total"] = entity_value
        elif "fecha" in entity_type:
            fields["fecha_factura"] = entity_value
    
    # Campos específicos del documento
    specific_data = extracted_entities.get("specific_data", {})
    fields.update(specific_data)
    
    return fields


def _calculate_suggestion_confidence(
    conversation_context: str,
    extracted_entities: Dict[str, Any]
) -> float:
    """Calcula confianza de las sugerencias."""
    
    confidence = 0.0
    
    # Bonus por longitud del contexto
    if len(conversation_context) > 100:
        confidence += 0.2
    
    # Bonus por entidades extraídas
    entities_count = len(extracted_entities.get("entities", []))
    confidence += min(entities_count * 0.1, 0.5)
    
    # Bonus por datos específicos
    specific_data_count = len(extracted_entities.get("specific_data", {}))
    confidence += min(specific_data_count * 0.05, 0.3)
    
    return min(confidence, 1.0)


def _generate_analysis_summary(
    conversation_context: str,
    extracted_entities: Dict[str, Any]
) -> str:
    """Genera resumen del análisis de contexto."""
    
    entities_count = len(extracted_entities.get("entities", []))
    specific_data_count = len(extracted_entities.get("specific_data", {}))
    context_length = len(conversation_context)
    
    summary = f"Análisis completado: {context_length} caracteres de contexto, "
    summary += f"{entities_count} entidades extraídas, "
    summary += f"{specific_data_count} campos específicos identificados."
    
    if entities_count > 5:
        summary += " Alto nivel de información estructurada detectada."
    elif entities_count > 2:
        summary += " Información moderada para generación de documento."
    else:
        summary += " Información limitada - se usarán campos por defecto."
    
    return summary