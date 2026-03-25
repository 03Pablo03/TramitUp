"""
TramitUp Marketing — Configuracion central compartida por todos los bots.
"""

# ─── Marca ────────────────────────────────────────────────────────────────────

BRAND = {
    "name": "TramitUp",
    "tagline": "Tu asistente legal de bolsillo",
    "url": "https://tramitup.es",
    "tiktok": "@tramitup",
    "facebook": "TramitUp",
    "emoji_flag": "🇪🇸",
}

# ─── Voz de marca ─────────────────────────────────────────────────────────────

VOICE = {
    "tone": "cercano, directo, educativo",
    "persona": "Un amigo que sabe de leyes y te lo explica facil",
    "prohibido": [
        "jerga legal innecesaria",
        "tono condescendiente",
        "vender directamente la app",
        "prometer resultados legales concretos",
    ],
    "siempre": [
        "dar valor primero",
        "usar ejemplos reales y cotidianos",
        "incluir dato concreto (cifra, plazo, ley)",
        "CTA sutil al final (link en bio)",
    ],
}

# ─── Publico objetivo ─────────────────────────────────────────────────────────

AUDIENCE = {
    "edad": "25-55",
    "pais": "España",
    "pain_points": [
        "multas de trafico",
        "problemas con caseros/alquileres",
        "herencias y sucesiones",
        "reclamaciones a empresas",
        "tramites burocraticos",
        "facturas incorrectas",
        "despidos y derechos laborales",
        "vuelos cancelados/retrasados",
        "devoluciones de compras",
        "seguridad social y prestaciones",
    ],
}

# ─── Embudo de conversion ─────────────────────────────────────────────────────

FUNNEL = {
    "steps": [
        "Video viral / post util",
        "Perfil de TramitUp",
        "Link en bio",
        "Registro con trial gratuito 3 dias",
        "Conversion a Pro",
    ],
    "trial_days": 3,
    "price": "9,99 €/mes",
}

# ─── CTAs aprobados ───────────────────────────────────────────────────────────

CTAS = {
    "tiktok": [
        "Si quieres saber mas sobre tus derechos, tengo algo en mi bio que te va a ayudar mucho.",
        "Sigueme para mas derechos que no conocias.",
        "En mi bio tienes TramitUp, tu asistente legal gratuito. Sigueme para mas.",
        "Si tienes un problema asi y no sabes que hacer, en mi bio hay una app que te explica todos tus derechos gratis.",
        "Guarda este video por si lo necesitas. Link en bio.",
        "Comenta tu caso y te respondo con un video.",
    ],
    "facebook": [
        "¿Te ha pasado algo asi? Cuentanos en los comentarios.",
        "Si quieres saber mas, en nuestra bio tienes un asistente que te lo explica paso a paso.",
        "Comparte con alguien que necesite saber esto.",
        "¿Quieres que hagamos un post detallado sobre este tema? Dejanos un comentario.",
    ],
}

# ─── Hashtags ─────────────────────────────────────────────────────────────────

HASHTAGS = {
    "tiktok": {
        "core": ["#tramitup", "#derechosespaña", "#leyesquenoconocias", "#aprendeentiktok"],
        "reach": ["#datoscuriosos", "#españa", "#viral", "#parati", "#fyp"],
        "topics": {
            "multas": ["#multas", "#multadetrafico", "#dgt", "#trafico"],
            "alquiler": ["#derechosinquilinos", "#alquiler", "#inquilinos", "#casero"],
            "laboral": ["#derechoslaborales", "#despido", "#trabajo", "#autonomos"],
            "consumo": ["#consumidores", "#reclamacion", "#devolucion"],
            "herencias": ["#herencia", "#herencias", "#sucesiones"],
            "vuelos": ["#vueloscancelados", "#reclamarvuelo", "#aerolineas"],
            "tramites": ["#tramites", "#burocracia", "#administracion"],
        },
    },
    "facebook": {
        "core": ["#tramitup", "#asistentejuridico", "#derechos", "#leyes"],
        "topics": {
            "alquiler": ["#inquilinos", "#alquiler", "#vivienda"],
            "consumo": ["#consumidores", "#reclamaciones"],
            "tramites": ["#tramites", "#españa"],
            "laboral": ["#trabajo", "#despido", "#autonomos"],
        },
    },
}

# ─── Horarios optimos ─────────────────────────────────────────────────────────

SCHEDULE = {
    "tiktok": {
        "frequency": "3-4 videos/semana",
        "best_hours": ["12:00-14:00", "19:00-21:00"],
        "best_days": ["martes", "jueves", "sabado"],
    },
    "facebook": {
        "page_frequency": "3-4 posts/semana",
        "group_frequency": "1-2 participaciones/semana",
        "best_hours": ["10:00-12:00", "18:00-20:00"],
    },
}

# ─── KPIs ─────────────────────────────────────────────────────────────────────

KPIS = {
    "mes_1": {
        "seguidores_tiktok": (500, 1000),
        "views_por_video": (1000, 5000),
        "seguidores_facebook": (200, 500),
        "registros_app": (50, 100),
        "conversion_trial": (0.05, 0.10),
    },
    "mes_3": {
        "seguidores_tiktok": (3000, 5000),
        "views_por_video": (5000, 20000),
        "seguidores_facebook": (1000, 2000),
        "registros_app": (200, 500),
        "conversion_trial": (0.10, 0.15),
    },
}

# ─── Formatos de contenido ────────────────────────────────────────────────────

