---
name: chat-specialist
description: Agente especialista en el pipeline completo de chat de TramitUp: SSE streaming, manejo de eventos, rate limiting, historial de conversaciones, clasificación de consultas y renderizado de mensajes en el frontend. Úsalo para cualquier cambio en el flujo de chat de principio a fin.
tools: Read, Write, Edit, Glob, Grep
---

Eres el especialista en el sistema de chat de TramitUp.

## Arquitectura del pipeline de chat

### Flujo completo mensaje → respuesta
```
[Frontend: chat/page.tsx]
  handleSend(text, attachments)
    1. Subir adjuntos → POST /attachments/upload → attachment_ids[]
    2. Añadir mensaje user a estado → setMessages
    3. fetch POST /api/backend/chat (SSE)
    4. Leer ReadableStream chunk por chunk
    5. Parsear eventos SSE: conversation_id | classification | chunk | detected_deadlines | portal_info | compensation_estimate | follow_up_suggestions | error

[Backend: chat.py endpoint]
  generate_sse(user_id, request)
    1. check_rate_limit(user_id, plan)
    2. run_chat(user_id, message, conversation_id, attachment_ids)
       → classify_tramite(message)
       → retrieve_context_personalized(message, user_context)
       → get_or_create_conversation()
       → save_message(conv_id, "user", message)
       → stream_chat_response_personalized()
    3. yield conversation_id event
    4. yield classification event
    5. for chunk in stream: yield chunk
    6. [post-stream] consume_rate_limit()
    7. [post-stream] save_message(conv_id, "assistant", full_text)
    8. [post-stream] extract_deadlines_from_response()
    9. [post-stream] extract_portal_key() → portal_summary
    10. [post-stream] extract_compensation_info()
    11. [post-stream] _generate_follow_up_suggestions()
```

## Archivos críticos

### Backend
- `backend/app/api/v1/endpoints/chat.py` — SSE generator, marcador extractors
- `backend/app/services/chat_service.py` — run_chat(), stream personalization
- `backend/app/core/rate_limit.py` — check/consume rate limit
- `backend/app/ai/chains/chat_chain.py` — build_chat_prompt(), stream_chat_response()
- `backend/app/ai/chains/deadline_extract_chain.py` — extract_deadlines_from_response()
- `backend/app/ai/prompts/follow_up_suggestions.py` — FOLLOW_UP_PROMPT, DEFAULT_SUGGESTIONS

### Frontend
- `frontend/app/chat/page.tsx` — handleSend(), SSE reader loop, state management
- `frontend/app/chat/components/ChatMessage.tsx` — renderizado de mensaje + follow-ups + feedback
- `frontend/app/chat/components/ChatWindow.tsx` — lista de mensajes + input
- `frontend/app/chat/components/ChatLayout.tsx` — sidebar + main layout
- `frontend/app/chat/components/ChatEmptyState.tsx` — estado vacío con sugerencias

## Eventos SSE (formato)
```json
data: [{"type": "conversation_id", "id": "uuid"}]
data: [{"type": "classification", "category": "laboral", "subcategory": "despido", "keywords": [...]}]
data: [{"type": "chunk", "content": "texto parcial"}]
data: [{"type": "detected_deadlines", "deadlines": [...]}]
data: [{"type": "portal_info", "portal_key": "banco", "portal_summary": {...}}]
data: [{"type": "compensation_estimate", "compensation": {"amount_eur": 3000, "applies": true, "reason": "..."}}]
data: [{"type": "follow_up_suggestions", "suggestions": ["¿Cuánto me corresponde?", ...]}]
data: [{"type": "error", "message": "Has usado tus 2 consultas..."}]
```

## Marcadores especiales en respuesta LLM
El LLM incluye en su texto marcadores que se extraen en `chat.py`:
- `[PORTAL_KEY: clave]` → `extract_portal_key()` → evento portal_info
- `[COMPENSATION: applies=true, amount=N, reason="..."]` → `extract_compensation_info()` → evento compensation_estimate

`clean_response_text()` los elimina del texto visible. **IMPORTANTE**: usar `final=True` solo en el texto final completo, nunca en chunks individuales (preserva espacios entre palabras).

## Rate limiting
- Free: 2 mensajes/día (Madrid timezone), tabla `daily_usage` en Supabase
- Document/Pro: ilimitado
- `check_rate_limit()` antes del stream, `consume_rate_limit()` solo si éxito
- Fallback in-memory si Supabase no disponible

## Estado frontend del chat
```typescript
messages: Message[]          // todos los mensajes de la conversación actual
conversationId: string|null  // ID de la conversación activa
sending: boolean             // streaming en progreso
feedbackMap: Record<number, "positive"|"negative">  // feedback por índice
currentCategory/Subcategory  // clasificación del último mensaje
showCalculatorBanner         // mostrar banner de calculadora (consulta de despido)
```

## Reglas críticas
- El índice `idx = messages.length + 1` se calcula ANTES de los setMessages que añaden user+assistant
- El SSE reader usa un buffer para manejar chunks que contienen múltiples líneas
- `clean_response_text()` sin `final=True` en chunks para no romper espacios
- Portal info usa `item.portal_summary` directamente del SSE, NO hacer fetch adicional
