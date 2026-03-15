"""
Prompt para extraer datos de la conversación y preparar el modelo de escrito.
"""

EXTRACT_DATA_PROMPT = """
Analiza la siguiente conversación entre un usuario y Tramitup.
Extrae todos los datos relevantes para generar un modelo de escrito.

Devuelve ÚNICAMENTE un JSON válido con esta estructura:

{{
  "document_type": "string (tipo de documento: reclamacion_aerolinea, reclamacion_fianza, etc)",
  "remitente": {{
    "nombre": "string | null",
    "dni_nie": "string | null",
    "direccion": "string | null",
    "email": "string | null",
    "telefono": "string | null"
  }},
  "destinatario": {{
    "nombre_empresa": "string | null",
    "departamento": "string | null",
    "direccion": "string | null"
  }},
  "hechos": ["string"],
  "datos_especificos": {{}},
  "normativa_aplicable": ["string"],
  "peticion": "string | null",
  "lugar_fecha": {{
    "lugar": "string | null",
    "fecha": "string (formato: Valencia, a 26 de febrero de 2026)"
  }},
  "datos_faltantes": ["string"]
}}

Tipos de documento soportados:
- reclamacion_aerolinea, reclamacion_banco, reclamacion_seguro, reclamacion_suministro_luz,
- reclamacion_suministro_internet, reclamacion_comercio, recurso_multa_trafico
- carta_disconformidad_finiquito, solicitud_certificado_empresa, reclamacion_salarios, solicitud_prestacion_desempleo
- reclamacion_fianza, burofax_arrendador, solicitud_informacion_comunidad, impugnacion_acuerdo_junta
- recurso_reposicion_hacienda, solicitud_aplazamiento_hacienda, reclamacion_seguridad_social, solicitud_informacion_administrativa

Usa la fecha actual para lugar_fecha.fecha. Si no hay lugar, usa "A" seguido de la fecha.
En datos_especificos incluye campos según el tipo: numero_vuelo, fecha_vuelo, importe_reclamado, etc.

Conversación:
{conversation}
"""