TIKTOK_FORMATS = [
    "mito_vs_realidad",
    "top_3_listicle",
    "tutorial_rapido",
    "pov_storytelling",
    "pregunta_gancho",
    "revelacion",
    "pregunta_viral",
    "demo_app",
    "listicle_valor",
    "consecuencias",
    "storytime",
    "datos_reales",
]

FACEBOOK_FORMATS = [
    "carrusel_informativo",
    "post_de_valor",
    "pregunta_engagement",
    "caso_real",
    "infografia",
    "demo_tutorial",
    "testimonio",
    "post_educativo",
]

# ─── Temas de contenido con datos legales reales ──────────────────────────────

CONTENT_BANK = [
    {
        "topic": "multas",
        "hooks": [
            "Si te han puesto una multa de trafico, NO la pagues todavia.",
            "¿Sabias que puedes pagar la mitad de cualquier multa?",
            "¿Que pasa si no pagas una multa? Te lo explico.",
        ],
        "facts": [
            "20 dias naturales para pagar con 50% descuento (art. 94 LTSV)",
            "Si pagas con descuento renuncias a recurrir",
            "Plazo para recurrir: 20 dias habiles desde notificacion",
            "Si no pagas: recargo del 5%, 10%, 20% segun plazo",
            "Ultimo paso: embargo de cuentas/nomina",
        ],
    },
    {
        "topic": "alquiler",
        "hooks": [
            "Si vives de alquiler, tu casero NO puede hacer estas 3 cosas.",
            "¿Tu casero quiere subir el alquiler? Esto es lo que dice la ley.",
            "¿Te pueden echar de tu piso si no pagas un mes?",
        ],
        "facts": [
            "El casero NO puede entrar sin permiso (art. 18 CE, inviolabilidad domicilio)",
            "Subida regulada por indice de referencia (LAU art. 18)",
            "Fianza: solo se retiene por daños reales, no desgaste normal",
            "Contrato minimo 5 años (persona fisica) o 7 (empresa) - LAU 2019",
            "Desahucio express: proceso judicial necesario, no puede echarte sin orden",
        ],
    },
    {
        "topic": "consumo",
        "hooks": [
            "¿Te han cobrado de mas en una factura? Esto es lo que tienes que hacer.",
            "14 dias para devolver CUALQUIER compra online sin dar explicaciones.",
            "Las empresas ODIAN que hagas esto cuando reclamas.",
        ],
        "facts": [
            "Derecho de desistimiento: 14 dias en compras online (RD 1/2007)",
            "Hoja de reclamaciones: obligatorio tenerla en todo local",
            "OMIC: servicio gratuito de mediacion del ayuntamiento",
            "Plazo reclamacion consumo: 3 años generalmente",
            "Si no responden en 30 dias: puedes escalar a consumo",
        ],
    },
    {
        "topic": "herencias",
        "hooks": [
            "Lo que NADIE te cuenta cuando heredas una casa.",
            "¿Cuanto cuesta REALMENTE heredar en España?",
            "Heredar puede arruinarte si no haces esto.",
        ],
        "facts": [
            "Plazo para aceptar/renunciar: no hay plazo legal fijo, pero 30 dias para impuesto",
            "Impuesto de sucesiones: varia MUCHO por comunidad autonoma",
            "Puedes aceptar a beneficio de inventario (no heredas deudas)",
            "Plusvalia municipal: hay que pagarla al heredar inmueble",
            "Renuncia de herencia: ante notario, irrevocable",
        ],
    },
    {
        "topic": "laboral",
        "hooks": [
            "Te despiden, ¿que haces? Los primeros 20 dias son CLAVE.",
            "Tu jefe no puede hacerte esto (y mucha gente no lo sabe).",
            "¿Te deben vacaciones? Calcula cuanto te corresponde.",
        ],
        "facts": [
            "Plazo para demandar por despido: 20 dias habiles",
            "Despido improcedente: 33 dias por año trabajado",
            "Periodo de prueba maximo: 6 meses (titulados), 2 meses (general)",
            "Vacaciones: 30 dias naturales minimo por año (art. 38 ET)",
            "Finiquito: derecho a recibirlo SIEMPRE al acabar relacion laboral",
        ],
    },
    {
        "topic": "vuelos",
        "hooks": [
            "Tu vuelo se retrasa mas de 3 horas. La aerolinea te debe dinero.",
            "POV: Descubres que puedes reclamar un vuelo de hace 3 años.",
            "Las aerolineas no quieren que sepas esto.",
        ],
        "facts": [
            "Compensacion por retraso >3h: 250-600€ segun distancia (Reg. CE 261/2004)",
            "Plazo reclamacion: hasta 5 años en España",
            "Cancelacion con menos de 14 dias: compensacion obligatoria",
            "Overbooking: compensacion + alternativa de vuelo",
            "La aerolinea NO puede alegar 'causas meteorologicas' siempre",
        ],
    },
    {
        "topic": "tramites",
        "hooks": [
            "5 tramites que puedes hacer GRATIS y no lo sabias.",
            "El tramite mas util que nadie conoce.",
            "Ahorra 200€ haciendo tu mismo este tramite.",
        ],
        "facts": [
            "Vida laboral: gratis en sede electronica Seguridad Social",
            "Certificado de antecedentes penales: gratis online",
            "Empadronamiento: gratis en tu ayuntamiento",
            "Recurso de reposicion a Hacienda: gratis, sin abogado",
            "Reclamacion a Seguridad Social: gratis, plazo 30 dias",
        ],
    },
]
