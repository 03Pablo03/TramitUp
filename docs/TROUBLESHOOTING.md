# Guía de Troubleshooting

Esta guía te ayudará a resolver los problemas más comunes en TramitUp.

## 🚨 Problemas Comunes

### 1. Error 502 en Chat

**Síntoma**: El chat devuelve error 502 "Bad Gateway"

**Causas posibles**:
- Backend no está ejecutándose
- Backend no es accesible desde el frontend
- Configuración incorrecta de BACKEND_URL

**Soluciones**:

1. **Verificar que el backend esté ejecutándose**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. **Verificar conectividad**:
   ```bash
   curl http://localhost:8000/health
   # Debería devolver: {"status": "ok", "service": "tramitup-api"}
   ```

3. **Verificar configuración en frontend**:
   ```typescript
   // En frontend/app/api/backend/[[...path]]/route.ts
   const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";
   ```

4. **Verificar logs del backend**:
   ```bash
   # Buscar errores en la consola del backend
   # Verificar que no hay errores de CORS
   ```

### 2. Error de Autenticación (401)

**Síntoma**: "No autorizado" en requests a la API

**Causas posibles**:
- Token JWT expirado o inválido
- Configuración incorrecta de Supabase
- Problemas con cookies

**Soluciones**:

1. **Verificar configuración de Supabase**:
   ```env
   # Frontend (.env.local)
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
   
   # Backend (.env)
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   SUPABASE_JWT_SECRET=your_jwt_secret
   ```

2. **Verificar JWT Secret**:
   - Ve a tu proyecto en Supabase
   - Settings > API > JWT Secret
   - Copia el valor exacto (sin espacios ni comillas)

3. **Limpiar cookies y reloguear**:
   ```javascript
   // En DevTools Console
   document.cookie.split(";").forEach(c => {
     document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
   });
   ```

4. **Verificar middleware de autenticación**:
   ```bash
   # Verificar que el middleware.ts está funcionando
   # Revisar logs del servidor Next.js
   ```

### 3. Error de Conexión con Supabase

**Síntoma**: Errores de conexión o timeout con Supabase

**Soluciones**:

1. **Verificar health check**:
   ```bash
   curl http://localhost:8000/health/supabase
   ```

2. **Verificar configuración**:
   ```python
   # En backend, verificar que la URL no tenga barra final
   SUPABASE_URL=https://your-project.supabase.co  # ✅ Correcto
   SUPABASE_URL=https://your-project.supabase.co/ # ❌ Incorrecto
   ```

3. **Verificar permisos de Service Role**:
   - El Service Role Key debe tener permisos completos
   - Verificar en Supabase Dashboard > Settings > API

### 4. Error de Rate Limit

**Síntoma**: "Has usado tus consultas gratuitas de hoy"

**Soluciones**:

1. **Verificar plan del usuario**:
   ```sql
   -- En Supabase SQL Editor
   SELECT plan FROM profiles WHERE id = 'user-id';
   ```

2. **Reset manual del rate limit**:
   ```sql
   -- Solo para testing/debugging
   UPDATE profiles 
   SET last_reset_date = CURRENT_DATE - INTERVAL '1 day'
   WHERE id = 'user-id';
   ```

3. **Verificar lógica de rate limiting**:
   ```python
   # En backend/app/core/rate_limit.py
   # Verificar que las fechas se comparan correctamente
   ```

### 5. Problemas de Compilación

**Frontend**:
```bash
# Limpiar cache
rm -rf .next node_modules package-lock.json
npm install
npm run build

# Verificar tipos
npx tsc --noEmit
```

**Backend**:
```bash
# Verificar sintaxis Python
python -m py_compile app/main.py

# Verificar imports
python -c "from app.main import app; print('OK')"
```

### 6. Problemas con Google AI

**Síntoma**: Errores en el chat relacionados con IA

**Soluciones**:

1. **Verificar API Key**:
   ```bash
   # Test directo de la API
   curl -H "Content-Type: application/json" \
        -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY"
   ```

2. **Verificar cuota y límites**:
   - Ve a Google AI Studio
   - Verifica que no hayas excedido los límites

3. **Verificar configuración en backend**:
   ```python
   # En app/core/config.py
   google_api_key: str  # Debe estar configurado
   ```

## 🔧 Herramientas de Debugging

