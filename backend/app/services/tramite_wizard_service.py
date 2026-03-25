"""
Servicio para trámites guiados (wizards).
Gestiona el estado del wizard, valida formularios, triggerea análisis IA,
genera documentos y crea alertas automáticas.
"""
import json
import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from app.core.supabase_client import get_supabase_client
from app.config.tramite_templates import get_tramite_template, list_tramite_templates, TRAMITE_TEMPLATES

logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ─── Template listing ────────────────────────────────────────────────────────

def get_templates() -> List[Dict[str, Any]]:
    """Lista todos los templates disponibles (resumen sin steps detallados)."""
    return list_tramite_templates()


def get_template_detail(template_id: str) -> Optional[Dict[str, Any]]:
    """Retorna un template completo con steps."""
    return get_tramite_template(template_id)


# ─── Wizard CRUD ─────────────────────────────────────────────────────────────

def start_wizard(user_id: str, template_id: str) -> Dict[str, Any]:
    """Inicia un nuevo wizard para el usuario."""
    template = get_tramite_template(template_id)
    if not template:
        raise ValueError(f"Template '{template_id}' no existe")

    steps = template["steps"]
    first_step = steps[0]["id"] if steps else "done"

    supabase = get_supabase_client()
    now = _now_iso()

    row = {
        "user_id": user_id,
        "template_id": template_id,
        "current_step": first_step,
        "step_data": {},
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
    }

    result = supabase.table("tramite_wizards").insert(row).execute()
    wizard = result.data[0]

    return {
        "wizard_id": wizard["id"],
        "template": template,
        "current_step": first_step,
        "step_data": {},
        "status": "in_progress",
    }


