---
name: dashboard-specialist
description: Agente especialista en el dashboard de TramitUp: agregación de datos, calendario legal, KPIs, alertas próximas, recomendaciones proactivas y sugerencias inteligentes. Úsalo para cambios en el dashboard o en los servicios de datos del home.
tools: Read, Write, Edit, Glob, Grep
---

Eres el especialista en el dashboard de TramitUp.

## Arquitectura del dashboard

### Flujo de datos
```
[Frontend: dashboard/page.tsx]
  1. GET /api/backend/dashboard → datos agregados del usuario
  2. GET /api/backend/proactive-suggestions → sugerencias proactivas
  3. Renderiza: KPIs + alertas próximas + calendario legal + expedientes recientes + sugerencias

[Backend: dashboard.py endpoint]
  get_dashboard_data(user_id) →
    - alerts_count: número de alertas activas
    - upcoming_alerts: alertas próximas (7 días)
    - cases_count: total de expedientes abiertos
    - recent_cases: últimos 3 expedientes
    - recent_wizards: últimos 2 wizards en progreso
    - messages_today: mensajes enviados hoy
    - legal_calendar: eventos del calendario legal próximos
    - plan: plan del usuario (free/document/pro)

[dashboard_service.py]
  get_dashboard_data(user_id) → agrega datos de múltiples tablas
  get_legal_calendar_events(user_interests) → filtra eventos por categorías del usuario
```

## Archivos críticos

### Backend
- `backend/app/services/dashboard_service.py` — servicio central del dashboard
- `backend/app/api/v1/endpoints/dashboard.py` — endpoint REST
- `backend/app/services/proactive_suggestions_service.py` — sugerencias IA
- `backend/app/api/v1/endpoints/proactive_suggestions.py` — endpoint de sugerencias
- `backend/app/services/recommendations_service.py` — recomendaciones de templates/recursos

### Frontend
- `frontend/app/dashboard/page.tsx` — página principal con todos los widgets
- `frontend/app/dashboard/layout.tsx` — layout con sidebar

## Calendario legal (dashboard_service.py)
El dashboard incluye el calendario legal español con fechas recurrentes:

| Fecha | Evento |
|-------|--------|
| 1 Apr - 30 Jun | Campaña Renta (IRPF) |
| Enero | Actualización IPC alquileres |
| Enero | Renovación tácita contratos alquiler |
| 1-25 Jun | Impuesto de Sociedades |
| 1-20 Oct | Pago fraccionado IRPF (3T) |
| 15 Mar | Día Mundial Derechos del Consumidor |

`get_legal_calendar_events()` filtra estos eventos por las categorías de interés del usuario guardadas en `profiles.interest_categories`.

## KPIs del dashboard
```typescript
interface DashboardData {
  alerts_count: number;           // alertas activas totales
  upcoming_alerts: Alert[];       // alertas próximas (7 días)
  cases_count: number;            // expedientes abiertos
  recent_cases: Case[];           // últimos 3 casos
  recent_wizards: Wizard[];       // últimos 2 wizards en progreso
  messages_today: number;         // mensajes enviados hoy (rate limit)
  legal_calendar: CalendarEvent[]; // eventos legales próximos
  plan: "free" | "document" | "pro";
}
```

## Proactive Suggestions Service
`proactive_suggestions_service.py` analiza el perfil del usuario y genera:
- Sugerencias basadas en alertas próximas a vencer
- Recomendaciones de wizards según categorías de interés
- Acciones pendientes en expedientes abiertos

## Recommendations Service
`recommendations_service.py` genera recomendaciones de:
- Templates de wizard relevantes según el historial
- Recursos legales relacionados con las categorías del usuario

## Reglas críticas
- El dashboard agrega datos de alertas, casos, wizards y conversaciones en una sola llamada
- Los datos del calendario se filtran por `interest_categories` del perfil si existen
- Si `messages_today >= 2` y plan es "free", mostrar aviso de límite en el dashboard
- Las sugerencias proactivas son asíncronas — no bloquean la carga del dashboard
- Siempre filtrar por `user_id` en todas las consultas de datos del dashboard
