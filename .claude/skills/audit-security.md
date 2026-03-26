Realiza una auditoría de seguridad del código de TramitUp.

**Checklist de seguridad:**

### Backend (FastAPI)

**Autenticación y autorización:**
- [ ] Todos los endpoints sensibles usan `Depends(require_auth)` — busca endpoints sin auth
- [ ] Todos los endpoints filtran por `user_id` del token, no de la URL/body
- [ ] No hay endpoints que permitan acceder a datos de otros usuarios
- [ ] `get_current_user_id` no se usa donde debería estar `require_auth`

**Validación de inputs:**
- [ ] Sin `eval()`, `exec()`, o ejecución de código dinámico
- [ ] Sin interpolación directa de inputs en queries SQL
- [ ] Whitelists para campos enum (VALID_STATUSES, VALID_CATEGORIES)
- [ ] Límites de longitud en campos de texto (title[:120], summary[:1000])
- [ ] Validación de tipos con Pydantic en todos los endpoints

**Secretos y configuración:**
- [ ] Sin credenciales hardcodeadas — busca `sk_live`, `Bearer `, passwords en código
- [ ] Variables de entorno validadas en `config.py`
- [ ] `ENVIRONMENT=production` deshabilita Swagger docs
- [ ] Webhook de Stripe verifica firma (`stripe.Webhook.construct_event`)

**CORS y headers:**
- [ ] CORS solo permite dominios conocidos (no `*` en producción)
- [ ] Headers de seguridad configurados (HSTS, X-Frame-Options)

### Frontend (Next.js)

**XSS:**
- [ ] Sin `dangerouslySetInnerHTML` con datos del usuario
- [ ] Sin `innerHTML` con contenido no sanitizado
- [ ] Markdown renderizado con sanitización (DOMPurify o similar)

**Auth:**
- [ ] `apiFetch()` siempre incluye el token — sin fetch directo sin auth
- [ ] No hay tokens en localStorage — usar cookies HttpOnly de Supabase
- [ ] Middleware protege todas las rutas que requieren auth

**Datos sensibles:**
- [ ] Sin `console.log` con datos de usuario en producción
- [ ] Sin datos sensibles en URLs (parámetros de query)
- [ ] Variables de entorno `NEXT_PUBLIC_*` no incluyen secretos

### Resultado
Genera un informe con: hallazgos críticos, hallazgos medios, recomendaciones.

**Alcance de la auditoría:** $ARGUMENTS
