"""
Mapeo de tipos de documento a normativa base.
"""

DOCUMENT_TEMPLATES = {
    "reclamacion_aerolinea": {
        "normativa": "Reglamento (CE) 261/2004, compensación por retrasos/cancelaciones",
        "destinatario_default": "Servicio de Atención al Cliente",
    },
    "reclamacion_banco": {
        "normativa": "Ley 7/1998, Ley 16/2011, Banco de España",
        "destinatario_default": "Servicio de Reclamaciones",
    },
    "reclamacion_seguro": {
        "normativa": "Ley 50/1980 de Contrato de Seguro",
        "destinatario_default": "Servicio de Reclamaciones",
    },
    "reclamacion_suministro_luz": {
        "normativa": "Ley 24/2013 sector eléctrico, RD 1955/2000",
        "destinatario_default": "Servicio de Atención al Cliente",
    },
    "reclamacion_suministro_internet": {
        "normativa": "Ley 9/2014 telecomunicaciones",
        "destinatario_default": "Servicio de Atención al Cliente",
    },
    "reclamacion_comercio": {
        "normativa": "RDL 1/2007 LGDCU",
        "destinatario_default": "Servicio de Atención al Cliente",
    },
    "recurso_multa_trafico": {
        "normativa": "RDL 6/2015 LSV",
        "destinatario_default": "Jefatura Provincial de Tráfico",
    },
    "carta_disconformidad_finiquito": {
        "normativa": "RDL 2/2015 Estatuto de los Trabajadores",
        "destinatario_default": "Departamento de Recursos Humanos",
    },
    "solicitud_certificado_empresa": {
        "normativa": "RDL 2/2015 ET",
        "destinatario_default": "Departamento de RRHH",
    },
    "reclamacion_salarios": {
        "normativa": "RDL 2/2015 ET",
        "destinatario_default": "Departamento de RRHH",
    },
    "solicitud_prestacion_desempleo": {
        "normativa": "RDL 8/2015 LGSS",
        "destinatario_default": "SEPE",
    },
    "reclamacion_fianza": {
        "normativa": "LAU 29/1994",
        "destinatario_default": "Arrendador",
    },
    "burofax_arrendador": {
        "normativa": "LAU 29/1994",
        "destinatario_default": "Arrendador",
    },
    "solicitud_informacion_comunidad": {
        "normativa": "LPH 49/1960",
        "destinatario_default": "Administrador de fincas",
    },
    "impugnacion_acuerdo_junta": {
        "normativa": "LPH 49/1960",
        "destinatario_default": "Comunidad de propietarios",
    },
    "recurso_reposicion_hacienda": {
        "normativa": "Ley 58/2003 LGT",
        "destinatario_default": "AEAT",
    },
    "solicitud_aplazamiento_hacienda": {
        "normativa": "Ley 58/2003 LGT",
        "destinatario_default": "AEAT",
    },
    "reclamacion_seguridad_social": {
        "normativa": "RDL 8/2015 LGSS",
        "destinatario_default": "INSS / TGSS",
    },
    "solicitud_informacion_administrativa": {
        "normativa": "Ley 39/2015 PAC",
        "destinatario_default": "Registro del organismo",
    },
}
