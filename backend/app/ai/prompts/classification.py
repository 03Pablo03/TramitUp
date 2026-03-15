"""
Prompt para clasificar el trámite desde texto libre del usuario.
Rápido y conciso (< 1 segundo).
"""

CLASSIFICATION_PROMPT = """Analiza el mensaje del usuario sobre su situación legal/burocrática en España.
Devuelve ÚNICAMENTE un JSON válido (sin texto adicional):

{
  "category": "reclamaciones" | "laboral" | "vivienda" | "burocracia_general" | "otro",
  "subcategory": "string corta: aerolinea, finiquito, alquiler, hacienda...",
  "urgency": "alta" | "media" | "baja",
  "keywords": ["lista", "de", "términos", "clave"],
  "needs_more_info": true | false,
  "titulo_resumen": "string breve < 60 caracteres"
}

Categorías: reclamaciones (aerolíneas, bancos, suministros, comercio), laboral (paro, finiquito, despido, bajas), vivienda (alquiler, hipotecas, comunidad), burocracia_general (hacienda, SS, ayuntamiento).

needs_more_info: true si faltan datos relevantes para dar una guía completa.

Mensaje:
{text}
"""
