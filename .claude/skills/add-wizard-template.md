Añade un nuevo template de trámite guiado al sistema de wizards de TramitUp.

**Pasos:**

1. Lee `backend/app/config/tramite_templates.py` para entender la estructura existente
2. Lee `backend/app/config/workflow_templates.py` para ver cómo se relacionan con expedientes
3. Añade el nuevo template en `TRAMITE_TEMPLATES` con esta estructura:
   ```python
   "id_del_tramite": {
       "id": "id_del_tramite",
       "title": "Título descriptivo",
       "description": "Descripción breve de lo que se consigue",
       "icon": "emoji",
       "category": "laboral|vivienda|consumo|familia|trafico|administrativo|fiscal",
       "subcategory": "subcategoría específica",
       "estimated_time": "X-Y minutos",
       "steps": [...]
   }
   ```
4. Define los steps siguiendo los tipos disponibles:
   - `"form"` — campos del formulario (text, date, number, select, textarea)
   - `"ai_analysis"` — análisis IA con `prompt_context`
   - `"document_generation"` — genera carta/documento
   - `"instructions"` — instrucciones estáticas con `content`
   - `"follow_up"` — alerta automática con `auto_alert_days` y `auto_alert_description`
5. Si el trámite crea un expediente, añade el workflow en `workflow_templates.py`
6. Verifica que el template aparece en `list_tramite_templates()` (galería del wizard)
7. Comprueba que el frontend en `wizard/page.tsx` lo renderiza correctamente

**Template de descripción:** $ARGUMENTS
