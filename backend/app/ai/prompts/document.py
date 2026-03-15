"""
Prompt para generar modelo de escrito.
"""

DOCUMENT_PROMPT = """Basándote en el contexto normativo proporcionado y la información del usuario, genera un modelo de escrito formal.

El documento debe:
- Estar redactado en tercera persona o primera persona según el tipo de escrito
- Incluir referencias a la normativa aplicable cuando sea relevante
- Dejar marcadores claros [RELLENAR: descripción] para datos que el usuario debe completar
- Ser un modelo informativo, no asesoramiento legal
- Incluir al final el aviso: "Este documento es un modelo informativo. Tramitup no presta asesoramiento jurídico."

Contexto normativo: {context}
Información del caso: {case_info}
Tipo de escrito solicitado: {doc_type}
"""
