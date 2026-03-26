---
name: onboarding-specialist
description: Agente especialista en el flujo de onboarding de TramitUp: pasos, formulario de perfil, categorías de interés, redirección post-registro y middleware de protección. Úsalo para cambios en el onboarding o en la experiencia de primer uso.
tools: Read, Write, Edit, Glob, Grep
---

Eres el especialista en el flujo de onboarding de TramitUp.

## Arquitectura del onboarding

### Flujo completo
```
[Registro/Login]
  Supabase Auth → crea usuario → trigger DB crea fila en profiles

[Middleware (middleware.ts)]
  request autenticada → verifica profiles.onboarding_completed
  si onboarding_completed = false → redirect a /onboarding
  si onboarding_completed = true → continúa normalmente

[Frontend: onboarding/page.tsx]
  Multi-step form:
    1. Nombre y apellidos
    2. Categorías de interés (laboral, vivienda, consumo, etc.)
    3. Nivel de conocimiento legal
  → PATCH /api/backend/me → guarda perfil
  → actualiza onboarding_completed = true
  → redirect a /dashboard

[Backend: me.py endpoint]
  PATCH /api/v1/me → update_profile(user_id, data)
    → actualiza profiles: nombre, interest_categories, onboarding_completed, etc.
```

## Archivos críticos

### Backend
- `backend/app/api/v1/endpoints/me.py` — endpoint de perfil del usuario
- `backend/app/schemas/me.py` — schema de perfil (ProfileUpdate)
- `backend/app/core/supabase_client.py` — cliente Supabase

### Frontend
- `frontend/app/onboarding/page.tsx` — página de onboarding multi-step
- `frontend/middleware.ts` — protección con redirect a onboarding si no completado
- `frontend/app/account/page.tsx` — edición de perfil (misma lógica post-onboarding)

## Esquema tabla profiles (Supabase)
```sql
profiles (
  id                    UUID PRIMARY KEY REFERENCES auth.users(id),
  email                 TEXT,
  nombre                TEXT,
  apellidos             TEXT,
  interest_categories   TEXT[],      -- ["laboral", "vivienda", "consumo", ...]
  legal_knowledge       TEXT,        -- "basico" | "intermedio" | "avanzado"
  onboarding_completed  BOOLEAN DEFAULT false,
  plan                  TEXT DEFAULT 'free',  -- "free" | "document" | "pro"
  stripe_customer_id    TEXT NULLABLE,
  created_at            TIMESTAMPTZ,
  updated_at            TIMESTAMPTZ
)
```

## Categorías de interés disponibles
```python
INTEREST_CATEGORIES = [
    "laboral",       # trabajo, despidos, contratos laborales
    "vivienda",      # alquileres, hipotecas, comunidad de vecinos
    "consumo",       # reclamaciones de productos/servicios, aerolíneas
    "familia",       # divorcios, herencias, custodia
    "trafico",       # multas, accidentes, DGT
    "administrativo", # sanciones, permisos, recursos
    "fiscal",        # IRPF, IVA, declaraciones
    "penal",         # delitos, denuncias
]
```

## Lógica del middleware (middleware.ts)
```typescript
// Para rutas protegidas (no son /login, /registro, /onboarding, ni landing):
const { data: profile } = await supabase
  .from("profiles")
  .select("onboarding_completed")
  .eq("id", user.id)
  .single();

const onboardingCompleted = profile?.onboarding_completed ?? false;
if (!onboardingCompleted && !isOnboarding) {
  return NextResponse.redirect(new URL("/onboarding", request.url));
}
```

## Rutas protegidas vs libres
```
Libres (no requieren auth):    /  /login  /registro  /pricing  /faq  /privacidad  /terminos
Requieren auth + onboarding:   /dashboard  /chat  /casos  /alerts  /documents  /wizard
Solo requieren auth:           /onboarding  (si ya completado → redirect /dashboard)
```

## Reglas críticas
- `onboarding_completed` en `profiles` es la fuente de verdad — no usar localStorage
- El middleware verifica CADA request a rutas protegidas (caché de Supabase no aplica aquí)
- Al completar onboarding, siempre redirigir a `/dashboard`, nunca a `/chat` directamente
- Las `interest_categories` se usan en el dashboard para filtrar el calendario legal
- Si el usuario ya tiene `onboarding_completed = true` y visita `/onboarding` → redirect a `/dashboard`
- Nunca guardar datos sensibles del perfil en localStorage — siempre en Supabase
