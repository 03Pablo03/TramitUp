Corrige el bug descrito en TramitUp.

**Proceso:**
1. Lee el archivo afectado completo para entender el contexto
2. Identifica la causa raíz (no solo el síntoma)
3. Aplica el fix mínimo necesario — no refactorices código no relacionado
4. Verifica que el fix no rompe otros flujos que usen el mismo código

**Contexto del proyecto:**
- Backend: FastAPI en `/backend/app/` — errores se propagan como `HTTPException` o `ValueError`
- Frontend: Next.js en `/frontend/app/` — errores de API se muestran en state `error`
- API calls frontend → backend siempre via `apiFetch()` en `/api/backend/`
- Auth: `useAuth()` en frontend, `require_auth` dependency en backend

Bug a corregir: $ARGUMENTS
