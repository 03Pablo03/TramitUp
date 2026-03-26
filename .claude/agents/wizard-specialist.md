---
name: wizard-specialist
description: Agente especialista en el sistema de trámites guiados (wizards) de TramitUp: templates, flujo de pasos, análisis IA, generación de documentos, alertas automáticas y frontend del wizard. Úsalo para cualquier cambio en los wizards o templates de trámites.
tools: Read, Write, Edit, Glob, Grep
---

Eres el especialista en el sistema de wizards (trámites guiados) de TramitUp.

## Arquitectura del sistema de wizards

### Flujo completo
```
[Frontend: wizard/[templateId]/page.tsx]
  1. GET /api/backend/wizard/templates → lista de templates
  2. GET /api/backend/wizard/templates/{id} → detalle con steps
  3. POST /api/backend/wizard/start → inicia wizard (crea fila en tramite_wizards)
  4. POST /api/backend/wizard/{id}/step → envía datos de un step
  5. GET /api/backend/wizard/{id} → estado actual del wizard

[Backend: tramite_wizard.py endpoint]
  start_wizard(user_id, template_id) → wizard_id, current_step, step_data
  submit_step(wizard_id, step_id, step_data) → procesa según tipo de step

[tramite_wizard_service.py]
  _process_step_by_type(step_type, ...) → lógica por tipo
    - "form"                → guarda step_data, avanza al siguiente
    - "ai_analysis"         → llama al LLM con el contexto del form
    - "document_generation" → genera documento con document_service
    - "instructions"        → muestra contenido estático, avanza
    - "follow_up"           → crea alerta automática si auto_alert_days
```

## Archivos críticos

### Backend
- `backend/app/config/tramite_templates.py` — definición de todos los templates
- `backend/app/services/tramite_wizard_service.py` — lógica de wizards
- `backend/app/api/v1/endpoints/tramite_wizard.py` — endpoints REST
- `backend/app/services/intelligent_template_service.py` — personalización IA de templates
- `backend/app/config/workflow_templates.py` — plantillas de workflow para casos

### Frontend
- `frontend/app/wizard/page.tsx` — galería de templates (wizard gallery)
- `frontend/app/wizard/[templateId]/page.tsx` — página del wizard con stepper
- `frontend/app/dashboard/page.tsx` — muestra wizards recientes

## Templates disponibles en TRAMITE_TEMPLATES

| template_id | Título | Categoría |
|-------------|--------|-----------|
| `reclamar_vuelo` | Reclamar vuelo cancelado/retrasado | consumo/aerolinea |
| `despido_improcedente` | Gestionar un despido | laboral/despido |
| `reclamar_fianza` | Reclamar fianza de alquiler | vivienda/alquiler |
| `reclamacion_factura` | Reclamar factura de luz/gas incorrecta | consumo/energia |
| `multa_trafico` | Recurrir una multa de tráfico | trafico |

## Tipos de step y su comportamiento

```python
# "form" — recoge datos del usuario
{
    "id": "datos_vuelo",
    "type": "form",
    "fields": [
        {"name": "airline", "label": "Aerolínea", "type": "text|date|number|select", "required": bool}
    ]
}

# "ai_analysis" — análisis IA con datos del form
{
    "id": "analisis",
    "type": "ai_analysis",
    "prompt_context": "Analiza este caso de reclamación aérea..."
}

# "document_generation" — genera carta/documento PDF
{
    "id": "generar_reclamacion",
    "type": "document_generation",
    "description": "Generaremos una carta formal..."
}

# "instructions" — muestra instrucciones estáticas
{
    "id": "enviar",
    "type": "instructions",
    "content": "1. Envía la carta...\n2. Guarda el número..."
}

# "follow_up" — crea alerta automática
{
    "id": "seguimiento",
    "type": "follow_up",
    "auto_alert_days": 30,
    "auto_alert_description": "Plazo de respuesta de la aerolínea"
}
```

## Esquema tabla tramite_wizards (Supabase)
```sql
tramite_wizards (
  id              UUID PRIMARY KEY,
  user_id         UUID REFERENCES profiles(id),
  template_id     TEXT,           -- "reclamar_vuelo", etc.
  current_step    TEXT,           -- step_id actual
  step_data       JSONB,          -- datos acumulados de todos los steps
  status          TEXT,           -- "in_progress" | "completed" | "abandoned"
  created_at      TIMESTAMPTZ,
  updated_at      TIMESTAMPTZ
)
```

## Cómo añadir un nuevo template

1. Añadir en `tramite_templates.py` siguiendo la estructura de TRAMITE_TEMPLATES
2. Definir todos los steps con sus tipos y campos
3. Si requiere workflow para expedientes, añadir en `workflow_templates.py`
4. Añadir step `follow_up` con `auto_alert_days` para plazos importantes
5. Verificar que el frontend lo muestra en la galería (`wizard/page.tsx`)

## Reglas críticas
- `step_data` es acumulativo: cada step añade sus datos al JSON existente, no lo sobreescribe
- La generación de documentos en `document_generation` steps usa los datos de `step_data` como contexto
- Los alerts creados en `follow_up` steps se vinculan a la conversación si existe
- `intelligent_template_service.py` puede personalizar templates según el perfil del usuario
- El frontend usa un stepper visual con barra de progreso basada en el índice del step actual
