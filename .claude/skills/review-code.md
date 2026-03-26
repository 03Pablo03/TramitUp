Realiza una revisión de código completa de los cambios recientes en TramitUp.

**Proceso de revisión:**

### 1. Identifica los cambios a revisar
```bash
git diff main..HEAD --name-only  # archivos modificados
git log main..HEAD --oneline     # commits recientes
```

### 2. Lee los archivos modificados
Para cada archivo cambiado, verifica:

**Seguridad:**
- [ ] Sin credenciales hardcodeadas
- [ ] Endpoints con `require_auth` donde es necesario
- [ ] Filtrado por `user_id` en todas las queries
- [ ] Validación de inputs con Pydantic/TypeScript
- [ ] Sin XSS (dangerouslySetInnerHTML, innerHTML)

**Correctitud:**
- [ ] La lógica implementada coincide con la especificación
- [ ] Manejo de errores adecuado (try/catch, HTTPException)
- [ ] Sin estados inconsistentes en el frontend
- [ ] TypeScript sin `any` explícito

**Performance:**
- [ ] Sin SELECT * innecesarios
- [ ] Sin N+1 queries
- [ ] Fetches paralelos donde sea posible
- [ ] Sin console.log en código de producción

**Convenciones TramitUp:**
- [ ] Frontend usa `apiFetch()` en lugar de fetch directo
- [ ] Backend usa `from app.core.auth import require_auth`
- [ ] TypeScript usa `Array.from(new Set(...))` para conjuntos
- [ ] Errores backend via `HTTPException`, frontend via state `error`

### 3. Genera el informe
Clasifica cada hallazgo como:
- 🔴 **Crítico**: bug o vulnerabilidad de seguridad — requiere fix inmediato
- 🟡 **Medio**: problema de calidad o performance — fix antes de deploy
- 🟢 **Bajo**: sugerencia de mejora — opcional

**Código a revisar:** $ARGUMENTS
