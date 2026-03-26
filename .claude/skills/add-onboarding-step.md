Añade o modifica un paso del flujo de onboarding de TramitUp.

**Pasos:**

1. Lee `frontend/app/onboarding/page.tsx` para entender el flujo actual de steps
2. Lee `backend/app/schemas/me.py` para ver los campos del perfil
3. Define el nuevo step:
   - Posición en el flujo (antes/después de qué step existente)
   - Campos que recoge
   - Validaciones necesarias
4. Modifica `onboarding/page.tsx`:
   - Añade el step al array de pasos
   - Crea el componente de UI del nuevo step
   - Actualiza el índice máximo de pasos en la barra de progreso
5. Si el step recoge nuevos datos, actualiza el schema:
   - `backend/app/schemas/me.py` — añade el campo a ProfileUpdate
   - Supabase `profiles` table — añade la columna (migración)
   - `backend/app/api/v1/endpoints/me.py` — endpoint PATCH /me acepta el nuevo campo
6. Verifica que el campo se guarda en `profiles` al completar el step
7. Si el dato afecta al comportamiento del sistema (ej. categorías de interés → RAG personalizado), verifica esa integración

**Step a añadir:** $ARGUMENTS
