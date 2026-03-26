Añade una nueva categoría legal al sistema de TramitUp.

**Pasos:**

1. Lee los archivos de configuración de categorías:
   - `backend/app/services/case_service.py` → `VALID_CATEGORIES`
   - `backend/app/ai/prompts/classification.py` → categorías de clasificación
   - `backend/app/config/workflow_templates.py` → templates de workflow
   - `frontend/app/onboarding/page.tsx` → categorías de interés del usuario

2. Añade la categoría en `case_service.py`:
   ```python
   VALID_CATEGORIES = frozenset({
       "laboral", "vivienda", "consumo", "familia",
       "trafico", "administrativo", "fiscal", "penal",
       "nueva_categoria",  # ← añadir aquí
       "otro",
   })
   ```

3. Añade la categoría en el prompt de clasificación (`classification.py`):
   - Describe cuándo se debe clasificar una consulta como esta categoría
   - Añade subcategorías relevantes
   - Define keywords típicas de esta categoría

4. Crea el workflow template en `workflow_templates.py`:
   - Steps típicos del proceso legal de esta categoría en España
   - Documentos requeridos habitualmente

5. Actualiza el frontend:
   - `onboarding/page.tsx` → añade opción en categorías de interés
   - `casos/page.tsx` → añade opción en filtro de categoría
   - Icono/color para la nueva categoría en el UI

6. Añade contenido RAG para la nueva categoría:
   - Usa el skill `/add-rag-content` para indexar información legal básica
   - Mínimo 10-15 chunks autocontenidos de la legislación relevante

7. Verifica end-to-end:
   - Crear expediente con la nueva categoría
   - Hacer consulta al chat sobre un tema de la categoría
   - Verificar que la clasificación detecta correctamente la categoría

**Categoría a añadir:** $ARGUMENTS