def get_wizard_status(user_id: str, wizard_id: str) -> Dict[str, Any]:
    """Obtiene el estado actual del wizard."""
    supabase = get_supabase_client()
    result = (
        supabase.table("tramite_wizards")
        .select("*")
        .eq("id", wizard_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    wizard = result.data
    if not wizard:
        raise ValueError("Wizard no encontrado")

    template = get_tramite_template(wizard["template_id"])
    steps = template["steps"] if template else []

    # Calculate progress
    step_data = wizard.get("step_data") or {}
    completed_steps = len([s for s in steps if s["id"] in step_data])
    total_steps = len(steps)
    progress_pct = int((completed_steps / total_steps) * 100) if total_steps else 0

    return {
        "wizard_id": wizard["id"],
        "template_id": wizard["template_id"],
        "template": template,
        "current_step": wizard["current_step"],
        "step_data": step_data,
        "status": wizard["status"],
        "progress_pct": progress_pct,
        "case_id": wizard.get("case_id"),
        "created_at": wizard.get("created_at"),
        "updated_at": wizard.get("updated_at"),
    }


def submit_step(
    user_id: str,
    wizard_id: str,
    step_id: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Procesa un paso del wizard.
    - form: valida y almacena datos
    - ai_analysis: triggerea análisis IA
    - document_generation: genera documento
    - follow_up: crea alerta automática
    - instructions: solo avanza
    """
    supabase = get_supabase_client()

    # Fetch wizard
    result = (
        supabase.table("tramite_wizards")
        .select("*")
        .eq("id", wizard_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    wizard = result.data
    if not wizard:
        raise ValueError("Wizard no encontrado")
    if wizard["status"] != "in_progress":
        raise ValueError("Este trámite ya está completado")

    template = get_tramite_template(wizard["template_id"])
    if not template:
        raise ValueError("Template no encontrado")

    # Find step definition
    steps = template["steps"]
    step_def = next((s for s in steps if s["id"] == step_id), None)
    if not step_def:
        raise ValueError(f"Paso '{step_id}' no existe en este trámite")

    step_data = wizard.get("step_data") or {}
    step_result: Dict[str, Any] = {}

    # Process based on step type
    step_type = step_def["type"]

    if step_type == "form":
        step_result = _process_form_step(step_def, data)
    elif step_type == "ai_analysis":
        step_result = _process_ai_analysis(template, step_def, step_data, data)
    elif step_type == "document_generation":
        step_result = _process_document_generation(template, step_def, step_data, user_id)
    elif step_type == "instructions":
        step_result = {"acknowledged": True}
    elif step_type == "follow_up":
        step_result = _process_follow_up(step_def, step_data, user_id, wizard_id)
    else:
        step_result = {"acknowledged": True}

    # Save step data
    step_data[step_id] = step_result

    # Determine next step
    current_idx = next((i for i, s in enumerate(steps) if s["id"] == step_id), -1)
    next_step = steps[current_idx + 1]["id"] if current_idx + 1 < len(steps) else "done"
    new_status = "completed" if next_step == "done" else "in_progress"

    supabase.table("tramite_wizards").update({
        "step_data": step_data,
        "current_step": next_step,
        "status": new_status,
        "updated_at": _now_iso(),
    }).eq("id", wizard_id).eq("user_id", user_id).execute()

    return {
        "step_id": step_id,
        "step_result": step_result,
        "next_step": next_step,
        "status": new_status,
    }


# ─── Step processors ────────────────────────────────────────────────────────

def _process_form_step(step_def: Dict, data: Dict) -> Dict[str, Any]:
    """Valida y almacena datos de formulario."""
    fields = step_def.get("fields", [])
    form_data = {}
    errors = []

    for field in fields:
        name = field["name"]
        value = data.get(name)

        if field.get("required") and not value:
            errors.append(f"El campo '{field['label']}' es obligatorio")
            continue

        if value is not None:
            # Type validation
            field_type = field.get("type", "text")
            if field_type == "number" and value:
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    errors.append(f"'{field['label']}' debe ser un número")
                    continue
            elif field_type == "select" and value:
                options = field.get("options", [])
                if options and value not in options:
                    errors.append(f"'{field['label']}': valor no válido")
                    continue

            form_data[name] = value

    if errors:
        raise ValueError("; ".join(errors))

    return {"form_data": form_data}


def _process_ai_analysis(
    template: Dict,
    step_def: Dict,
    step_data: Dict,
    extra_data: Dict,
) -> Dict[str, Any]:
    """Genera análisis IA basado en los datos recopilados."""
    from app.ai.llm_client import get_llm

    # Collect all form data from previous steps
    all_form_data = {}
    for sid, sdata in step_data.items():
        if isinstance(sdata, dict) and "form_data" in sdata:
            all_form_data.update(sdata["form_data"])

    prompt_context = step_def.get("prompt_context", "Analiza este caso legal.")

    # Build analysis prompt
    case_summary = "\n".join(f"- {k}: {v}" for k, v in all_form_data.items() if v)
    prompt = f"""Eres un asistente legal especializado en derecho español.

{prompt_context}

Datos del caso:
{case_summary}

Proporciona un análisis estructurado que incluya:
1. **Resumen de la situación**: Descripción clara del caso
2. **Base legal**: Normativa aplicable y artículos relevantes
3. **Derechos del usuario**: Qué le corresponde según la ley
4. **Cálculos** (si aplican): Indemnización, compensación o importes estimados
5. **Viabilidad**: Probabilidad de éxito de la reclamación (alta/media/baja)
6. **Plazos importantes**: Fechas límite a tener en cuenta
7. **Recomendación**: Qué debería hacer el usuario

IMPORTANTE: Responde en español. Sé específico con cifras y plazos concretos.
No inventes datos que no se proporcionan."""

    try:
        llm = get_llm(temperature=0.3, max_output_tokens=2048)
        result = llm.invoke(prompt)
        analysis_text = result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        logger.error("Error en análisis IA del wizard: %s", e)
        analysis_text = (
            "No se pudo completar el análisis automático. "
            "Puedes continuar con el trámite y consultar a un profesional para un análisis detallado."
        )

    return {
        "analysis": analysis_text,
        "form_data_used": all_form_data,
    }


def _process_document_generation(
    template: Dict,
    step_def: Dict,
    step_data: Dict,
    user_id: str,
) -> Dict[str, Any]:
    """Genera un documento legal basado en datos recopilados y análisis."""
    from app.ai.llm_client import get_llm
    from app.ai.prompts.system_base import AVISO_LEGAL_UI

    # Collect all form data and analysis
    all_form_data = {}
    analysis_text = ""
    for sid, sdata in step_data.items():
        if isinstance(sdata, dict):
            if "form_data" in sdata:
                all_form_data.update(sdata["form_data"])
            if "analysis" in sdata:
                analysis_text = sdata["analysis"]

    doc_type = step_def.get("description", "documento legal")
    template_title = template.get("title", "Trámite")

    case_summary = "\n".join(f"- {k}: {v}" for k, v in all_form_data.items() if v)

    prompt = f"""Eres un asistente legal experto en redacción de documentos legales españoles.

Genera un documento formal de tipo: {doc_type}
Para el trámite: {template_title}

Datos del caso:
{case_summary}

Análisis previo:
{analysis_text[:1500]}

Instrucciones:
- Redacta un documento formal, profesional y completo
- Incluye todos los datos proporcionados
- Usa formato de carta/escrito formal español
- Incluye lugar para firma y fecha
- Deja marcadores [NOMBRE COMPLETO], [DNI], [DIRECCIÓN] donde el usuario deba completar sus datos personales
- Cita la normativa aplicable
- Sé claro y preciso en las peticiones

Responde SOLO con el contenido del documento, sin explicaciones previas."""

    try:
        llm = get_llm(temperature=0.2, max_output_tokens=4096)
        result = llm.invoke(prompt)
        doc_content = result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        logger.error("Error generando documento en wizard: %s", e)
        doc_content = (
            "No se pudo generar el documento automáticamente. "
            "Puedes usar los datos del análisis para redactarlo manualmente o consultar a un profesional."
        )

    return {
        "document_content": doc_content,
        "document_title": f"{template_title} - Documento generado",
        "legal_notice": AVISO_LEGAL_UI,
    }


def _process_follow_up(
    step_def: Dict,
    step_data: Dict,
    user_id: str,
    wizard_id: str,
) -> Dict[str, Any]:
    """Crea alerta automática de seguimiento si aplica."""
    auto_alert_days = step_def.get("auto_alert_days")
    auto_alert_desc = step_def.get("auto_alert_description", "Seguimiento de tu trámite")

    alert_created = False
    alert_id = None

    if auto_alert_days:
        try:
            from app.services.alerts_service import create_alert
            deadline = date.today() + timedelta(days=auto_alert_days)
            alert = create_alert(
                user_id=user_id,
                conversation_id=None,
                description=auto_alert_desc,
                deadline_date=deadline,
                notify_days_before=[7, 3, 1],
            )
            alert_created = True
            alert_id = alert.get("id")
        except Exception as e:
            logger.warning("No se pudo crear alerta automática: %s", e)

    return {
        "alert_created": alert_created,
        "alert_id": alert_id,
        "alert_days": auto_alert_days,
        "alert_description": auto_alert_desc,
    }


# ─── Link wizard to case ────────────────────────────────────────────────────

def link_wizard_to_case(user_id: str, wizard_id: str, case_id: str) -> Dict[str, Any]:
    """Vincula un wizard a un expediente existente."""
    supabase = get_supabase_client()
    supabase.table("tramite_wizards").update({
        "case_id": case_id,
        "updated_at": _now_iso(),
    }).eq("id", wizard_id).eq("user_id", user_id).execute()
    return {"wizard_id": wizard_id, "case_id": case_id}


def list_user_wizards(user_id: str) -> List[Dict[str, Any]]:
    """Lista los wizards del usuario."""
    supabase = get_supabase_client()
    result = (
        supabase.table("tramite_wizards")
        .select("id, template_id, current_step, status, case_id, created_at, updated_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )
    wizards = result.data or []

    # Enrich with template info
    for w in wizards:
        tmpl = get_tramite_template(w["template_id"])
        if tmpl:
            w["template_title"] = tmpl["title"]
            w["template_icon"] = tmpl["icon"]
        else:
            w["template_title"] = w["template_id"]
            w["template_icon"] = "📋"

    return wizards