### 1. Logs del Backend

```bash
# Ejecutar con logs detallados
PYTHONPATH=. python -m uvicorn app.main:app --reload --log-level debug

# Verificar logs estructurados
tail -f logs/app.log | jq '.'  # Si usas archivos de log
```

### 2. Logs del Frontend

```javascript
// En DevTools Console
localStorage.setItem('debug', 'tramitup:*');
// Recargar página para ver logs detallados
```

### 3. Network Inspector

1. Abrir DevTools > Network
2. Filtrar por "backend" para ver calls a la API
3. Verificar:
   - Status codes
   - Request headers (Authorization)
   - Response bodies
   - Timing

### 4. Database Queries

```sql
-- Verificar usuario
SELECT * FROM auth.users WHERE email = 'user@example.com';

-- Verificar perfil
SELECT * FROM profiles WHERE id = 'user-id';

-- Verificar conversaciones
SELECT * FROM conversations WHERE user_id = 'user-id' ORDER BY created_at DESC;

-- Verificar alertas
SELECT * FROM alerts WHERE user_id = 'user-id';
```

## 🚀 Performance Issues

### 1. Chat Lento

**Diagnóstico**:
```bash
# Verificar tiempo de respuesta
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/health"

# Donde curl-format.txt contiene:
#     time_namelookup:  %{time_namelookup}\n
#     time_connect:     %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#     time_pretransfer: %{time_pretransfer}\n
#     time_redirect:    %{time_redirect}\n
#     time_starttransfer: %{time_starttransfer}\n
#     time_total:       %{time_total}\n
```

**Soluciones**:
- Verificar que el caché esté funcionando
- Optimizar prompts de IA
- Verificar conectividad con Google AI

### 2. Frontend Lento

**Diagnóstico**:
```bash
# Analizar bundle
npm run build
npx @next/bundle-analyzer
```

**Soluciones**:
- Lazy loading de componentes pesados
- Optimización de imágenes
- Code splitting

## 🔍 Debugging Específico por Componente

### AuthContext

```typescript
// Añadir logs temporales
useEffect(() => {
  console.log('Auth state:', { user, session, loading });
}, [user, session, loading]);
```

### Chat SSE

```typescript
// Verificar eventos SSE
const eventSource = new EventSource('/api/backend/chat');
eventSource.onmessage = (event) => {
  console.log('SSE Event:', event.data);
};
eventSource.onerror = (error) => {
  console.error('SSE Error:', error);
};
```

### Supabase Queries

```typescript
// Añadir logging a queries
const { data, error } = await supabase
  .from('profiles')
  .select('*')
  .eq('id', userId);

console.log('Supabase query:', { data, error });
```

## 📱 Problemas Específicos por Plataforma

### Windows

1. **Problemas con PowerShell**:
   ```powershell
   # Usar cmd en lugar de PowerShell si hay problemas
   cmd /c "npm run dev"
   ```

2. **Problemas con paths**:
   ```bash
   # Usar barras normales en paths
   cd frontend && npm run dev  # ❌ Puede fallar en PowerShell
   cd frontend; npm run dev    # ✅ Mejor en PowerShell
   ```

### Mac/Linux

1. **Problemas de permisos**:
   ```bash
   chmod +x scripts/setup.sh
   ```

2. **Variables de entorno**:
   ```bash
   export GOOGLE_API_KEY="your-key"
   # En lugar de set GOOGLE_API_KEY=your-key
   ```

## 🆘 Cuándo Pedir Ayuda

Si después de seguir esta guía el problema persiste:

1. **Recopilar información**:
   - Logs completos del error
   - Pasos exactos para reproducir
   - Versiones de Node.js, Python, etc.
   - Sistema operativo

2. **Crear un issue en GitHub** con:
   - Descripción clara del problema
   - Información del entorno
   - Logs relevantes
   - Lo que ya has intentado

3. **Información útil para incluir**:
   ```bash
   # Versiones
   node --version
   npm --version
   python --version
   
   # Estado del sistema
   curl http://localhost:8000/health
   curl http://localhost:3000/api/health
   
   # Logs recientes
   tail -n 50 logs/error.log
   ```

---

¿No encuentras tu problema aquí? [Crear un issue](https://github.com/tramitup/tramitup/issues/new) con los detalles.