"""
Servicio de sugerencias proactivas basado en patrones de usuario.
Genera recomendaciones inteligentes y oportunas para mejorar la experiencia.
"""

import json
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from app.core.supabase_client import get_supabase_client
from app.ai.llm_client import get_llm
from app.services.personalization_service import personalization_service


class SuggestionType(Enum):
    """Tipos de sugerencias proactivas."""
    DOCUMENT_TEMPLATE = "document_template"
    LEGAL_DEADLINE = "legal_deadline"
    FOLLOW_UP_ACTION = "follow_up_action"
    DOCUMENT_ANALYSIS = "document_analysis"
    RELATED_PROCEDURE = "related_procedure"
    PREVENTIVE_ACTION = "preventive_action"
    OPTIMIZATION_TIP = "optimization_tip"
    REGULATORY_UPDATE = "regulatory_update"


class SuggestionPriority(Enum):
    """Prioridades de sugerencias."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ProactiveSuggestion:
    """Sugerencia proactiva para el usuario."""
    id: str
    type: SuggestionType
    priority: SuggestionPriority
    title: str
    description: str
    action_text: str
    action_data: Dict[str, Any]
    context: Dict[str, Any]
    expires_at: Optional[datetime] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class ProactiveSuggestionsService:
    """Servicio de sugerencias proactivas basado en patrones de usuario."""
    
    def __init__(self):
        self.suggestion_generators = {
            SuggestionType.DOCUMENT_TEMPLATE: self._generate_template_suggestions,
            SuggestionType.LEGAL_DEADLINE: self._generate_deadline_suggestions,
            SuggestionType.FOLLOW_UP_ACTION: self._generate_followup_suggestions,
            SuggestionType.DOCUMENT_ANALYSIS: self._generate_analysis_suggestions,
            SuggestionType.RELATED_PROCEDURE: self._generate_related_suggestions,
            SuggestionType.PREVENTIVE_ACTION: self._generate_preventive_suggestions,
            SuggestionType.OPTIMIZATION_TIP: self._generate_optimization_suggestions,
            SuggestionType.REGULATORY_UPDATE: self._generate_regulatory_suggestions
        }
        
        self.pattern_analyzers = {
            "conversation_patterns": self._analyze_conversation_patterns,
            "document_patterns": self._analyze_document_patterns,
            "temporal_patterns": self._analyze_temporal_patterns,
            "success_patterns": self._analyze_success_patterns
        }
    
    async def generate_proactive_suggestions(
        self,
        user_id: str,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[ProactiveSuggestion]:
        """
        Genera sugerencias proactivas personalizadas para el usuario.
        
        Args:
            user_id: ID del usuario
            context: Contexto adicional (conversación actual, documentos, etc.)
            limit: Número máximo de sugerencias
            
        Returns:
            Lista de sugerencias ordenadas por relevancia y prioridad
        """
        # 1. Obtener contexto del usuario
        user_context = personalization_service.get_user_context(user_id)
        
        # 2. Analizar patrones del usuario
        user_patterns = await self._analyze_user_patterns(user_id)
        
        # 3. Obtener datos relevantes
        user_data = await self._get_user_data(user_id)
        
        # 4. Generar sugerencias por tipo
        all_suggestions = []
        
        for suggestion_type, generator in self.suggestion_generators.items():
            try:
                suggestions = await generator(
                    user_id, user_context, user_patterns, user_data, context or {}
                )
                all_suggestions.extend(suggestions)
            except Exception as e:
                print(f"Error generating {suggestion_type} suggestions: {e}")
        
        # 5. Filtrar sugerencias duplicadas y expiradas
        filtered_suggestions = self._filter_suggestions(all_suggestions)
        
        # 6. Ordenar por relevancia y prioridad
        ranked_suggestions = self._rank_suggestions(
            filtered_suggestions, user_context, user_patterns
        )
        
        # 7. Limitar resultados
        return ranked_suggestions[:limit]
    
    async def _analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones de comportamiento del usuario."""
        patterns = {}
        
        for pattern_name, analyzer in self.pattern_analyzers.items():
            try:
                pattern_data = await analyzer(user_id)
                patterns[pattern_name] = pattern_data
            except Exception as e:
                print(f"Error analyzing {pattern_name}: {e}")
                patterns[pattern_name] = {}
        
        return patterns
    
    async def _get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Obtiene datos relevantes del usuario."""
        try:
            supabase = get_supabase_client()
            
            # Conversaciones recientes
            conversations_result = supabase.table("conversations").select(
                "id, title, category, subcategory, created_at, updated_at"
            ).eq("user_id", user_id).order("updated_at", desc=True).limit(20).execute()
            
            # Documentos adjuntos recientes
            attachments_result = supabase.table("conversation_attachments").select(
                "id, filename, file_type, legal_entities, created_at"
            ).eq("user_id", user_id).order("created_at", desc=True).limit(10).execute()
            
            # Alertas activas
            alerts_result = supabase.table("alerts").select(
                "id, description, deadline_date, status, created_at"
            ).eq("user_id", user_id).eq("status", "active").order("deadline_date").execute()
            
            return {
                "conversations": conversations_result.data or [],
                "attachments": attachments_result.data or [],
                "alerts": alerts_result.data or []
            }
            
        except Exception as e:
            print(f"Error getting user data: {e}")
            return {"conversations": [], "attachments": [], "alerts": []}
    
    async def _analyze_conversation_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones en las conversaciones del usuario."""
        try:
            supabase = get_supabase_client()
            
            # Obtener conversaciones de los últimos 30 días
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            
            result = supabase.table("conversations").select(
                "category, subcategory, created_at"
            ).eq("user_id", user_id).gte("created_at", thirty_days_ago).execute()
            
            conversations = result.data or []
            
            # Analizar categorías más frecuentes
            category_counts = {}
            subcategory_counts = {}
            
            for conv in conversations:
                category = conv.get("category", "otro")
                subcategory = conv.get("subcategory", "general")
                
                category_counts[category] = category_counts.get(category, 0) + 1
                subcategory_counts[subcategory] = subcategory_counts.get(subcategory, 0) + 1
            
            # Calcular tendencias temporales
            recent_activity = len([c for c in conversations if 
                                 (datetime.now() - datetime.fromisoformat(c["created_at"].replace('Z', '+00:00'))).days <= 7])
            
            return {
                "total_conversations": len(conversations),
                "top_categories": sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "top_subcategories": sorted(subcategory_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "recent_activity": recent_activity,
                "activity_trend": "high" if recent_activity > 3 else "medium" if recent_activity > 1 else "low"
            }
            
        except Exception as e:
            print(f"Error analyzing conversation patterns: {e}")
            return {}
    
    async def _analyze_document_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones en los documentos del usuario."""
        try:
            supabase = get_supabase_client()
            
            result = supabase.table("conversation_attachments").select(
                "file_type, legal_entities, created_at"
            ).eq("user_id", user_id).execute()
            
            attachments = result.data or []
            
            # Analizar tipos de archivos
            file_type_counts = {}
            entity_type_counts = {}
            
            for attachment in attachments:
                file_type = attachment.get("file_type", "unknown")
                file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
                
                # Analizar entidades legales
                legal_entities = attachment.get("legal_entities", {})
                entities = legal_entities.get("entities", [])
                
                for entity in entities:
                    entity_type = entity.get("type", "unknown")
                    entity_type_counts[entity_type] = entity_type_counts.get(entity_type, 0) + 1
            
            return {
                "total_documents": len(attachments),
                "file_types": file_type_counts,
                "common_entities": sorted(entity_type_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                "has_financial_docs": any("factura" in str(e).lower() or "euros" in str(e).lower() 
                                        for attachment in attachments 
                                        for e in attachment.get("legal_entities", {}).get("entities", [])),
                "has_legal_docs": any("multa" in str(e).lower() or "sancion" in str(e).lower() 
                                    for attachment in attachments 
                                    for e in attachment.get("legal_entities", {}).get("entities", []))
            }
            
        except Exception as e:
            print(f"Error analyzing document patterns: {e}")
            return {}
    
    async def _analyze_temporal_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones temporales del usuario."""
        try:
            supabase = get_supabase_client()
            
            # Obtener actividad por días de la semana y horas
            result = supabase.table("conversations").select(
                "created_at"
            ).eq("user_id", user_id).execute()
            
            conversations = result.data or []
            
            # Analizar días de la semana (0=lunes, 6=domingo)
            weekday_counts = [0] * 7
            hour_counts = [0] * 24
            
            for conv in conversations:
                try:
                    dt = datetime.fromisoformat(conv["created_at"].replace('Z', '+00:00'))
                    weekday_counts[dt.weekday()] += 1
                    hour_counts[dt.hour] += 1
                except:
                    continue
            
            # Encontrar patrones
            most_active_weekday = weekday_counts.index(max(weekday_counts))
            most_active_hour = hour_counts.index(max(hour_counts))
            
            weekday_names = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            
            return {
                "most_active_weekday": weekday_names[most_active_weekday],
                "most_active_hour": most_active_hour,
                "weekend_user": sum(weekday_counts[5:7]) > sum(weekday_counts[0:5]),
                "business_hours_user": sum(hour_counts[9:18]) > sum(hour_counts[0:9] + hour_counts[18:24])
            }
            
        except Exception as e:
            print(f"Error analyzing temporal patterns: {e}")
            return {}
    
    async def _analyze_success_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones de éxito del usuario."""
        try:
            supabase = get_supabase_client()
            
            # Obtener alertas completadas vs activas
            alerts_result = supabase.table("alerts").select(
                "status, created_at"
            ).eq("user_id", user_id).execute()
            
            alerts = alerts_result.data or []
            
            completed_alerts = [a for a in alerts if a.get("status") == "completed"]
            active_alerts = [a for a in alerts if a.get("status") == "active"]
            
            # Calcular tasa de finalización
            total_alerts = len(alerts)
            completion_rate = len(completed_alerts) / total_alerts if total_alerts > 0 else 0
            
            return {
                "total_alerts": total_alerts,
                "completed_alerts": len(completed_alerts),
                "active_alerts": len(active_alerts),
                "completion_rate": completion_rate,
                "success_level": "high" if completion_rate > 0.7 else "medium" if completion_rate > 0.4 else "low"
            }
            
        except Exception as e:
            print(f"Error analyzing success patterns: {e}")
            return {}
    
    async def _generate_template_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias de plantillas de documentos."""
        suggestions = []
        
        # Sugerir plantillas basadas en conversaciones recientes
        recent_conversations = user_data.get("conversations", [])[:5]
        
        for conv in recent_conversations:
            category = conv.get("category", "")
            subcategory = conv.get("subcategory", "")
            
            # Sugerir plantilla de reclamación para facturas
            if "factura" in category.lower() or "reclamacion" in subcategory.lower():
                suggestions.append(ProactiveSuggestion(
                    id=f"template_reclamacion_{conv['id']}",
                    type=SuggestionType.DOCUMENT_TEMPLATE,
                    priority=SuggestionPriority.HIGH,
                    title="Generar Reclamación de Factura",
                    description=f"Basándose en tu conversación sobre '{conv['title']}', puedo ayudarte a generar una reclamación formal.",
                    action_text="Generar Documento",
                    action_data={
                        "template_id": "reclamacion_factura_smart",
                        "conversation_id": conv["id"]
                    },
                    context={"conversation": conv}
                ))
            
            # Sugerir recurso de multa
            elif "multa" in category.lower() or "sancion" in subcategory.lower():
                suggestions.append(ProactiveSuggestion(
                    id=f"template_recurso_{conv['id']}",
                    type=SuggestionType.DOCUMENT_TEMPLATE,
                    priority=SuggestionPriority.HIGH,
                    title="Generar Recurso de Multa",
                    description=f"Para tu consulta sobre '{conv['title']}', puedo crear un recurso de reposición profesional.",
                    action_text="Generar Recurso",
                    action_data={
                        "template_id": "recurso_multa_smart",
                        "conversation_id": conv["id"]
                    },
                    context={"conversation": conv}
                ))
        
        return suggestions
    
    async def _generate_deadline_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias sobre plazos legales."""
        suggestions = []
        
        # Alertas próximas a vencer
        alerts = user_data.get("alerts", [])
        
        for alert in alerts:
            try:
                deadline_date = datetime.fromisoformat(alert["deadline_date"])
                days_until_deadline = (deadline_date - datetime.now()).days
                
                if 1 <= days_until_deadline <= 7:  # Próximos 7 días
                    priority = SuggestionPriority.CRITICAL if days_until_deadline <= 3 else SuggestionPriority.HIGH
                    
                    suggestions.append(ProactiveSuggestion(
                        id=f"deadline_reminder_{alert['id']}",
                        type=SuggestionType.LEGAL_DEADLINE,
                        priority=priority,
                        title=f"Plazo próximo a vencer: {days_until_deadline} día(s)",
                        description=f"Tu alerta '{alert['description']}' vence el {deadline_date.strftime('%d/%m/%Y')}.",
                        action_text="Ver Detalles",
                        action_data={"alert_id": alert["id"]},
                        context={"alert": alert, "days_remaining": days_until_deadline}
                    ))
                    
            except Exception as e:
                print(f"Error processing alert deadline: {e}")
        
        return suggestions
    
    async def _generate_followup_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias de seguimiento."""
        suggestions = []
        
        # Conversaciones sin actividad reciente
        conversations = user_data.get("conversations", [])
        
        for conv in conversations:
            try:
                last_update = datetime.fromisoformat(conv["updated_at"].replace('Z', '+00:00'))
                days_since_update = (datetime.now() - last_update).days
                
                # Sugerir seguimiento para conversaciones importantes sin actividad
                if 7 <= days_since_update <= 30 and conv.get("category") != "otro":
                    suggestions.append(ProactiveSuggestion(
                        id=f"followup_{conv['id']}",
                        type=SuggestionType.FOLLOW_UP_ACTION,
                        priority=SuggestionPriority.MEDIUM,
                        title="Seguimiento Recomendado",
                        description=f"Han pasado {days_since_update} días desde tu última actividad en '{conv['title']}'.",
                        action_text="Continuar Conversación",
                        action_data={"conversation_id": conv["id"]},
                        context={"conversation": conv, "days_inactive": days_since_update}
                    ))
                    
            except Exception as e:
                print(f"Error processing conversation followup: {e}")
        
        return suggestions
    
    async def _generate_analysis_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias de análisis de documentos."""
        suggestions = []
        
        # Documentos sin análisis completo
        attachments = user_data.get("attachments", [])
        
        for attachment in attachments:
            legal_entities = attachment.get("legal_entities", {})
            entities_count = len(legal_entities.get("entities", []))
            
            # Sugerir análisis más profundo para documentos con pocas entidades
            if entities_count < 3 and attachment.get("file_type") == "application/pdf":
                suggestions.append(ProactiveSuggestion(
                    id=f"analysis_{attachment['id']}",
                    type=SuggestionType.DOCUMENT_ANALYSIS,
                    priority=SuggestionPriority.MEDIUM,
                    title="Análisis Mejorado Disponible",
                    description=f"Puedo extraer más información de '{attachment['filename']}'.",
                    action_text="Analizar Documento",
                    action_data={"attachment_id": attachment["id"]},
                    context={"attachment": attachment}
                ))
        
        return suggestions
    
    async def _generate_related_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias de procedimientos relacionados."""
        suggestions = []
        
        # Basado en patrones de conversación
        conversation_patterns = patterns.get("conversation_patterns", {})
        top_categories = conversation_patterns.get("top_categories", [])
        
        for category, count in top_categories:
            if category == "reclamaciones" and count >= 2:
                suggestions.append(ProactiveSuggestion(
                    id=f"related_consumer_rights",
                    type=SuggestionType.RELATED_PROCEDURE,
                    priority=SuggestionPriority.LOW,
                    title="Derechos del Consumidor",
                    description="Basándose en tus reclamaciones, podrías beneficiarte de conocer más sobre tus derechos como consumidor.",
                    action_text="Explorar Derechos",
                    action_data={"topic": "consumer_rights"},
                    context={"category": category, "frequency": count}
                ))
            
            elif category == "laboral" and count >= 2:
                suggestions.append(ProactiveSuggestion(
                    id=f"related_labor_rights",
                    type=SuggestionType.RELATED_PROCEDURE,
                    priority=SuggestionPriority.LOW,
                    title="Derechos Laborales",
                    description="Veo que tienes varias consultas laborales. Te puedo ayudar con información sobre tus derechos en el trabajo.",
                    action_text="Ver Información",
                    action_data={"topic": "labor_rights"},
                    context={"category": category, "frequency": count}
                ))
        
        return suggestions
    
    async def _generate_preventive_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias preventivas."""
        suggestions = []
        
        # Sugerencias basadas en patrones de documentos
        document_patterns = patterns.get("document_patterns", {})
        
        if document_patterns.get("has_financial_docs"):
            suggestions.append(ProactiveSuggestion(
                id="preventive_financial_organization",
                type=SuggestionType.PREVENTIVE_ACTION,
                priority=SuggestionPriority.LOW,
                title="Organización Financiera",
                description="Mantén tus documentos financieros organizados para futuras reclamaciones.",
                action_text="Ver Consejos",
                action_data={"topic": "financial_organization"},
                context={"pattern": "financial_documents"}
            ))
        
        if document_patterns.get("has_legal_docs"):
            suggestions.append(ProactiveSuggestion(
                id="preventive_legal_deadlines",
                type=SuggestionType.PREVENTIVE_ACTION,
                priority=SuggestionPriority.MEDIUM,
                title="Gestión de Plazos Legales",
                description="Configura recordatorios para todos tus plazos legales importantes.",
                action_text="Configurar Alertas",
                action_data={"topic": "legal_deadlines"},
                context={"pattern": "legal_documents"}
            ))
        
        return suggestions
    
    async def _generate_optimization_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias de optimización."""
        suggestions = []
        
        # Basado en patrones de éxito
        success_patterns = patterns.get("success_patterns", {})
        completion_rate = success_patterns.get("completion_rate", 0)
        
        if completion_rate < 0.5:
            suggestions.append(ProactiveSuggestion(
                id="optimization_task_management",
                type=SuggestionType.OPTIMIZATION_TIP,
                priority=SuggestionPriority.MEDIUM,
                title="Mejora tu Gestión de Tareas",
                description="He notado que algunas de tus alertas quedan pendientes. Te puedo ayudar a organizarte mejor.",
                action_text="Ver Consejos",
                action_data={"topic": "task_management"},
                context={"completion_rate": completion_rate}
            ))
        
        # Patrones temporales
        temporal_patterns = patterns.get("temporal_patterns", {})
        if not temporal_patterns.get("business_hours_user", True):
            suggestions.append(ProactiveSuggestion(
                id="optimization_business_hours",
                type=SuggestionType.OPTIMIZATION_TIP,
                priority=SuggestionPriority.LOW,
                title="Contacto en Horario Comercial",
                description="Para mejores resultados en trámites, considera realizar gestiones en horario comercial.",
                action_text="Ver Horarios",
                action_data={"topic": "business_hours"},
                context={"user_pattern": "non_business_hours"}
            ))
        
        return suggestions
    
    async def _generate_regulatory_suggestions(
        self, user_id: str, user_context: Dict, patterns: Dict, user_data: Dict, context: Dict
    ) -> List[ProactiveSuggestion]:
        """Genera sugerencias sobre actualizaciones normativas."""
        suggestions = []
        
        # Basado en categorías de interés del usuario
        conversation_patterns = patterns.get("conversation_patterns", {})
        top_categories = conversation_patterns.get("top_categories", [])
        
        for category, count in top_categories:
            if category == "vivienda" and count >= 1:
                suggestions.append(ProactiveSuggestion(
                    id="regulatory_housing_2024",
                    type=SuggestionType.REGULATORY_UPDATE,
                    priority=SuggestionPriority.INFO,
                    title="Ley de Vivienda 2024",
                    description="Hay cambios importantes en la normativa de vivienda que podrían afectarte.",
                    action_text="Ver Cambios",
                    action_data={"topic": "housing_law_2024"},
                    context={"category": category},
                    expires_at=datetime.now() + timedelta(days=30)
                ))
            
            elif category == "laboral" and count >= 1:
                suggestions.append(ProactiveSuggestion(
                    id="regulatory_labor_2024",
                    type=SuggestionType.REGULATORY_UPDATE,
                    priority=SuggestionPriority.INFO,
                    title="Actualizaciones Laborales 2024",
                    description="Nuevas regulaciones sobre teletrabajo y derechos digitales.",
                    action_text="Leer Más",
                    action_data={"topic": "labor_updates_2024"},
                    context={"category": category},
                    expires_at=datetime.now() + timedelta(days=45)
                ))
        
        return suggestions
    
    def _filter_suggestions(self, suggestions: List[ProactiveSuggestion]) -> List[ProactiveSuggestion]:
        """Filtra sugerencias duplicadas y expiradas."""
        filtered = []
        seen_ids = set()
        
        for suggestion in suggestions:
            # Filtrar duplicados
            if suggestion.id in seen_ids:
                continue
            
            # Filtrar expirados
            if suggestion.expires_at and suggestion.expires_at < datetime.now():
                continue
            
            seen_ids.add(suggestion.id)
            filtered.append(suggestion)
        
        return filtered
    
    def _rank_suggestions(
        self,
        suggestions: List[ProactiveSuggestion],
        user_context: Dict[str, Any],
        patterns: Dict[str, Any]
    ) -> List[ProactiveSuggestion]:
        """Ordena sugerencias por relevancia y prioridad."""
        
        def calculate_score(suggestion: ProactiveSuggestion) -> float:
            score = 0.0
            
            # Puntuación base por prioridad
            priority_scores = {
                SuggestionPriority.CRITICAL: 100,
                SuggestionPriority.HIGH: 80,
                SuggestionPriority.MEDIUM: 60,
                SuggestionPriority.LOW: 40,
                SuggestionPriority.INFO: 20
            }
            score += priority_scores.get(suggestion.priority, 0)
            
            # Bonus por tipo de sugerencia
            type_bonuses = {
                SuggestionType.LEGAL_DEADLINE: 20,
                SuggestionType.DOCUMENT_TEMPLATE: 15,
                SuggestionType.FOLLOW_UP_ACTION: 10,
                SuggestionType.DOCUMENT_ANALYSIS: 8,
                SuggestionType.PREVENTIVE_ACTION: 5
            }
            score += type_bonuses.get(suggestion.type, 0)
            
            # Penalty por antigüedad
            age_hours = (datetime.now() - suggestion.created_at).total_seconds() / 3600
            score -= age_hours * 0.1  # Pequeña penalización por antigüedad
            
            # Bonus por contexto relevante
            if suggestion.context:
                if "conversation" in suggestion.context:
                    score += 5
                if "days_remaining" in suggestion.context and suggestion.context["days_remaining"] <= 3:
                    score += 15
            
            return score
        
        # Ordenar por puntuación descendente
        return sorted(suggestions, key=calculate_score, reverse=True)
    
    async def mark_suggestion_as_seen(self, user_id: str, suggestion_id: str) -> bool:
        """Marca una sugerencia como vista por el usuario."""
        try:
            supabase = get_supabase_client()
            
            # Guardar en tabla de sugerencias vistas
            supabase.table("user_suggestion_interactions").upsert({
                "user_id": user_id,
                "suggestion_id": suggestion_id,
                "action": "seen",
                "created_at": datetime.now().isoformat()
            }).execute()
            
            return True
            
        except Exception as e:
            print(f"Error marking suggestion as seen: {e}")
            return False
    
    async def mark_suggestion_as_acted(self, user_id: str, suggestion_id: str, action_data: Dict[str, Any]) -> bool:
        """Marca una sugerencia como ejecutada por el usuario."""
        try:
            supabase = get_supabase_client()
            
            # Guardar interacción
            supabase.table("user_suggestion_interactions").insert({
                "user_id": user_id,
                "suggestion_id": suggestion_id,
                "action": "acted",
                "action_data": action_data,
                "created_at": datetime.now().isoformat()
            }).execute()
            
            return True
            
        except Exception as e:
            print(f"Error marking suggestion as acted: {e}")
            return False


# Instancia global del servicio
proactive_suggestions_service = ProactiveSuggestionsService()