Implementa un nuevo endpoint en TramitUp siguiendo la arquitectura del proyecto.

**Pasos a seguir:**

1. **Lee** primero los archivos relevantes:
   - `backend/app/api/v1/router.py` — para ver cómo se registran rutas
   - El endpoint más similar al que vas a crear (para seguir el patrón)
   - El service correspondiente si ya existe

2. **Crea o modifica** en este orden:
   a. Schema Pydantic en `backend/app/schemas/` (si hay request/response body)
   b. Lógica de negocio en `backend/app/services/` (función pura, sin HTTP)
   c. Endpoint en `backend/app/api/v1/endpoints/`
   d. Registrar en `backend/app/api/v1/router.py`

3. **Patrones obligatorios:**
   - `user_id: str = Depends(require_auth)` en todos los endpoints auth
   - Try/except con logging y HTTPException apropiado
   - Verificación de propiedad del recurso (`user_id == resource.user_id`)
   - Respuesta: `{"success": True, "data": resultado}`

4. **Para el frontend** (si aplica):
   - Añadir la llamada via `apiFetch("/nueva-ruta")` en el componente
   - Actualizar tipos TypeScript

Ahora implementa: $ARGUMENTS
