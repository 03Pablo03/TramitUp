"""
Servicio de personalización inteligente para TramitUp.
Aprovecha datos del usuario y historial para mejorar respuestas de IA.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.core.supabase_client import get_supabase_client


class PersonalizationService:
    """Servicio que proporciona personalización basada en datos del usuario."""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene contexto completo del usuario para personalización.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con contexto del usuario
        """
        try:
            # Obtener perfil del usuario
            profile = self._get_user_profile(user_id)
            
            # Obtener historial de conversaciones
            conversation_history = self._get_conversation_patterns(user_id)
            
            # Obtener categorías de interés
            interest_categories = self._get_interest_categories(user_id)
            
            # Obtener patrones de uso
            usage_patterns = self._get_usage_patterns(user_id)
            
            return {
                "profile": profile,
                "conversation_history": conversation_history,
                "interest_categories": interest_categories,
                "usage_patterns": usage_patterns,
                "personalization_score": self._calculate_personalization_score(profile, conversation_history)
            }
            
        except Exception as e:
            print(f"Error getting user context: {e}")
            return self._get_default_context()
    
    def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Obtiene el perfil del usuario."""
        try:
            result = self.supabase.table("profiles").select(
                "name, categories_interest, onboarding_completed, plan, documents_used_today, created_at"
            ).eq("id", user_id).execute()
            
            if result.data:
                profile = result.data[0]
                return {
                    "name": profile.get("name"),
                    "categories_interest": profile.get("categories_interest", []),
                    "onboarding_completed": profile.get("onboarding_completed", False),
                    "plan": profile.get("plan", "free"),
                    "documents_used_today": profile.get("documents_used_today", 0),
                    "user_since": profile.get("created_at"),
                    "is_experienced_user": self._is_experienced_user(profile)
                }
            
            return {}
            
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return {}
    
    def _get_conversation_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones en el historial de conversaciones."""
        try:
            # Obtener conversaciones recientes (últimos 30 días)
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            
            result = self.supabase.table("conversations").select(
                "id, category, subcategory, created_at, updated_at"
            ).eq("user_id", user_id).gte("created_at", thirty_days_ago).execute()
            
            conversations = result.data or []
            
            # Analizar patrones
            category_frequency = {}
            subcategory_frequency = {}
            recent_topics = []
            
            for conv in conversations:
                category = conv.get("category")
                subcategory = conv.get("subcategory")
                
                if category:
                    category_frequency[category] = category_frequency.get(category, 0) + 1
                
                if subcategory:
                    subcategory_frequency[subcategory] = subcategory_frequency.get(subcategory, 0) + 1
                    recent_topics.append({
                        "category": category,
                        "subcategory": subcategory,
                        "date": conv.get("created_at")
                    })
            
            # Determinar categoría principal
            primary_category = max(category_frequency.items(), key=lambda x: x[1])[0] if category_frequency else None
            
            return {
                "total_conversations": len(conversations),
                "category_frequency": category_frequency,
                "subcategory_frequency": subcategory_frequency,
                "primary_category": primary_category,
                "recent_topics": recent_topics[-5:],  # Últimos 5 temas
                "conversation_frequency": self._calculate_conversation_frequency(conversations)
            }
            
        except Exception as e:
            print(f"Error analyzing conversation patterns: {e}")
            return {}
    
    def _get_interest_categories(self, user_id: str) -> List[str]:
        """Obtiene categorías de interés del usuario."""
        try:
            result = self.supabase.table("profiles").select("categories_interest").eq("id", user_id).execute()
            
            if result.data and result.data[0].get("categories_interest"):
                return result.data[0]["categories_interest"]
            
            return []
            
        except Exception as e:
            print(f"Error getting interest categories: {e}")
            return []
    
    def _get_usage_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analiza patrones de uso del usuario."""
        try:
            # Obtener estadísticas de uso diario
            result = self.supabase.table("daily_usage").select(
                "date, message_count, document_count"
            ).eq("user_id", user_id).order("date", desc=True).limit(30).execute()
            
            usage_data = result.data or []
            
            if not usage_data:
                return {}
            
            # Calcular métricas
            total_messages = sum(day.get("message_count", 0) for day in usage_data)
            total_documents = sum(day.get("document_count", 0) for day in usage_data)
            avg_messages_per_day = total_messages / len(usage_data) if usage_data else 0
            
            # Determinar tipo de usuario
            user_type = self._determine_user_type(avg_messages_per_day, total_documents)
            
            return {
                "total_messages_30d": total_messages,
                "total_documents_30d": total_documents,
                "avg_messages_per_day": avg_messages_per_day,
                "active_days": len(usage_data),
                "user_type": user_type,
                "last_activity": usage_data[0].get("date") if usage_data else None
            }
            
        except Exception as e:
            print(f"Error analyzing usage patterns: {e}")
            return {}
    
    def _is_experienced_user(self, profile: Dict[str, Any]) -> bool:
        """Determina si es un usuario experimentado."""
        try:
            created_at = profile.get("created_at")
            if not created_at:
                return False
            
            # Usuario experimentado si tiene más de 7 días y ha completado onboarding
            user_age = datetime.now() - datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            return user_age.days > 7 and profile.get("onboarding_completed", False)
            
        except Exception:
            return False
    
    def _calculate_conversation_frequency(self, conversations: List[Dict]) -> str:
        """Calcula la frecuencia de conversaciones del usuario."""
        if not conversations:
            return "new_user"
        
        if len(conversations) >= 10:
            return "high_frequency"
        elif len(conversations) >= 3:
            return "medium_frequency"
        else:
            return "low_frequency"
    
    def _determine_user_type(self, avg_messages: float, total_documents: int) -> str:
        """Determina el tipo de usuario basado en patrones de uso."""
        if avg_messages >= 5 and total_documents >= 10:
            return "power_user"
        elif avg_messages >= 2 and total_documents >= 3:
            return "regular_user"
        elif total_documents >= 1:
            return "document_focused"
        else:
            return "casual_user"
    
    def _calculate_personalization_score(self, profile: Dict, history: Dict) -> float:
        """Calcula un score de personalización (0-1)."""
        score = 0.0
        
        # Puntuación por completitud del perfil
        if profile.get("name"):
            score += 0.2
        if profile.get("categories_interest"):
            score += 0.2
        if profile.get("onboarding_completed"):
            score += 0.2
        
        # Puntuación por historial
        if history.get("total_conversations", 0) > 0:
            score += 0.2
        if history.get("primary_category"):
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_default_context(self) -> Dict[str, Any]:
        """Contexto por defecto para usuarios nuevos."""
        return {
            "profile": {},
            "conversation_history": {},
            "interest_categories": [],
            "usage_patterns": {},
            "personalization_score": 0.0
        }
    
    def get_contextual_prompt_additions(self, user_context: Dict[str, Any]) -> str:
        """
        Genera adiciones contextuales para el prompt basadas en el contexto del usuario.
        
        Args:
            user_context: Contexto del usuario obtenido de get_user_context
            
        Returns:
            String con adiciones contextuales para el prompt
        """
        additions = []
        
        profile = user_context.get("profile", {})
        history = user_context.get("conversation_history", {})
        interests = user_context.get("interest_categories", [])
        usage = user_context.get("usage_patterns", {})
        
        # Personalización por nombre
        if profile.get("name"):
            additions.append(f"El usuario se llama {profile['name']}.")
        
        # Personalización por experiencia
        if profile.get("is_experienced_user"):
            additions.append("Es un usuario experimentado, puedes usar terminología más técnica.")
        else:
            additions.append("Es un usuario nuevo, explica conceptos básicos claramente.")
        
        # Personalización por categorías de interés
        if interests:
            categories_text = ", ".join(interests)
            additions.append(f"Sus áreas de interés principales son: {categories_text}.")
        
        # Personalización por historial
        primary_category = history.get("primary_category")
        if primary_category:
            additions.append(f"Ha consultado principalmente sobre: {primary_category}.")
        
        # Personalización por tipo de usuario
        user_type = usage.get("user_type")
        if user_type == "power_user":
            additions.append("Es un usuario avanzado que genera muchos documentos.")
        elif user_type == "document_focused":
            additions.append("Se enfoca principalmente en generar documentos legales.")
        elif user_type == "casual_user":
            additions.append("Es un usuario ocasional, proporciona explicaciones detalladas.")
        
        # Personalización por plan
        if profile.get("plan") == "pro":
            additions.append("Tiene plan PRO, puedes sugerir funcionalidades avanzadas.")
        
        if additions:
            return "\n\nCONTEXTO DEL USUARIO:\n" + " ".join(additions)
        
        return ""


# Instancia global del servicio
personalization_service = PersonalizationService()