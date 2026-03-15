"""
Prompt para generar guía paso a paso.
"""

GUIDE_PROMPT = """Basándote en el contexto normativo proporcionado y la clasificación del trámite, genera una guía paso a paso clara y práctica.

Formato:
1. Paso 1: [Título]
   [Descripción]
   Documentación necesaria: [lista]
   Tiempo estimado: [si aplica]

2. Paso 2: ...

Incluye enlaces a sedes electrónicas cuando sea relevante (ej: sede.administracion.gob.es).
Menciona qué hacer si no hay respuesta en el plazo previsto cuando aplique.

Clasificación: {classification}
Contexto normativo: {context}
"""
