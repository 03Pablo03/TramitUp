"""
Portales oficiales de reclamación en España.
IMPORTANTE: Verificar URLs cada 3 meses. Los portales del gobierno
cambian con frecuencia. Actualizar last_verified tras cada revisión.
Última revisión: 2026-03-21
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Portal:
    name: str                         # Nombre del organismo
    url: str                          # URL directa al formulario de reclamación
    needs_digital_cert: bool          # ¿Requiere certificado digital / Cl@ve?
    also_by_post: bool                # ¿Se puede presentar también por correo postal?
    notes: Optional[str]              # Notas adicionales para el usuario
    last_verified: str                # Fecha de última verificación (YYYY-MM-DD)
    official_form_url: Optional[str] = None  # URL al formulario oficial PDF/web, si existe


PORTALS: dict[str, Portal] = {

    # ─── TRANSPORTE AÉREO ───────────────────────────────────────────────────
    "aerolinea": Portal(
        name="AESA — Agencia Estatal de Seguridad Aérea",
        url="https://www.seguridadaerea.gob.es/es/ambitos/transporte-aereo-comercial/derechos-de-los-pasajeros/reclamaciones",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Primero debes reclamar a la aerolínea. Si no responden en 1 mes, puedes acudir a AESA.",
        last_verified="2026-02-27",
        official_form_url="https://www.seguridadaerea.gob.es/es/ambitos/transporte-aereo-comercial/derechos-de-los-pasajeros/reclamaciones/formulario-de-reclamacion",
    ),

    # ─── BANCA Y SEGUROS ────────────────────────────────────────────────────
    "banco": Portal(
        name="Banco de España — Portal del Cliente Bancario",
        url="https://www.bde.es/bde/es/areas/clientes/Reclamaciones/como_presentar_una_r.html",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Primero debes agotar el SAC del banco (plazo máximo 2 meses). Si no responden o la respuesta es insatisfactoria, acude al Banco de España.",
        last_verified="2026-02-26",
        official_form_url="https://www.bde.es/bde/es/areas/clientes/Reclamaciones/como_presentar_una_r.html",
    ),
    "seguro": Portal(
        name="DGSFP — Dirección General de Seguros y Fondos de Pensiones",
        url="https://www.dgsfp.mineco.es/es/Consumidor/Reclamaciones/Paginas/Reclamaciones.aspx",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Primero debes agotar el SAC de la aseguradora (plazo máximo 2 meses). Si no resuelven, acude a la DGSFP.",
        last_verified="2026-02-26",
        official_form_url="https://www.dgsfp.mineco.es/es/Consumidor/Reclamaciones/Paginas/Reclamaciones.aspx",
    ),

    # ─── SUMINISTROS Y TELECOMUNICACIONES ───────────────────────────────────
    "luz_gas": Portal(
        name="CNMC — Comisión Nacional de Mercados y la Competencia",
        url="https://sede.cnmc.gob.es/reclamaciones",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Primero debes reclamar a la compañía suministradora. Si no responden en 1 mes, acude a la CNMC.",
        last_verified="2026-02-26",
        official_form_url="https://sede.cnmc.gob.es/reclamaciones",
    ),
    "internet_telefono": Portal(
        name="CNMC — Oficina de Atención al Usuario de Telecomunicaciones",
        url="https://telecos.cnmc.es/oficina-atencion-usuario",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Primero debes reclamar a la operadora (tienen 1 mes para responder). Si no resuelven, acude a la CNMC Telecos.",
        last_verified="2026-02-26",
        official_form_url="https://telecos.cnmc.es/oficina-atencion-usuario",
    ),

    # ─── CONSUMO Y COMERCIO ─────────────────────────────────────────────────
    "consumo_general": Portal(
        name="Sistema Arbitral de Consumo — Ministerio de Consumo",
        url="https://www.consumo.gob.es/es/areas-de-actuacion/sistema-arbitral-de-consumo",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Arbitraje gratuito y vinculante para conflictos entre consumidores y empresas adheridas. También puedes acudir a la OMIC de tu municipio como primer paso.",
        last_verified="2026-02-26",
        official_form_url="https://www.consumo.gob.es/es/areas-de-actuacion/sistema-arbitral-de-consumo/como-presentar-una-solicitud-de-arbitraje",
    ),
    "omic": Portal(
        name="OMIC — Oficina Municipal de Información al Consumidor",
        url="https://www.consumo.gob.es/es/omic",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Cada ayuntamiento tiene su propia OMIC. Busca la de tu municipio en el enlace.",
        last_verified="2026-02-26",
    ),

    # ─── TRÁFICO Y MULTAS ───────────────────────────────────────────────────
    "multa_trafico_dgt": Portal(
        name="DGT — Sede Electrónica (recurso de multas)",
        url="https://sede.dgt.gob.es/es/tramites-y-multas/multas/",
        needs_digital_cert=True,
        also_by_post=True,
        notes="Para multas de tráfico de competencia estatal (DGT). Plazo: 20 días hábiles desde notificación.",
        last_verified="2026-02-26",
        official_form_url="https://sede.dgt.gob.es/es/tramites-y-multas/multas/",
    ),
    "multa_trafico_ayuntamiento": Portal(
        name="Sede electrónica del ayuntamiento correspondiente",
        url="https://administracion.gob.es/pag_Home/atencionCiudadana/buscadorOrganismos.html",
        needs_digital_cert=True,
        also_by_post=True,
        notes="Para multas de tráfico municipales. Usa el buscador para encontrar el ayuntamiento concreto.",
        last_verified="2026-02-26",
    ),

    # ─── HACIENDA / AEAT ────────────────────────────────────────────────────
    "hacienda": Portal(
        name="AEAT — Sede Electrónica (recursos y reclamaciones)",
        url="https://sede.agenciatributaria.gob.es/Sede/procedimientoini/GC24.shtml",
        needs_digital_cert=True,
        also_by_post=True,
        notes="Para recursos de reposición y reclamaciones económico-administrativas ante la AEAT. Plazo: 1 mes desde la notificación.",
        last_verified="2026-02-27",
        official_form_url="https://sede.agenciatributaria.gob.es/Sede/procedimientoini/GC24.shtml",
    ),
    "tribunal_economico": Portal(
        name="TEAR — Tribunal Económico-Administrativo Regional",
        url="https://www.hacienda.gob.es/es-ES/Areas%20Tematicas/Tribunales%20Economico%20Administrativos/Paginas/ReclamacionesEconomico-Administrativas.aspx",
        needs_digital_cert=True,
        also_by_post=True,
        notes="Segunda instancia tras el recurso de reposición ante la AEAT. Plazo: 1 mes.",
        last_verified="2026-02-27",
    ),

    # ─── SEGURIDAD SOCIAL ───────────────────────────────────────────────────
    "seguridad_social": Portal(
        name="INSS — Sede Electrónica de la Seguridad Social",
        url="https://sede.seg-social.gob.es/",
        needs_digital_cert=True,
        also_by_post=True,
        notes="Para prestaciones, pensiones, bajas médicas y reclamaciones al INSS.",
        last_verified="2026-02-27",
    ),
    "sepe_paro": Portal(
        name="SEPE — Servicio Público de Empleo Estatal",
        url="https://sede.sepe.gob.es/",
        needs_digital_cert=True,
        also_by_post=True,
        notes="Para solicitar y gestionar la prestación por desempleo (paro).",
        last_verified="2026-02-27",
    ),

    # ─── LABORAL ────────────────────────────────────────────────────────────
    "smac": Portal(
        name="SMAC — Servicio de Mediación, Arbitraje y Conciliación",
        url="https://www.mites.gob.es/es/sec_trabajo/smac/index.htm",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Paso previo obligatorio antes de acudir al juzgado de lo social (art. 63 LRJS). Varía por comunidad autónoma — el enlace da acceso al directorio nacional.",
        last_verified="2026-02-27",
        official_form_url="https://www.mites.gob.es/es/sec_trabajo/smac/papeleta.htm",
    ),
    "inspeccion_trabajo": Portal(
        name="Inspección de Trabajo y Seguridad Social",
        url="https://sede.mites.gob.es/nlt/faces/home",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Para denunciar irregularidades laborales, accidentes de trabajo o incumplimientos del convenio colectivo.",
        last_verified="2026-02-27",
        official_form_url="https://sede.mites.gob.es/nlt/faces/home",
    ),

    # ─── VIVIENDA ───────────────────────────────────────────────────────────
    "fianza_vivienda": Portal(
        name="Organismo autonómico de depósito de fianzas",
        url="https://www.vivienda.gob.es/vivienda-y-suelo/alquiler/fianzas.html",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Cada comunidad autónoma gestiona el depósito de fianzas. El enlace redirige al directorio por CCAA.",
        last_verified="2026-02-27",
    ),
    "comunidad_propietarios": Portal(
        name="Juzgado de Primera Instancia (vía judicial)",
        url="https://www.poderjudicial.es/cgpj/es/Servicios/Oficina-Judicial-Virtual/",
        needs_digital_cert=True,
        also_by_post=False,
        notes="Para impugnar acuerdos de junta de propietarios. Plazo: 3 meses desde adopción del acuerdo.",
        last_verified="2026-02-27",
    ),

    # ─── PROTECCIÓN DE DATOS ────────────────────────────────────────────────
    "aepd": Portal(
        name="AEPD — Agencia Española de Protección de Datos",
        url="https://sedeagpd.gob.es/sede-electronica-web/vistas/formReclamacionDerechos/reclamacionDerechos.jsf",
        needs_digital_cert=False,
        also_by_post=True,
        notes="Para reclamaciones por uso indebido de datos personales.",
        last_verified="2026-02-26",
        official_form_url="https://sedeagpd.gob.es/sede-electronica-web/vistas/formReclamacionDerechos/reclamacionDerechos.jsf",
    ),
}


def get_portal(key: str) -> Portal | None:
    """Obtener portal por clave. Devuelve None si no existe."""
    return PORTALS.get(key)


def get_portal_summary(key: str) -> str:
    """
    Devuelve un bloque de texto formateado para incluir en la respuesta del chat.
    Ejemplo de output:
    
    📋 Dónde presentar tu reclamación:
    AESA — Agencia Estatal de Seguridad Aérea
    🔗 https://reclamaciones.seguridadaerea.gob.es
    ✅ No requiere certificado digital
    📮 También disponible por correo postal
    ℹ️ Primero debes reclamar a la aerolínea...
    """
    portal = PORTALS.get(key)
    if not portal:
        return ""

    cert_text = "✅ No requiere certificado digital" if not portal.needs_digital_cert \
        else "🔐 Requiere certificado digital o Cl@ve"
    post_text = "📮 También se puede presentar por correo postal" if portal.also_by_post else ""
    notes_text = f"ℹ️ {portal.notes}" if portal.notes else ""

    lines = [
        "📋 Dónde presentar tu reclamación:",
        f"**{portal.name}**",
        f"🔗 {portal.url}",
        cert_text,
    ]
    if post_text:
        lines.append(post_text)
    if notes_text:
        lines.append(notes_text)

    return "\n".join(lines)