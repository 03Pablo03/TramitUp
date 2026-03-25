"""
Prompt para generar sugerencias de seguimiento contextuales tras cada respuesta.
"""

FOLLOW_UP_PROMPT = """Eres un asistente legal español. Basándote en la conversación, genera exactamente 3 sugerencias de seguimiento que el usuario probablemente necesitará.

CATEGORÍA detectada: {category}
SUBCATEGORÍA: {subcategory}

ÚLTIMO MENSAJE DEL USUARIO:
{user_message}

RESUMEN DE LA RESPUESTA DEL ASISTENTE (últimos 500 caracteres):
{assistant_summary}

REGLAS:
- Genera exactamente 3 sugerencias, una por línea
- Cada sugerencia debe ser una pregunta o acción concreta (máximo 60 caracteres)
- Deben ser el siguiente paso lógico que el usuario necesitaría
- Usa lenguaje natural, directo y en primera persona ("¿Cuánto me corresponde?")
- NO repitas lo que ya se ha respondido
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
        "Genera una carta de reclamación",
    ],
    "vivienda": [
        "¿Es legal esta cláusula de mi contrato?",
        "¿Cómo reclamo la fianza?",
        "¿Qué plazos tengo?",
    ],
    # "reclamaciones" es la categoría que genera el clasificador para consumo
    "reclamaciones": [
        "¿Cuánto me deben compensar?",
        "¿Dónde presento la reclamación?",
        "Genera una carta de reclamación",
    ],
    # Alias para compatibilidad si el clasificador genera "consumo"
    "consumo": [
        "¿Cuánto me deben compensar?",
        "¿Dónde presento la reclamación?",
        "Genera una hoja de reclamaciones",
    ],
    "trafico": [
        "¿Puedo recurrir esta multa?",
        "¿Qué plazo tengo para recurrir?",
        "¿Qué documentos necesito?",
    ],
    "fiscal": [
        "¿Me afecta esta campaña fiscal?",
        "¿Qué deducciones puedo aplicar?",
        "¿Cuál es el plazo de presentación?",
    ],
    "familia": [
        "¿Qué documentos necesito?",
        "¿Cuáles son mis derechos?",
        "¿Qué plazos hay?",
    ],
    # "burocracia_general" y "administrativo" son categorías equivalentes
    "administrativo": [
        "¿Cómo presento un recurso?",
        "¿Qué plazo tengo?",
        "¿Necesito certificado digital?",
    ],
    "burocracia_general": [
        "¿Cómo presento un recurso administrativo?",
        "¿Qué plazo tengo para recurrir?",
        "¿Necesito certificado digital?",
    ],
    "penal": [
        "¿Qué derechos tengo?",
        "¿Necesito abogado?",
        "¿Cuáles son los plazos?",
    ],
}

GENERIC_SUGGESTIONS = [
    "¿Qué plazos tengo?",
    "¿Qué documentos necesito?",
    "Crear un expediente para esto",
]
