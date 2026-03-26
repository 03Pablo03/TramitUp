Crea una nueva plantilla de workflow para expedientes en TramitUp.

**Pasos:**

1. Lee `backend/app/config/workflow_templates.py` para ver las plantillas existentes
2. Lee `backend/app/services/case_service.py` → `create_case()` para ver cómo se usan
3. Añade la nueva plantilla en `workflow_templates.py`:
   ```python
   "categoria_subcategoria": {
       "steps": [
           {
               "id": "paso_unico_id",
               "title": "Título del paso",
               "description": "Qué hacer en este paso",
               "status": "pending",
               "order": 1,
               "required": True,
               "document_type": "tipo_documento_opcional"  # si requiere un documento
           },
           # ... más pasos ordenados cronológicamente
       ],
       "documents": [
           "Documento requerido 1",
           "Documento requerido 2",
       ]
   }
   ```
4. Los steps deben reflejar el proceso legal real en España:
   - Seguir orden cronológico del proceso
   - Incluir plazos relevantes en la descripción
   - `required: True` para los steps críticos, `False` para opcionales
5. Registra el mapping en `get_workflow_template(category, subcategory)` para que se auto-popule
6. Verifica que al crear un expediente con esa categoría, los steps aparecen correctamente

**Workflow a crear:** $ARGUMENTS
