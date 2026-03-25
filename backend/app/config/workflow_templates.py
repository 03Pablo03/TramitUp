"""
Plantillas de workflow para expedientes.
Cada categoría+subcategoría tiene un flujo paso a paso con documentos necesarios.
"""
from typing import Any

# ── Workflow Steps ────────────────────────────────────────────────────────────
# Cada step: { step, title, description, status: "pending" }
# status values: pending | in_progress | completed | skipped

WORKFLOW_TEMPLATES: dict[str, dict[str, Any]] = {
    "laboral_despido": {
        "label": "Despido",
        "steps": [
            {"step": 1, "title": "Recopilar documentación", "description": "Carta de despido, nóminas de los últimos 12 meses, contrato de trabajo e informe de vida laboral.", "status": "pending"},
            {"step": 2, "title": "Verificar importes", "description": "Usar la calculadora para comprobar la indemnización y el finiquito que te corresponden.", "status": "pending"},
            {"step": 3, "title": "Presentar papeleta de conciliación (SMAC)", "description": "Plazo de 20 días hábiles desde la notificación del despido. Se presenta en el SMAC de tu comunidad.", "status": "pending"},
            {"step": 4, "title": "Acto de conciliación", "description": "Asistir al acto de conciliación. Si hay acuerdo, se firma. Si no, se abre vía judicial.", "status": "pending"},
            {"step": 5, "title": "Demanda judicial (si necesario)", "description": "Si no hay acuerdo en conciliación, presentar demanda en el Juzgado de lo Social dentro del plazo.", "status": "pending"},
        ],
        "documents": [
            {"name": "Carta de despido", "required": True, "how_to_get": "La empresa debe entregarla. Si no la tienes, solicita copia a RRHH por escrito."},
            {"name": "Últimas 12 nóminas", "required": True, "how_to_get": "Solicitar a tu empresa o descargar de tu portal de empleado."},
            {"name": "Contrato de trabajo", "required": True, "how_to_get": "Si no tienes copia, solicitar a la empresa o consultar en el SEPE."},
            {"name": "Informe de vida laboral", "required": True, "how_to_get": "Descargar desde la Sede Electrónica de la Seguridad Social con Cl@ve o certificado digital.", "portal": "seguridad_social"},
            {"name": "Certificado de empresa", "required": False, "how_to_get": "La empresa lo genera para el SEPE. Necesario para solicitar la prestación por desempleo."},
        ],
    },
    "laboral_finiquito": {
        "label": "Finiquito y baja voluntaria",
        "steps": [
            {"step": 1, "title": "Revisar tu contrato", "description": "Comprobar el plazo de preaviso y condiciones de baja voluntaria.", "status": "pending"},
            {"step": 2, "title": "Comunicar la baja por escrito", "description": "Entregar carta de baja voluntaria con el preaviso pactado (habitualmente 15 días).", "status": "pending"},
            {"step": 3, "title": "Calcular el finiquito", "description": "Usar la calculadora para verificar vacaciones no disfrutadas, parte proporcional de pagas y días trabajados.", "status": "pending"},
            {"step": 4, "title": "Revisar y firmar el finiquito", "description": "La empresa debe presentar el finiquito. Puedes firmar 'no conforme' si no estás de acuerdo con los importes.", "status": "pending"},
        ],
        "documents": [
            {"name": "Contrato de trabajo", "required": True, "how_to_get": "Necesario para verificar el plazo de preaviso."},
            {"name": "Últimas nóminas", "required": True, "how_to_get": "Para calcular el finiquito correctamente."},
            {"name": "Carta de baja voluntaria", "required": True, "how_to_get": "Tú la redactas. TramitUp puede generarla por ti."},
        ],
    },
    "vivienda_fianza": {
        "label": "Reclamar fianza de alquiler",
        "steps": [
            {"step": 1, "title": "Recopilar documentación", "description": "Contrato de alquiler, inventario de entrada, fotos del estado del piso, justificantes de pagos.", "status": "pending"},
            {"step": 2, "title": "Esperar plazo legal", "description": "El casero tiene 30 días desde la entrega de llaves para devolver la fianza (art. 36.4 LAU).", "status": "pending"},
            {"step": 3, "title": "Enviar requerimiento al casero", "description": "Si no devuelve en 30 días, enviar burofax reclamando la devolución más intereses.", "status": "pending"},
            {"step": 4, "title": "Reclamar en juzgado (si necesario)", "description": "Si no responde al requerimiento, demanda en Juzgado de Primera Instancia (verbal si <6.000€).", "status": "pending"},
        ],
        "documents": [
            {"name": "Contrato de alquiler", "required": True, "how_to_get": "Tu copia firmada del contrato."},
            {"name": "Inventario de entrada", "required": False, "how_to_get": "Documento firmado al inicio del alquiler con el estado del inmueble."},
            {"name": "Fotos del estado del piso", "required": True, "how_to_get": "Fotos al entrar y al salir del piso. Mejor con fecha visible."},
            {"name": "Justificante de entrega de llaves", "required": True, "how_to_get": "Documento firmado o acta notarial de entrega de llaves."},
            {"name": "Justificantes de pago de la fianza", "required": True, "how_to_get": "Transferencia o recibo del depósito de la fianza."},
        ],
    },
    "vivienda_alquiler": {
        "label": "Problema con el alquiler",
        "steps": [
            {"step": 1, "title": "Identificar el problema", "description": "Cláusulas abusivas, subida ilegal de renta, reparaciones pendientes, problemas con la fianza.", "status": "pending"},
            {"step": 2, "title": "Revisar el contrato", "description": "Analizar las cláusulas del contrato usando el analizador de TramitUp.", "status": "pending"},
            {"step": 3, "title": "Comunicar al arrendador", "description": "Enviar escrito formal (burofax) detallando el problema y la solución que solicitas.", "status": "pending"},
            {"step": 4, "title": "Acudir a organismos de consumo", "description": "Si no hay respuesta, acudir a la Oficina Municipal de Información al Consumidor (OMIC).", "status": "pending"},
        ],
        "documents": [
            {"name": "Contrato de alquiler", "required": True, "how_to_get": "Tu copia firmada del contrato."},
            {"name": "Recibos de pago", "required": True, "how_to_get": "Transferencias o recibos de las mensualidades."},
        ],
    },
    "consumo_aerolinea": {
        "label": "Reclamación a aerolínea",
        "steps": [
            {"step": 1, "title": "Recopilar datos del vuelo", "description": "Número de vuelo, fecha, aerolínea, aeropuertos de origen y destino, horas previstas y reales.", "status": "pending"},
            {"step": 2, "title": "Calcular compensación", "description": "Según el Reglamento UE 261/2004: 250€ (<1.500km), 400€ (1.500-3.500km), 600€ (>3.500km).", "status": "pending"},
            {"step": 3, "title": "Reclamar a la aerolínea", "description": "Enviar reclamación formal al servicio de atención al cliente de la aerolínea.", "status": "pending"},
            {"step": 4, "title": "Reclamar a AESA (si no responde)", "description": "Si la aerolínea no responde en 30 días o deniega, reclamar ante la Agencia Estatal de Seguridad Aérea.", "status": "pending"},
            {"step": 5, "title": "Vía judicial (si necesario)", "description": "Si AESA no resuelve, demanda en juzgado (verbal si <6.000€, no necesitas abogado).", "status": "pending"},
        ],
        "documents": [
            {"name": "Tarjeta de embarque / reserva", "required": True, "how_to_get": "Email de confirmación de la aerolínea o plataforma de reserva."},
            {"name": "Comunicaciones de la aerolínea", "required": True, "how_to_get": "Emails o SMS sobre cancelación, retraso o cambio de vuelo."},
            {"name": "Gastos adicionales", "required": False, "how_to_get": "Facturas de hotel, comida, transporte alternativo si los hubo."},
        ],
    },
    "consumo_factura": {
        "label": "Reclamar factura incorrecta",
        "steps": [
            {"step": 1, "title": "Identificar el problema", "description": "Revisar la factura y comparar con el consumo real, tarifas contratadas y conceptos facturados.", "status": "pending"},
            {"step": 2, "title": "Reclamar a la empresa", "description": "Contactar con atención al cliente y presentar reclamación formal. Pedir número de referencia.", "status": "pending"},
            {"step": 3, "title": "Presentar hoja de reclamaciones", "description": "Si no hay solución en 30 días, solicitar hoja de reclamaciones oficial.", "status": "pending"},
            {"step": 4, "title": "Acudir a organismos de consumo", "description": "Presentar reclamación ante la OMIC o Junta Arbitral de Consumo.", "status": "pending"},
        ],
        "documents": [
            {"name": "Factura reclamada", "required": True, "how_to_get": "Copia de la factura que quieres reclamar."},
            {"name": "Contrato del servicio", "required": True, "how_to_get": "Contrato o condiciones del servicio contratado."},
            {"name": "Lecturas del contador", "required": False, "how_to_get": "Fotos o registros de lectura del contador."},
        ],
    },
    "trafico_multa": {
        "label": "Recurrir multa de tráfico",
        "steps": [
            {"step": 1, "title": "Analizar la multa", "description": "Revisar la notificación: infracción, fecha, lugar, importe, plazo para alegar.", "status": "pending"},
            {"step": 2, "title": "Reunir pruebas", "description": "Fotos de señalización, testigos, documentación del vehículo, trayecto GPS.", "status": "pending"},
            {"step": 3, "title": "Presentar alegaciones", "description": "Plazo de 20 días naturales desde la notificación. Enviar escrito de alegaciones al organismo sancionador.", "status": "pending"},
            {"step": 4, "title": "Recurso de reposición (si desestiman)", "description": "Si desestiman las alegaciones, recurso de reposición en 1 mes o recurso contencioso-administrativo en 2 meses.", "status": "pending"},
        ],
        "documents": [
            {"name": "Notificación de la multa", "required": True, "how_to_get": "La notificación oficial recibida por correo o en la Sede Electrónica de la DGT."},
            {"name": "Fotos de señalización", "required": False, "how_to_get": "Fotos del lugar donde se cometió la supuesta infracción."},
            {"name": "Permiso de conducir", "required": False, "how_to_get": "Puede ser necesario si se recurre la identidad del conductor."},
        ],
    },
    "fiscal_renta": {
        "label": "Declaración de la Renta",
        "steps": [
            {"step": 1, "title": "Obtener datos fiscales", "description": "Descargar los datos fiscales desde la Sede Electrónica de la Agencia Tributaria.", "status": "pending"},
            {"step": 2, "title": "Revisar el borrador", "description": "Comprobar que todos los ingresos, deducciones y circunstancias personales son correctos.", "status": "pending"},
            {"step": 3, "title": "Aplicar deducciones", "description": "Verificar deducciones aplicables: vivienda, donaciones, inversión, maternidad/paternidad.", "status": "pending"},
            {"step": 4, "title": "Presentar la declaración", "description": "Confirmar y presentar a través de Renta WEB o la app de la AEAT.", "status": "pending"},
        ],
        "documents": [
            {"name": "Datos fiscales (certificado AEAT)", "required": True, "how_to_get": "Descargar desde la Sede Electrónica de la AEAT con Cl@ve o certificado digital.", "portal": "agencia_tributaria"},
            {"name": "Certificados de retenciones", "required": True, "how_to_get": "Tu empresa debe facilitarlos. También aparecen en los datos fiscales."},
            {"name": "Recibos de hipoteca/alquiler", "required": False, "how_to_get": "Si tienes derecho a deducción por vivienda habitual."},
        ],
    },
}

