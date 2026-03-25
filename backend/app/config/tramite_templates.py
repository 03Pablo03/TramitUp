"""
Plantillas de trámites guiados paso a paso.
Cada template define un flujo completo con formularios, análisis IA y generación de documentos.
"""

TRAMITE_TEMPLATES = {
    "reclamar_vuelo": {
        "id": "reclamar_vuelo",
        "title": "Reclamar vuelo cancelado o retrasado",
        "description": "Obtén la compensación que te corresponde según el Reglamento UE 261/2004.",
        "icon": "✈️",
        "category": "consumo",
        "subcategory": "aerolinea",
        "estimated_time": "10-15 minutos",
        "steps": [
            {
                "id": "datos_vuelo",
                "title": "Datos del vuelo",
                "type": "form",
                "fields": [
                    {"name": "airline", "label": "Aerolínea", "type": "text", "required": True, "placeholder": "Ej: Ryanair, Iberia, Vueling..."},
                    {"name": "flight_number", "label": "Número de vuelo", "type": "text", "required": False, "placeholder": "Ej: FR1234"},
                    {"name": "flight_date", "label": "Fecha del vuelo", "type": "date", "required": True},
                    {"name": "origin", "label": "Aeropuerto de origen", "type": "text", "required": True, "placeholder": "Ej: Madrid-Barajas"},
                    {"name": "destination", "label": "Aeropuerto de destino", "type": "text", "required": True, "placeholder": "Ej: Londres-Gatwick"},
                    {"name": "issue_type", "label": "¿Qué pasó?", "type": "select", "required": True, "options": ["Cancelación", "Retraso de más de 3 horas", "Denegación de embarque (overbooking)", "Pérdida de equipaje"]},
                    {"name": "delay_hours", "label": "Horas de retraso (si aplica)", "type": "number", "required": False, "placeholder": "Ej: 4"},
                    {"name": "advance_notice", "label": "¿Con cuánta antelación te avisaron?", "type": "select", "required": False, "options": ["No me avisaron", "Menos de 7 días", "Entre 7 y 14 días", "Más de 14 días"]},
                ],
            },
            {
                "id": "analisis",
                "title": "Análisis de tu caso",
                "type": "ai_analysis",
                "prompt_context": "Analiza este caso de reclamación aérea y calcula la compensación según el Reglamento UE 261/2004.",
            },
            {
                "id": "generar_reclamacion",
                "title": "Generar carta de reclamación",
                "type": "document_generation",
                "description": "Generaremos una carta formal de reclamación dirigida a la aerolínea.",
            },
            {
                "id": "enviar",
                "title": "Cómo enviar tu reclamación",
                "type": "instructions",
                "content": "1. Envía la carta generada al servicio de atención al cliente de la aerolínea (email o formulario web).\n2. Guarda el número de referencia de la reclamación.\n3. Si no te responden en 30 días o deniegan tu reclamación, puedes reclamar ante AESA (Agencia Estatal de Seguridad Aérea).\n4. Como último recurso, demanda en juzgado (verbal si <6.000€, no necesitas abogado ni procurador).",
            },
            {
                "id": "seguimiento",
                "title": "Seguimiento",
                "type": "follow_up",
                "auto_alert_days": 30,
                "auto_alert_description": "Plazo de respuesta de la aerolínea a tu reclamación",
            },
        ],
    },
    "despido_improcedente": {
        "id": "despido_improcedente",
        "title": "Gestionar un despido",
        "description": "Verifica tus derechos, calcula tu indemnización y actúa dentro de los plazos legales.",
        "icon": "💼",
        "category": "laboral",
        "subcategory": "despido",
        "estimated_time": "15-20 minutos",
        "steps": [
            {
                "id": "datos_despido",
                "title": "Datos de tu situación laboral",
                "type": "form",
                "fields": [
                    {"name": "company_name", "label": "Nombre de la empresa", "type": "text", "required": True},
                    {"name": "hire_date", "label": "Fecha de inicio del contrato", "type": "date", "required": True},
                    {"name": "fire_date", "label": "Fecha de despido (o de la carta)", "type": "date", "required": True},
                    {"name": "contract_type", "label": "Tipo de contrato", "type": "select", "required": True, "options": ["Indefinido", "Temporal", "De obra o servicio", "Interino", "No lo sé"]},
                    {"name": "gross_salary", "label": "Salario bruto anual (€)", "type": "number", "required": True, "placeholder": "Ej: 24000"},
                    {"name": "dismissal_type", "label": "Tipo de despido comunicado", "type": "select", "required": True, "options": ["Despido disciplinario", "Despido objetivo", "ERE/ERTE", "No me lo han dicho", "Fin de contrato temporal"]},
                    {"name": "has_letter", "label": "¿Te han dado carta de despido?", "type": "select", "required": True, "options": ["Sí", "No"]},
                    {"name": "paid_compensation", "label": "¿Te han ofrecido indemnización?", "type": "select", "required": True, "options": ["Sí", "No", "Aún no lo sé"]},
                ],
            },
            {
                "id": "analisis",
                "title": "Análisis y cálculo de indemnización",
                "type": "ai_analysis",
                "prompt_context": "Analiza este caso de despido según el Estatuto de los Trabajadores y calcula la indemnización correspondiente.",
            },
            {
                "id": "generar_papeleta",
                "title": "Generar modelo de papeleta SMAC",
                "type": "document_generation",
                "description": "Generaremos el modelo de papeleta de conciliación para presentar en el SMAC.",
            },
            {
                "id": "pasos_siguientes",
                "title": "Pasos siguientes",
                "type": "instructions",
                "content": "1. Presenta la papeleta de conciliación en el SMAC de tu comunidad autónoma en los próximos 20 días hábiles.\n2. Solicita la prestación por desempleo en el SEPE (plazo de 15 días hábiles desde el despido).\n3. Asiste al acto de conciliación cuando te citen.\n4. Si no hay acuerdo, valora presentar demanda en el Juzgado de lo Social.",
            },
            {
                "id": "seguimiento",
                "title": "Seguimiento de plazos",
                "type": "follow_up",
                "auto_alert_days": 20,
                "auto_alert_description": "Plazo para presentar papeleta SMAC (20 días hábiles desde despido)",
            },
        ],
    },
    "reclamar_fianza": {
        "id": "reclamar_fianza",
        "title": "Reclamar la fianza del alquiler",
        "description": "Recupera tu fianza si el casero no la devuelve en el plazo legal de 30 días.",
        "icon": "🏠",
        "category": "vivienda",
        "subcategory": "fianza",
        "estimated_time": "10-15 minutos",
        "steps": [
            {
                "id": "datos_alquiler",
                "title": "Datos del alquiler",
                "type": "form",
                "fields": [
                    {"name": "landlord_name", "label": "Nombre del arrendador", "type": "text", "required": True},
                    {"name": "property_address", "label": "Dirección del inmueble", "type": "text", "required": True},
                    {"name": "deposit_amount", "label": "Importe de la fianza (€)", "type": "number", "required": True, "placeholder": "Ej: 800"},
                    {"name": "key_delivery_date", "label": "Fecha de entrega de llaves", "type": "date", "required": True},
                    {"name": "contract_start", "label": "Fecha de inicio del contrato", "type": "date", "required": True},
                    {"name": "has_inventory", "label": "¿Se hizo inventario al entrar?", "type": "select", "required": True, "options": ["Sí", "No", "No estoy seguro"]},
                    {"name": "property_condition", "label": "Estado del piso al dejarlo", "type": "select", "required": True, "options": ["Buen estado (desgaste normal)", "Hice mejoras", "Hay algunos desperfectos", "Mal estado"]},
                    {"name": "landlord_excuse", "label": "¿Qué dice el casero?", "type": "select", "required": False, "options": ["No contesta", "Dice que hay desperfectos", "Quiere descontar importes", "Dice que no tiene dinero"]},
                ],
            },
            {
                "id": "analisis",
                "title": "Análisis de tu caso",
                "type": "ai_analysis",
                "prompt_context": "Analiza este caso de devolución de fianza según la LAU (art. 36.4) y normativa autonómica.",
            },
            {
                "id": "generar_burofax",
                "title": "Generar requerimiento al casero",
                "type": "document_generation",
                "description": "Generaremos un requerimiento formal para enviar al arrendador.",
            },
            {
                "id": "enviar",
                "title": "Cómo enviar el requerimiento",
                "type": "instructions",
                "content": "1. Envía el requerimiento por burofax con acuse de recibo y certificación de contenido.\n2. Guarda la copia del burofax y el justificante de envío.\n3. Si no responde en 30 días, puedes interponer demanda verbal en el Juzgado de Primera Instancia (si el importe es <6.000€ no necesitas abogado ni procurador).\n4. Puedes reclamar la fianza + intereses legales desde el día 31 tras la entrega de llaves.",
            },
        ],
    },
    "recurrir_multa": {
        "id": "recurrir_multa",
        "title": "Recurrir multa de tráfico",
        "description": "Presenta alegaciones si crees que la multa es incorrecta o desproporcionada.",
        "icon": "🚗",
        "category": "trafico",
        "subcategory": "multa",
        "estimated_time": "10 minutos",
        "steps": [
            {
                "id": "datos_multa",
                "title": "Datos de la multa",
                "type": "form",
                "fields": [
                    {"name": "fine_number", "label": "Número de expediente", "type": "text", "required": False, "placeholder": "Aparece en la notificación"},
                    {"name": "fine_date", "label": "Fecha de la infracción", "type": "date", "required": True},
                    {"name": "notification_date", "label": "Fecha de la notificación", "type": "date", "required": True},
                    {"name": "fine_amount", "label": "Importe de la multa (€)", "type": "number", "required": True},
                    {"name": "points", "label": "Puntos que retiran", "type": "number", "required": False},
                    {"name": "infraction_type", "label": "Tipo de infracción", "type": "select", "required": True, "options": ["Exceso de velocidad", "Semáforo en rojo", "Estacionamiento indebido", "Uso del móvil", "No llevar cinturón", "ITV caducada", "Otra"]},
                    {"name": "reason_to_appeal", "label": "¿Por qué quieres recurrir?", "type": "select", "required": True, "options": ["No fui yo quien conducía", "La señalización es incorrecta", "Error en los datos de la multa", "El radar no estaba calibrado", "Había una causa justificada", "Otra razón"]},
                    {"name": "issuing_body", "label": "Organismo sancionador", "type": "select", "required": True, "options": ["DGT", "Ayuntamiento", "Policía autonómica", "No lo sé"]},
                ],
            },
            {
                "id": "analisis",
                "title": "Análisis de viabilidad",
                "type": "ai_analysis",
                "prompt_context": "Analiza la viabilidad de recurrir esta multa según la Ley de Tráfico y normativa vigente.",
            },
            {
                "id": "generar_alegacion",
                "title": "Generar escrito de alegaciones",
                "type": "document_generation",
                "description": "Generaremos el escrito de alegaciones adaptado a tu caso.",
            },
            {
                "id": "enviar",
                "title": "Cómo presentar las alegaciones",
                "type": "instructions",
                "content": "1. Tienes 20 días naturales desde la notificación para presentar alegaciones.\n2. Presenta el escrito en la Sede Electrónica de la DGT (si es DGT), en el registro del ayuntamiento (si es municipal), o por correo certificado.\n3. Si te desestiman las alegaciones, puedes presentar recurso de reposición (1 mes) o recurso contencioso-administrativo (2 meses).\n4. IMPORTANTE: Si pagas con reducción del 50% en 20 días, pierdes el derecho a recurrir.",
            },
        ],
    },
    "reclamar_factura": {
        "id": "reclamar_factura",
        "title": "Reclamar factura incorrecta",
        "description": "Reclama cobros indebidos a tu compañía de luz, gas, teléfono u otros servicios.",
        "icon": "💡",
        "category": "consumo",
        "subcategory": "factura",
        "estimated_time": "10 minutos",
        "steps": [
            {
                "id": "datos_factura",
                "title": "Datos de la factura",
                "type": "form",
                "fields": [
                    {"name": "company", "label": "Empresa", "type": "text", "required": True, "placeholder": "Ej: Endesa, Vodafone, Naturgy..."},
                    {"name": "service_type", "label": "Tipo de servicio", "type": "select", "required": True, "options": ["Electricidad", "Gas", "Telefonía/Internet", "Agua", "Seguro", "Otro"]},
                    {"name": "invoice_date", "label": "Fecha de la factura", "type": "date", "required": True},
                    {"name": "invoice_amount", "label": "Importe facturado (€)", "type": "number", "required": True},
                    {"name": "expected_amount", "label": "Importe que consideras correcto (€)", "type": "number", "required": False},
                    {"name": "issue", "label": "¿Cuál es el problema?", "type": "select", "required": True, "options": ["Cobro de servicio no contratado", "Importe muy superior al habitual", "Cobro tras dar de baja", "Doble facturación", "Error en lectura de contador", "Penalización indebida", "Otro"]},
                    {"name": "contacted_company", "label": "¿Has contactado con la empresa?", "type": "select", "required": True, "options": ["No", "Sí, pero no me solucionan", "Sí, me dijeron que era correcto"]},
                ],
            },
            {
                "id": "analisis",
                "title": "Análisis de tu reclamación",
                "type": "ai_analysis",
                "prompt_context": "Analiza esta reclamación de factura según la normativa de consumo española.",
            },
            {
                "id": "generar_reclamacion",
                "title": "Generar reclamación formal",
                "type": "document_generation",
                "description": "Generaremos una reclamación formal dirigida a la empresa.",
            },
            {
                "id": "enviar",
                "title": "Cómo proceder",
                "type": "instructions",
                "content": "1. Envía la reclamación al servicio de atención al cliente de la empresa.\n2. Si no resuelven en 30 días, solicita la hoja de reclamaciones oficial.\n3. Puedes acudir a la OMIC (Oficina Municipal de Información al Consumidor) de tu ayuntamiento.\n4. Para servicios de telecomunicaciones, puedes reclamar ante la Secretaría de Estado de Telecomunicaciones.\n5. Para energía, puedes contactar con la CNMC (Comisión Nacional de los Mercados y la Competencia).",
            },
        ],
    },
}


def get_tramite_template(template_id: str) -> dict | None:
    """Retorna un template de trámite por su ID."""
    return TRAMITE_TEMPLATES.get(template_id)


def list_tramite_templates() -> list[dict]:
    """Lista todos los templates disponibles (sin los steps detallados)."""
    return [
        {
            "id": t["id"],
            "title": t["title"],
            "description": t["description"],
            "icon": t["icon"],
            "category": t["category"],
            "estimated_time": t["estimated_time"],
        }
        for t in TRAMITE_TEMPLATES.values()
    ]
