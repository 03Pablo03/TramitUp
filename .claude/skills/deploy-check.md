Verifica que TramitUp está listo para deploy a producción.

**Checklist automático:**

### Variables de entorno backend
Comprueba que `backend/app/core/config.py` valida:
- `GOOGLE_API_KEY` — LLM/Gemini
- `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` + `SUPABASE_JWT_SECRET` — DB
- `STRIPE_SECRET_KEY` + precios — pagos
- `FRONTEND_URL` — CORS (no debe ser localhost)
- `ENVIRONMENT=production`

### Variables de entorno frontend
Busca en `frontend/` los `process.env.NEXT_PUBLIC_*` usados:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`

### Código
- Busca `console.log` en frontend (no deben estar en producción)
- Busca `TODO` pendientes críticos
- Verifica que no hay credenciales hardcodeadas
- Confirma que Swagger está deshabilitado en producción (`main.py`)
- Verifica que `middleware.ts` redirige correctamente a `/dashboard`

### Base de datos
Lista las tablas que necesitan existir en Supabase:
`profiles, conversations, messages, alerts, cases, tramite_wizards, message_feedback, daily_usage, attachments`

Genera un informe de estado de deploy. $ARGUMENTS