# ── Categoría genérica (para categorías sin template específico) ──────────────
GENERIC_WORKFLOW = {
    "steps": [
        {"step": 1, "title": "Identificar el problema", "description": "Define claramente qué ha pasado y qué quieres conseguir.", "status": "pending"},
        {"step": 2, "title": "Recopilar documentación", "description": "Reúne todos los documentos relacionados con tu caso.", "status": "pending"},
        {"step": 3, "title": "Consultar al asistente", "description": "Pregunta a TramitUp sobre tus derechos y opciones.", "status": "pending"},
        {"step": 4, "title": "Tomar acción", "description": "Sigue los pasos recomendados por el asistente.", "status": "pending"},
    ],
    "documents": [],
}


def get_workflow_template(category: str, subcategory: str | None = None) -> dict[str, Any]:
    """Busca el template de workflow más específico disponible."""
    if subcategory:
        key = f"{category}_{subcategory}"
        if key in WORKFLOW_TEMPLATES:
            return WORKFLOW_TEMPLATES[key]

    # Buscar por categoría con cualquier subcategoría
    for template_key, template in WORKFLOW_TEMPLATES.items():
        if template_key.startswith(f"{category}_"):
            return template

    return GENERIC_WORKFLOW


def get_all_template_ids() -> list[str]:
    """Lista todos los IDs de templates disponibles."""
    return list(WORKFLOW_TEMPLATES.keys())
