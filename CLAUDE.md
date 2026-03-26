# TramitUp — Guía para Claude Code

Plataforma de información jurídica para ciudadanos españoles.
**Stack**: Next.js 14 + FastAPI + Supabase + Google Gemini

## Estructura del proyecto
```
TramitUp/
├── frontend/          # Next.js 14 (App Router) + TypeScript + Tailwind
├── backend/           # FastAPI + Python 3.11
├── .claude/
│   ├── agents/        # Agentes especializados (backend-dev, frontend-dev, ai-specialist…)
│   ├── skills/        # Slash commands (/nuevo-endpoint, /fix-bug, /sprint-status…)
│   ├── hooks/         # Hooks de herramientas
│   └── teams/         # Referencia del equipo de agentes
└── CLAUDE.md          # Este archivo
```

## Comandos rápidos
```bash
# Frontend (desde /frontend)
npm run dev          # Desarrollo local :3000
npm run build        # Build producción
npx tsc --noEmit     # Verificar tipos TypeScript

# Backend (desde /backend)
uvicorn app.main:app --reload   # Desarrollo local :8000
python -m pytest                # Tests
```

## Agentes especializados
Usa los agentes en `.claude/agents/` para tareas específicas:
- **backend-dev**: endpoints, services, lógica Python
- **frontend-dev**: páginas Next.js, componentes, hooks
- **ai-specialist**: chat pipeline, bots, prompts, RAG
- **db-specialist**: Supabase, esquema, queries
- **reviewer**: revisión pre-deploy

## Convenciones críticas
1. **Auth**: `require_auth` en backend, `useAuth()` en frontend
2. **API calls**: siempre `apiFetch("/ruta")`, nunca fetch directo
3. **Ownership**: siempre filtrar por `user_id` en queries
4. **Errores**: `HTTPException` en backend, state `error` en frontend
5. **TypeScript**: strict, sin `any`, `Array.from(new Set(...))` para conjuntos

## Planes y planes de usuario
- `free`: 2 consultas/día
- `document`: ilimitado + PDFs + alertas
- `pro`: todo lo anterior + funciones premium

## Variables de entorno necesarias
Ver `backend/app/core/config.py` (backend) y archivos `.env.local` del frontend.
En producción: `ENVIRONMENT=production` deshabilita Swagger docs.
