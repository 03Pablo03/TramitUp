# Equipo TramitUp — Referencia completa

## Agentes disponibles (16)

| Agente | Cuándo usarlo |
|--------|--------------|
| `backend-dev` | Endpoints FastAPI, servicios Python, lógica de negocio general |
| `frontend-dev` | Páginas Next.js, componentes React, hooks, UI en general |
| `ai-specialist` | Pipeline de chat, bots, prompts, RAG, clasificación de consultas |
| `db-specialist` | Esquema Supabase, queries, migraciones, RLS, optimización SQL |
| `reviewer` | Revisión pre-deploy, code review completo, seguridad |
| `chat-specialist` | Pipeline SSE completo, eventos, rate limiting, historial de chat |
| `wizard-specialist` | Templates de trámites guiados, steps, análisis IA en wizards |
| `cases-specialist` | Expedientes (casos), workflow steps, progreso, documentos adjuntos |
| `dashboard-specialist` | Dashboard, KPIs, calendario legal, sugerencias proactivas |
| `alerts-specialist` | Alertas de plazos, notificaciones email, job de envío |
| `onboarding-specialist` | Flujo de onboarding, perfil inicial, categorías de interés |
| `auth-specialist` | JWT, require_auth, middleware Next.js, RLS, seguridad de sesiones |
| `stripe-specialist` | Pagos, suscripciones, webhooks, planes (free/document/pro) |
| `document-specialist` | Generación de cartas/docs, análisis de PDFs, adjuntos del chat |
| `rag-specialist` | Embeddings, knowledge base, retrieval personalizado, indexación |
| `performance-specialist` | Caché, queries lentas, bundle size, Core Web Vitals, monitoring |

## Skills disponibles — slash commands (20)

| Skill | Uso |
|-------|-----|
| `/nuevo-endpoint <descripción>` | Crea endpoint backend + integración frontend |
| `/nueva-pagina <descripción>` | Crea página Next.js con auth y fetching |
| `/fix-bug <descripción>` | Corrige un bug específico con diagnóstico sistemático |
| `/sprint-status` | Revisa estado de implementación del plan de sprints |
| `/deploy-check` | Checklist completo de producción antes de deploy |
| `/add-wizard-template <descripción>` | Añade nuevo template de trámite guiado |
| `/add-bot <descripción>` | Añade nuevo bot especializado al sistema de chat |
| `/update-prompt <descripción>` | Actualiza o mejora un prompt de IA |
| `/add-rag-content <descripción>` | Añade contenido legal al knowledge base RAG |
| `/create-migration <descripción>` | Crea migración de base de datos para Supabase |
| `/add-legal-template <descripción>` | Añade plantilla de documento legal generado por IA |
| `/debug-chat <descripción>` | Diagnostica problemas en el pipeline de chat SSE |
| `/create-workflow-template <descripción>` | Crea plantilla de workflow para expedientes |
| `/add-onboarding-step <descripción>` | Añade o modifica paso del onboarding |
| `/audit-security [alcance]` | Auditoría de seguridad completa o de un área |
| `/optimize-performance <área>` | Análisis y optimización de rendimiento |
| `/add-seo-page <descripción>` | Crea nueva landing page SEO |
| `/test-wizard-flow <template_id>` | Testea el flujo completo de un wizard |
| `/review-code [archivos]` | Revisión de código con checklist completo |
| `/add-legal-category <categoría>` | Añade nueva categoría legal al sistema |

## Flujos de trabajo recomendados

### Nueva feature completa
1. Planificar con `backend-dev` + `frontend-dev` en paralelo
2. Backend: `backend-dev` crea service → endpoint → registra en router
3. Frontend: `frontend-dev` crea página/componente → conecta con `apiFetch`
4. Revisar con `reviewer` antes de commit

### Bug en producción
1. Identifica si es frontend o backend
2. Usa el agente especialista del área afectada (ej. `chat-specialist` para bugs del chat)
3. Usa `/fix-bug <descripción>` para diagnóstico sistemático
4. Revisar con `reviewer`

### Cambio en el chat pipeline
1. Usar `chat-specialist` para cualquier cambio en SSE, eventos o flujo de mensajes
2. Siempre testear con una consulta real después del cambio
3. Verificar `clean_response_text()` no se llama con `final=True` en chunks

### Nueva funcionalidad de IA/LLM
1. `ai-specialist` para bots y diseño del prompt
2. `/update-prompt` para modificar prompts existentes
3. `/add-bot` para añadir un nuevo bot especializado
4. Siempre testear con preguntas de prueba representativas

### Nuevo trámite guiado (wizard)
1. `wizard-specialist` para definir el template y los steps
2. `/add-wizard-template <descripción>` para implementación guiada
3. `/create-workflow-template` si crea expediente automáticamente
4. `/test-wizard-flow <id>` para verificar el flujo completo

### Cambio en base de datos
1. `db-specialist` para diseño del esquema
2. `/create-migration` para generar el SQL de la migración
3. Actualizar servicios Python afectados
4. Verificar RLS policies con `/audit-security`

### Preparar deploy a producción
1. `/sprint-status` para verificar estado de implementación
2. `/audit-security` para revisión de seguridad
3. `/deploy-check` para checklist completo
4. `/review-code` para los últimos cambios

## Contexto del proyecto
- **Stack**: Next.js 14 + FastAPI + Supabase + Google Gemini
- **Producción**: render.yaml define el deploy
- **Base de datos**: Supabase (PostgreSQL + pgvector para RAG)
- **IA**: Google Gemini vía LangChain (chat + embeddings)
- **Pagos**: Stripe (ver `stripe-specialist`)
- **Auth**: Supabase Auth con JWT verificado localmente en el backend
- **Planes**: free (2 consultas/día) | document (pago único) | pro (suscripción)
- **Plan gratuito**: sin alertas automáticas, sin PDFs
- **Plan Document/Pro**: ilimitado + alertas + documentos PDF
