Diagnostica y corrige problemas en el pipeline de chat de TramitUp.

**Diagnóstico sistemático:**

### 1. Identifica dónde falla el pipeline
Lee los archivos clave del chat y busca el error:
- `backend/app/api/v1/endpoints/chat.py` — SSE generator
- `backend/app/services/chat_service.py` — run_chat(), classify, retrieve
- `frontend/app/chat/page.tsx` — handleSend(), SSE reader loop

### 2. Problemas frecuentes y soluciones

**El chat no responde / spinner infinito:**
- Verifica rate limit: ¿usuario free con >= 2 mensajes hoy?
- Verifica que el SSE reader lee `data: ` correctamente (buffer de líneas)
- Comprueba logs del backend: ¿hay excepción silenciosa?

**Respuesta cortada o sin spaces:**
- Verifica que `clean_response_text()` no se llama con `final=True` en chunks
- Solo usar `final=True` en el texto completo post-stream

**Portal info no aparece:**
- Verificar que `item.portal_summary` existe en el evento SSE
- El frontend NO hace fetch adicional — usa directamente `item.portal_summary`

**Error de rate limit erróneo:**
- Verificar timezone: debe ser Europe/Madrid
- Verificar tabla `daily_usage` en Supabase
- Verificar fallback in-memory: ¿está activo accidentalmente?

**Sugerencias de follow-up no aparecen:**
- Verificar `_generate_follow_up_suggestions()` en chat.py
- Verificar `FOLLOW_UP_PROMPT` en `prompts/follow_up_suggestions.py`
- Verificar que el evento `follow_up_suggestions` se parsea en `page.tsx`

**Índice de mensaje incorrecto (feedback en mensaje equivocado):**
- Verificar cálculo de `idx = messages.length + 1` ANTES de los setMessages

### 3. Pasos de debugging
1. Activa logs en el backend con nivel DEBUG
2. Abre DevTools → Network → busca la request del chat (SSE)
3. Inspecciona los chunks raw del SSE en el Network tab
4. Verifica que cada evento tiene `data: [{...}]` con el JSON correcto

**Problema específico:** $ARGUMENTS
