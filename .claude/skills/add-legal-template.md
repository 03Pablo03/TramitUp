Añade una nueva plantilla de documento legal al sistema de generación de TramitUp.

**Pasos:**

1. Lee `backend/app/ai/prompts/document_templates.py` para ver las plantillas existentes
2. Lee `backend/app/ai/prompts/document_generate.py` para entender el prompt de generación
3. Añade la nueva plantilla en `document_templates.py`:
   ```python
   "tipo_documento": {
       "name": "Nombre legible del documento",
       "description": "Para qué sirve",
       "category": "laboral|vivienda|consumo|familia|trafico|administrativo",
       "required_fields": ["campo1", "campo2", ...],  # campos obligatorios del form_data
       "optional_fields": ["campo_opcional"],
       "prompt_template": """
       Eres un abogado español experto en {categoria}.
       Redacta una carta/recurso/reclamación formal con los siguientes datos:
       {datos_del_formulario}

       La carta debe:
       - Seguir el formato legal español
       - Incluir referencias a la legislación aplicable
       - Tener fecha, destinatario y firma del remitente
       - Ser clara y formal
       """,
       "output_format": "carta|recurso|reclamacion|denuncia"
   }
   ```
4. Registra el tipo en `document_service.py` para que sea genereable via API
5. Si hay una página SEO asociada (ej. `/modelo-carta-xxx`), actualiza `frontend/app/` con la nueva landing
6. Si el documento se puede generar desde un wizard, añade el step `document_generation` al template

**Plantilla a crear:** $ARGUMENTS
