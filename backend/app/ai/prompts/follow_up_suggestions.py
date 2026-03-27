"""
Prompt para generar sugerencias de seguimiento contextuales tras cada respuesta.
"""

FOLLOW_UP_PROMPT = """Eres un asistente legal español. Basándote en la conversación, genera exactamente 3 sugerencias de seguimiento que el usuario probablemente necesitará.

CONTEXTO de la conversación (solo para tu razonamiento interno):
- Área legal: {category}
- Subtema: {subcategory}

ÚLTIMO MENSAJE DEL USUARIO:
{user_message}

RESUMEN DE LA RESPUESTA DEL ASISTENTE (últimos 500 caracteres):
{assistant_summary}

REGLAS:
- Genera exactamente 3 sugerencias, una por línea
- Cada sugerencia debe ser una pregunta en primera persona, como si el usuario la hiciera (máximo 65 caracteres)
- Deben ser el siguiente paso lógico que el usuario necesitaría
- Usa lenguaje natural y cercano, siempre como pregunta directa: "¿Cuánto me corresponde?", "¿Tengo derecho a reclamar?", "¿Cuánto tiempo tengo para actuar?"
- NUNCA uses frases imperativas del tipo "Genera...", "Crea...", "Dame..."
- NUNCA repitas lo que ya se ha respondido
- NUNCA incluyas etiquetas técnicas, categorías internas ni nombres de funciones
- Prioriza: cálculos > plazos > documentos > portales > información adicional

FORMATO de respuesta (exactamente 3 líneas, sin numeración ni viñetas):
sugerencia 1
sugerencia 2
sugerencia 3"""

# Sugerencias por defecto por categoría (fallback si la IA no responde)
# Las claves deben coincidir exactamente con los valores que genera classify_tramite()
DEFAULT_SUGGESTIONS: dict[str, list[str]] = {
    "laboral": [
        "¿Cuánto me corresponde de indemnización?",
        "¿Qué plazos tengo para reclamar?",
        "¿Cómo preparo la reclamación por escrito?",
    ],
    "vivienda": [
        "¿Es legal esta cláusula de mi contrato?",
        "¿Cómo reclamo la devolución de la fianza?",
        "¿Qué plazos tengo para actuar?",
    ],
    # "reclamaciones" es la categoría que genera el clasificador para consumo
    "reclamaciones": [
        "¿Cuánto me deben compensar exactamente?",
        "¿Dónde y cómo presento la reclamación?",
        "¿Qué pasa si la empresa no me contesta?",
    ],
    # Alias para compatibilidad si el clasificador genera "consumo"
    "consumo": [
        "¿Cuánto me deben compensar exactamente?",
        "¿Dónde y cómo presento la reclamación?",
        "¿Qué hago si no me responden?",
    ],
    "trafico": [
        "¿Puedo recurrir esta multa?",
        "¿Cuánto tiempo tengo para recurrir?",
        "¿Qué documentos necesito para el recurso?",
    ],
    "fiscal": [
        "¿Me afecta esto en mi declaración de la renta?",
        "¿Qué deducciones puedo aplicar en mi caso?",
        "¿Cuál es el plazo límite de presentación?",
    ],
    "familia": [
        "¿Qué documentos necesito reunir?",
        "¿Cuáles son mis derechos en esta situación?",
        "¿Qué plazos debo tener en cuenta?",
    ],
    # "burocracia_general" y "administrativo" son categorías equivalentes
    "administrativo": [
        "¿Cómo presento un recurso administrativo?",
        "¿Cuánto tiempo tengo para recurrir?",
        "¿Necesito certificado digital para esto?",
    ],
    "burocracia_general": [
        "¿Cómo presento un recurso administrativo?",
        "¿Cuánto tiempo tengo para recurrir?",
        "¿Necesito certificado digital para esto?",
    ],
    "penal": [
        "¿Qué derechos tengo en esta situación?",
        "¿Necesito contratar un abogado?",
        "¿Cuáles son los plazos que debo respetar?",
    ],
}

GENERIC_SUGGESTIONS = [
    "¿Qué plazos tengo para actuar?",
    "¿Qué documentos necesito reunir?",
    "¿Cuál es el siguiente paso que debo dar?",
]
