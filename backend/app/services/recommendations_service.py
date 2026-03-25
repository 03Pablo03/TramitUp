"""
Motor de recomendaciones personalizadas.
Combina el historial del usuario con los trámites disponibles
para sugerir acciones relevantes y oportunas.
"""
import logging
from typing import Any, Dict, List

from app.core.supabase_client import get_supabase_client
from app.config.tramite_templates import list_tramite_templates

logger = logging.getLogger(__name__)

# Category → relevant wizard template IDs
_CATEGORY_WIZARD_MAP: Dict[str, List[str]] = {
    "laboral": ["despido_improcedente"],
    "consumo": ["reclamar_vuelo", "reclamar_factura"],
    "vivienda": ["reclamar_fianza"],
    "trafico": ["recurrir_multa"],
    "reclamaciones": ["reclamar_vuelo", "reclamar_factura"],
}

# Subcategory → specific wizard template
_SUBCATEGORY_WIZARD_MAP: Dict[str, str] = {
    "aerolinea": "reclamar_vuelo",
    "despido": "despido_improcedente",
    "finiquito": "despido_improcedente",
    "fianza": "reclamar_fianza",
    "alquiler": "reclamar_fianza",
    "multa": "recurrir_multa",
    "factura": "reclamar_factura",
}


def get_personalized_recommendations(user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Genera recomendaciones personalizadas combinando:
    1. Trámites guiados relevantes basados en conversaciones recientes
    2. Acciones pendientes (wizards incompletos, alertas próximas)
    3. Sugerencias basadas en perfil del usuario
    """
    recommendations = []

    try:
        supabase = get_supabase_client()

        # Get user profile and interests
        profile_result = supabase.table("profiles").select(
            "categories_interest, situation_type, first_scenario"
        ).eq("id", user_id).single().execute()
        profile = profile_result.data or {}

        # Get recent conversation categories
        conv_result = (
            supabase.table("conversations")
            .select("category, subcategory")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .limit(10)
            .execute()
        )
        recent_convs = conv_result.data or []

        # Get completed wizard template IDs to avoid re-suggesting
        wizard_result = (
            supabase.table("tramite_wizards")
            .select("template_id, status")
            .eq("user_id", user_id)
            .execute()
        )
        completed_wizards = {
            w["template_id"] for w in (wizard_result.data or []) if w["status"] == "completed"
        }
        in_progress_wizards = [
            w for w in (wizard_result.data or []) if w["status"] == "in_progress"
        ]

        # 1. Recommend based on recent conversations
        suggested_templates = set()
        for conv in recent_convs:
            sub = conv.get("subcategory", "")
            cat = conv.get("category", "")

            if sub and sub in _SUBCATEGORY_WIZARD_MAP:
                tmpl_id = _SUBCATEGORY_WIZARD_MAP[sub]
                if tmpl_id not in completed_wizards and tmpl_id not in suggested_templates:
                    suggested_templates.add(tmpl_id)
                    recommendations.append({
                        "type": "wizard_suggestion",
                        "priority": "high",
                        "title": f"Trámite guiado recomendado",
                        "template_id": tmpl_id,
                        "reason": f"Basado en tu consulta sobre {sub}",
                        "action_url": f"/wizard/{tmpl_id}",
                        "action_label": "Iniciar trámite",
                    })
            elif cat and cat in _CATEGORY_WIZARD_MAP:
                for tmpl_id in _CATEGORY_WIZARD_MAP[cat]:
                    if tmpl_id not in completed_wizards and tmpl_id not in suggested_templates:
                        suggested_templates.add(tmpl_id)
                        recommendations.append({
                            "type": "wizard_suggestion",
                            "priority": "medium",
                            "title": "Trámite guiado disponible",
                            "template_id": tmpl_id,
                            "reason": f"Relacionado con tus consultas de {cat}",
                            "action_url": f"/wizard/{tmpl_id}",
                            "action_label": "Iniciar trámite",
                        })

        # 2. Recommend based on user profile/interests
        interests = profile.get("categories_interest") or []
        for interest in interests:
            if interest in _CATEGORY_WIZARD_MAP:
                for tmpl_id in _CATEGORY_WIZARD_MAP[interest]:
                    if tmpl_id not in completed_wizards and tmpl_id not in suggested_templates:
                        suggested_templates.add(tmpl_id)
                        recommendations.append({
                            "type": "interest_suggestion",
                            "priority": "low",
                            "title": "Puede interesarte",
                            "template_id": tmpl_id,
                            "reason": f"Basado en tus intereses en {interest}",
                            "action_url": f"/wizard/{tmpl_id}",
                            "action_label": "Explorar",
                        })

        # 3. Enrich recommendations with template info
        all_templates = {t["id"]: t for t in list_tramite_templates()}
        for rec in recommendations:
            tmpl_id = rec.get("template_id", "")
            if tmpl_id in all_templates:
                tmpl = all_templates[tmpl_id]
                rec["template_title"] = tmpl["title"]
                rec["template_icon"] = tmpl["icon"]
                rec["template_description"] = tmpl["description"]

        # 4. Add generic actions if few recommendations
        if len(recommendations) < 2:
            recommendations.append({
                "type": "explore",
                "priority": "low",
                "title": "Explora los trámites guiados",
                "reason": "Te ayudamos paso a paso con tus gestiones legales",
                "action_url": "/wizard",
                "action_label": "Ver trámites",
                "template_icon": "📋",
                "template_title": "Todos los trámites",
            })

    except Exception as e:
        logger.warning("Error generating recommendations: %s", e)

    # Sort by priority and limit
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda r: priority_order.get(r.get("priority", "low"), 2))
    return recommendations[:limit]
