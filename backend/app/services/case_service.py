"""
Servicio de expedientes de caso.
Agrupa conversaciones, documentos y alertas bajo un mismo caso legal.
Todos los métodos verifican que el user_id es propietario del recurso (aislamiento total).
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

# Whitelist de valores permitidos para evitar inyección de datos inválidos
VALID_STATUSES = frozenset({"open", "resolved", "archived"})
VALID_CATEGORIES = frozenset({
    "laboral", "vivienda", "consumo", "familia",
    "trafico", "administrativo", "fiscal", "penal", "otro",
})


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ─── CRUD ─────────────────────────────────────────────────────────────────────

def create_case(
    user_id: str,
    title: str,
    category: Optional[str],
    summary: Optional[str],
    subcategory: Optional[str] = None,
) -> Dict[str, Any]:
    """Crea un nuevo caso con workflow auto-poblado según categoría."""
    from app.config.workflow_templates import get_workflow_template

    supabase = get_supabase_client()
    now = _now_iso()
    safe_category = category if category in VALID_CATEGORIES else None
    safe_summary = summary[:1000] if summary else None

    # Auto-populate workflow from templates
    template = get_workflow_template(safe_category or "otro", subcategory)
    workflow_steps = template.get("steps", [])
    required_documents = template.get("documents", [])

    row: Dict[str, Any] = {
        "user_id": user_id,
        "title": title[:120],
        "category": safe_category,
        "status": "open",
        "summary": safe_summary,
        "created_at": now,
        "updated_at": now,
        "workflow_steps": workflow_steps,
        "required_documents": required_documents,
        "progress_pct": 0,
    }
    if subcategory:
        row["subcategory"] = subcategory[:50]

    # Set next_action from first step
    if workflow_steps:
        row["next_action"] = workflow_steps[0].get("title", "")

    result = supabase.table("cases").insert(row).execute()

    if not result.data:
        raise ValueError("Error creando el caso")
    return result.data[0]


def count_open_cases(user_id: str) -> int:
    """Cuenta cuántos casos con status='open' tiene el usuario."""
    supabase = get_supabase_client()
    result = (
        supabase.table("cases")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .eq("status", "open")
        .execute()
    )
    return result.count or 0


def list_cases(user_id: str) -> List[Dict[str, Any]]:
    """Lista todos los casos del usuario con contadores de conversaciones y alertas."""
    supabase = get_supabase_client()
    result = (
        supabase.table("cases")
        .select("id, title, category, subcategory, status, summary, progress_pct, next_action, created_at, updated_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    cases = result.data or []
    if not cases:
        return []

    # Fetch conversation and alert counts in 2 bulk queries instead of 2*N
    case_ids = [c["id"] for c in cases]

    try:
        conv_res = (
            supabase.table("conversations")
            .select("case_id")
            .in_("case_id", case_ids)
            .execute()
        )
        conv_counts: dict[str, int] = {}
        for row in (conv_res.data or []):
            cid = row["case_id"]
            conv_counts[cid] = conv_counts.get(cid, 0) + 1
    except Exception:
        conv_counts = {}

    try:
        alert_res = (
            supabase.table("alerts")
            .select("case_id")
            .in_("case_id", case_ids)
            .execute()
        )
        alert_counts: dict[str, int] = {}
        for row in (alert_res.data or []):
            cid = row["case_id"]
            alert_counts[cid] = alert_counts.get(cid, 0) + 1
    except Exception:
        alert_counts = {}

    for case in cases:
        case["conversation_count"] = conv_counts.get(case["id"], 0)
        case["alert_count"] = alert_counts.get(case["id"], 0)

    return cases


def get_case(user_id: str, case_id: str) -> Optional[Dict[str, Any]]:
    """
    Devuelve el detalle completo de un caso: conversaciones y alertas vinculadas.
    Retorna None si el caso no existe o no pertenece al usuario.
    """
    supabase = get_supabase_client()

    # Verificar propiedad antes de cualquier otra consulta
    result = (
        supabase.table("cases")
        .select("*")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not result.data:
        return None

    case = result.data[0]

    # Conversaciones vinculadas
    try:
        conv_res = (
            supabase.table("conversations")
            .select("id, title, created_at")
            .eq("case_id", case_id)
            .order("created_at", desc=True)
            .execute()
        )
        case["conversations"] = conv_res.data or []
    except Exception as e:
        logger.error("Error fetching conversations for case %s: %s", case_id, e)
        case["conversations"] = []

    # Alertas vinculadas
    try:
        alert_res = (
            supabase.table("alerts")
            .select("id, description, deadline_date, status, urgency_level")
            .eq("case_id", case_id)
            .order("deadline_date", desc=False)
            .execute()
        )
        case["alerts"] = alert_res.data or []
    except Exception as e:
        logger.error("Error fetching alerts for case %s: %s", case_id, e)
        case["alerts"] = []

    return case


def update_case(user_id: str, case_id: str, updates: Dict[str, Any]) -> bool:
    """
    Actualiza título, status, resumen o categoría de un caso.
    Verifica propiedad antes de actualizar. Filtra campos no permitidos.
    """
    supabase = get_supabase_client()

    # Ownership check (double-check; RLS also enforces this at DB level)
    existing = (
        supabase.table("cases")
        .select("id")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not existing.data:
        return False

    safe: Dict[str, Any] = {}
    if "title" in updates and updates["title"]:
        safe["title"] = str(updates["title"])[:120]
    if "status" in updates and updates["status"] in VALID_STATUSES:
        safe["status"] = updates["status"]
    if "summary" in updates:
        safe["summary"] = str(updates["summary"])[:1000] if updates["summary"] else None
    if "category" in updates:
        safe["category"] = updates["category"] if updates["category"] in VALID_CATEGORIES else None

    if not safe:
        return True  # Nothing to update

    safe["updated_at"] = _now_iso()
    supabase.table("cases").update(safe).eq("id", case_id).eq("user_id", user_id).execute()
    return True


def delete_case(user_id: str, case_id: str) -> bool:
    """
    Elimina un caso.
    Primero desvincula conversaciones y alertas (case_id → NULL) para no dejar huérfanos.
    """
    supabase = get_supabase_client()

    existing = (
        supabase.table("cases")
        .select("id")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not existing.data:
        return False

    # Unlink related records so they aren't orphaned
    supabase.table("conversations").update({"case_id": None}).eq("case_id", case_id).execute()
    supabase.table("alerts").update({"case_id": None}).eq("case_id", case_id).execute()

    # Delete the case (double filter for extra safety)
    supabase.table("cases").delete().eq("id", case_id).eq("user_id", user_id).execute()
    return True


# ─── Vincular / desvincular conversaciones ────────────────────────────────────

def link_conversation(user_id: str, case_id: str, conversation_id: str) -> bool:
    """
    Vincula una conversación a un caso.
    Verifica que tanto el caso como la conversación pertenecen al usuario.
    """
    supabase = get_supabase_client()

    case = (
        supabase.table("cases")
        .select("id")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not case.data:
        return False

    conv = (
        supabase.table("conversations")
        .select("id")
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not conv.data:
        return False

    supabase.table("conversations").update({"case_id": case_id}).eq("id", conversation_id).eq("user_id", user_id).execute()
    return True


def unlink_conversation(user_id: str, case_id: str, conversation_id: str) -> bool:
    """
    Desvincula una conversación de un caso.
    Verifica que el caso pertenece al usuario antes de desconectar.
    """
    supabase = get_supabase_client()

    case = (
        supabase.table("cases")
        .select("id")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not case.data:
        return False

    supabase.table("conversations").update({"case_id": None}).eq("id", conversation_id).eq("user_id", user_id).execute()
    return True


# ─── Workflow steps ──────────────────────────────────────────────────────────

VALID_STEP_STATUSES = frozenset({"pending", "in_progress", "completed", "skipped"})


def update_step_status(
    user_id: str, case_id: str, step_index: int, new_status: str
) -> Optional[Dict[str, Any]]:
    """
    Actualiza el estado de un paso de workflow y recalcula el progreso.
    Retorna el caso actualizado o None si no existe / no pertenece al usuario.
    """
    if new_status not in VALID_STEP_STATUSES:
        raise ValueError(f"Estado no válido: {new_status}")

    supabase = get_supabase_client()
    result = (
        supabase.table("cases")
        .select("*")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not result.data:
        return None

    case = result.data[0]
    steps: list = case.get("workflow_steps") or []

    if step_index < 0 or step_index >= len(steps):
        raise ValueError(f"Índice de paso fuera de rango: {step_index}")

    steps[step_index]["status"] = new_status

    # Recalculate progress
    total = len(steps)
    completed = sum(1 for s in steps if s["status"] in ("completed", "skipped"))
    progress = int((completed / total) * 100) if total > 0 else 0

    # Determine next action
    next_action = None
    for s in steps:
        if s["status"] in ("pending", "in_progress"):
            next_action = s.get("title", "")
            break

    updates = {
        "workflow_steps": steps,
        "progress_pct": progress,
        "next_action": next_action,
        "updated_at": _now_iso(),
    }

    # Auto-mark case as resolved when all steps done
    if progress == 100:
        updates["status"] = "resolved"

    supabase.table("cases").update(updates).eq("id", case_id).eq("user_id", user_id).execute()

    return {**case, **updates}


def update_document_check(
    user_id: str, case_id: str, doc_index: int, checked: bool
) -> Optional[Dict[str, Any]]:
    """Marca o desmarca un documento de la checklist."""
    supabase = get_supabase_client()
    result = (
        supabase.table("cases")
        .select("*")
        .eq("id", case_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not result.data:
        return None

    case = result.data[0]
    docs: list = case.get("required_documents") or []

    if doc_index < 0 or doc_index >= len(docs):
        raise ValueError(f"Índice de documento fuera de rango: {doc_index}")

    docs[doc_index]["checked"] = checked

    supabase.table("cases").update({
        "required_documents": docs,
        "updated_at": _now_iso(),
    }).eq("id", case_id).eq("user_id", user_id).execute()

    return {**case, "required_documents": docs}


def create_case_from_conversation(
    user_id: str,
    conversation_id: str,
    title: str,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Crea un caso desde una conversación existente.
    Auto-vincula la conversación y aplica el workflow template.
    """
    supabase = get_supabase_client()

    # Verify conversation belongs to user
    conv = (
        supabase.table("conversations")
        .select("id, category, subcategory")
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not conv.data:
        return None

    conv_data = conv.data[0]
    effective_category = category or conv_data.get("category")
    effective_subcategory = subcategory or conv_data.get("subcategory")

    case = create_case(
        user_id=user_id,
        title=title,
        category=effective_category,
        summary=None,
        subcategory=effective_subcategory,
    )

    # Link the conversation to the new case
    supabase.table("conversations").update({"case_id": case["id"]}).eq("id", conversation_id).eq("user_id", user_id).execute()

    return case
