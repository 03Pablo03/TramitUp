Testea el flujo completo de un wizard de trámite guiado en TramitUp.

**Pasos de testing:**

1. Lee el template a testear en `backend/app/config/tramite_templates.py`
2. Verifica cada step del template manualmente:

### Backend — tests unitarios/integración
```bash
# Desde /backend:
python -m pytest tests/ -v -k "wizard"
```

3. Verifica endpoint de templates:
   - `GET /api/v1/wizard/templates` → devuelve lista con el template
   - `GET /api/v1/wizard/templates/{id}` → devuelve template completo con steps

4. Verifica flujo completo vía API:
   - `POST /api/v1/wizard/start` con `template_id` → crea wizard, devuelve `wizard_id`
   - `POST /api/v1/wizard/{id}/step` con step `form` → guarda datos, avanza
   - `POST /api/v1/wizard/{id}/step` con step `ai_analysis` → triggerea LLM
   - `POST /api/v1/wizard/{id}/step` con step `document_generation` → genera documento
   - `POST /api/v1/wizard/{id}/step` con step `follow_up` → crea alerta

5. Casos edge a verificar:
   - Enviar step fuera de orden → debe rechazar o ignorar
   - Enviar formulario con campos requeridos vacíos → debe validar
   - Acceder a wizard de otro usuario → debe dar 403/404

### Frontend — testing manual
6. Navega a `/wizard` → verifica que aparece en la galería
7. Inicia el wizard → verifica stepper visual y barra de progreso
8. Completa cada step → verifica que los datos se guardan
9. Verifica que el step `follow_up` crea la alerta en `/alerts`

**Template a testear:** $ARGUMENTS
