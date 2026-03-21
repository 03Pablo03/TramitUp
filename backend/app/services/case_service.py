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
) -> Dict[str, Any]:
    """Crea un nuevo caso. Lanza ValueError si falla la inserción."""
    supabase = get_supabase_client()
    now = _now_iso()
    safe_category = category if category in VALID_CATEGORIES else None
    safe_summary = summary[:1000] if summary else None

    result = supabase.table("cases").insert({
        "user_id": user_id,
        "title": title[:120],
        "category": safe_category,
        "status": "open",
        "summary": safe_summary,
        "created_at": now,
        "updated_at": now,
    }).execute()

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
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    cases = result.data or []

    for case in cases:
        case_id = case["id"]
        try:
            conv_res = (
                supabase.table("conversations")
                .select("id", count="exact")
                .eq("case_id", case_id)
                .execute()
            )
            case["conversation_count"] = conv_res.count or 0
        except Exception:
            case["conversation_count"] = 0

        try:
            alert_res = (
                supabase.table("alerts")
                .select("id", count="exact")
                .eq("case_id", case_id)
                .execute()
            )
            case["alert_count"] = alert_res.count or 0
        except Exception:
            case["alert_count"] = 0

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
