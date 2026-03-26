Actualiza o mejora un prompt del sistema de IA de TramitUp.

**Pasos:**

1. Identifica el prompt a modificar en `backend/app/ai/prompts/`:
   - `system_base.py` — prompt base del sistema
   - `classification.py` — clasificación de consultas
   - `guide.py` — respuestas guiadas
   - `document.py` / `document_generate.py` / `document_extract.py` — documentos
   - `contract_analysis.py` — análisis de contratos
   - `follow_up_suggestions.py` — sugerencias de seguimiento
2. Lee el prompt actual completo
3. Entiende el contexto: qué input recibe, qué output se espera, qué chain lo usa
4. Modifica el prompt con estas reglas:
   - Siempre en español (castellano)
   - Tono profesional pero accesible para ciudadanos sin formación jurídica
   - Incluir instrucciones explícitas sobre el formato de respuesta esperado
   - Mencionar el contexto legal español (legislación, tribunales, plazos)
   - Si el prompt usa marcadores especiales (`[PORTAL_KEY:]`, `[COMPENSATION:]`), preservarlos
5. Verifica que el chain que usa el prompt (`backend/app/ai/chains/`) lo interpreta correctamente
6. Testea manualmente con 2-3 consultas de prueba representativas

**Prompt a actualizar:** $ARGUMENTS
