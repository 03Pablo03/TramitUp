# TramitUp

**Entiende tus derechos y cómo ejercerlos.**

TramitUp es una aplicación de información jurídica que ayuda a los ciudadanos españoles a entender la normativa aplicable a su situación y generar modelos de escritos basados en la legislación vigente.

> ⚠️ **Importante:** TramitUp es un servicio de **información jurídica**, no de asesoramiento legal. No prescribimos qué debe hacer el usuario ni garantizamos resultados. Explicamos cómo funciona la normativa y facilitamos modelos de escritos que el usuario debe revisar y presentar por su cuenta.

## 🚀 Quick Start

### Requisitos

- Node.js >= 20
- Python >= 3.12
- Cuenta en [Supabase](https://supabase.com)
- API Key de [Google AI Studio](https://ai.google.dev) (Gemini)
- Docker (opcional, para contenedores)

### Método 1: Setup Automático (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/tramitup.git
cd tramitup

# Ejecutar script de setup
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh

# Editar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Iniciar desarrollo
make dev
```

### Método 2: Setup Manual

#### 1. Configurar Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
cp .env.example .env           # Rellenar con tus keys
uvicorn app.main:app --reload --port 8000
```

#### 2. Configurar Frontend

```bash
cd frontend
npm install
cp .env.example .env.local     # Rellenar con tus keys
npm run dev
```

#### 3. Configurar Base de Datos

1. Crear proyecto en Supabase
2. Ejecutar las migraciones SQL desde `backend/migrations/`
3. Configurar RLS (Row Level Security) según los esquemas

### Método 3: Docker

```bash
# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Construir y ejecutar
docker-compose up --build
```

La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🏗️ Arquitectura

### Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | Next.js 14 + TypeScript + Tailwind CSS |
| Backend | FastAPI (Python 3.12) |
| IA / LLM | Google AI (Gemini) via LangChain |
| Base de datos | Supabase (PostgreSQL + pgvector) |
| Autenticación | Supabase Auth (JWT) |
| Pagos | Stripe |
| Email | Resend |
| Testing | Jest + pytest |

### Componentes Principales

```
TramitUp/
├── frontend/           # Next.js 14 App Router
│   ├── app/           # Páginas y API routes
│   ├── components/    # Componentes React
│   ├── context/       # Context providers
│   ├── hooks/         # Custom hooks
│   ├── lib/           # Utilidades
│   └── types/         # Tipos TypeScript
├── backend/           # FastAPI
│   ├── app/
│   │   ├── api/       # Endpoints
│   │   ├── core/      # Configuración y utilidades
│   │   ├── services/  # Lógica de negocio
│   │   └── ai/        # Cadenas de IA
│   └── tests/         # Tests
└── docs/              # Documentación
```

## 🔧 Funcionalidades

### Core Features

- **Chat Inteligente**: Consultas en lenguaje natural sobre normativa española
- **Generación de Documentos**: Modelos de escritos personalizados
- **Alertas de Plazos**: Recordatorios automáticos de vencimientos legales
- **Autenticación**: Login con Google y Magic Links
- **Planes de Suscripción**: Free, Document y Pro

### Flujos Principales

1. **Onboarding**: Selección de áreas de interés
2. **Chat**: Conversación con IA sobre consultas legales
3. **Documentos**: Generación y descarga de modelos
4. **Alertas**: Gestión de plazos y recordatorios

## 🧪 Testing

### Frontend
```bash
cd frontend
npm test                    # Ejecutar tests
npm run test:watch         # Modo watch
npm run test:coverage      # Con cobertura
```

### Backend
```bash
cd backend
python -m pytest          # Ejecutar tests
python -m pytest -v       # Verbose
python -m pytest --cov    # Con cobertura
```

## 📝 Variables de Entorno

### Backend (.env)
```env
# IA
GOOGLE_API_KEY=your_google_ai_key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
RESEND_API_KEY=re_...

# App
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

## 🚀 Deployment

### Producción

1. **Frontend**: Deploy en Vercel
   ```bash
   vercel --prod
   ```

2. **Backend**: Deploy en Railway/Render
   ```bash
   # Configurar variables de entorno
   # Usar Dockerfile incluido
   ```

3. **Base de Datos**: Supabase en producción

### Staging

- Frontend: Preview deployments automáticos en Vercel
- Backend: Rama `staging` con variables de entorno separadas

## 🔒 Seguridad

- **Autenticación**: JWT tokens con Supabase Auth
- **Autorización**: Row Level Security (RLS) en Supabase
- **Rate Limiting**: Por usuario y plan
- **Validación**: Pydantic en backend, Zod en frontend
- **Headers**: Configuración de seguridad en middleware

## 📊 Monitoreo y Observabilidad

- **Logging**: Estructurado con structlog (JSON en producción)
- **Error Tracking**: Error Boundary + logging centralizado
- **Performance**: Métricas de tiempo de respuesta y throughput
- **Health Checks**: 
  - `/health` - Estado general de la aplicación
  - `/ready` - Readiness check para Kubernetes
  - `/live` - Liveness check para Kubernetes
  - `/metrics` - Métricas detalladas (requiere auth)
- **Monitoring**: Middleware personalizado para captura de métricas

## 🔧 Comandos de Desarrollo

```bash
# Setup inicial
make install              # Instalar todas las dependencias
./scripts/setup-dev.sh    # Setup automático completo

# Desarrollo
make dev                  # Iniciar frontend y backend
make dev-frontend         # Solo frontend
make dev-backend          # Solo backend

# Testing
make test                 # Ejecutar todos los tests
make test-frontend        # Tests del frontend
make test-backend         # Tests del backend
./scripts/run-tests.sh    # Script completo de testing

# Calidad de código
make lint                 # Linting completo
make format               # Formatear código
pre-commit run --all-files # Ejecutar hooks de pre-commit

# Docker
make docker-build         # Construir imágenes
make docker-up            # Levantar servicios
make docker-down          # Parar servicios

# Mantenimiento
make clean                # Limpiar caches y builds
```

## 🚀 CI/CD y DevOps

### GitHub Actions

- **CI Pipeline**: Tests automáticos en PRs y pushes
- **Security Scanning**: Trivy para vulnerabilidades
- **Code Coverage**: Codecov integration
- **Deployment**: Automático a producción desde `main`

### Pre-commit Hooks

- Linting y formateo automático
- Type checking
- Detección de secretos
- Validación de archivos

### Docker Support

- Imágenes optimizadas multi-stage
- Docker Compose para desarrollo local
- Health checks integrados
- Non-root user para seguridad

## 🤝 Contribución

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para guías detalladas de contribución.

### Estándares de Código

- **TypeScript**: Strict mode habilitado
- **Python**: Black + isort + flake8
- **ESLint + Prettier**: Configuración incluida
- **Commits**: Conventional commits
- **Testing**: Cobertura mínima 80%

### Workflow

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commits con mensajes descriptivos
4. Tests para nueva funcionalidad
5. Pull request con descripción detallada

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

- **Documentación**: `/docs` en este repositorio
- **Issues**: GitHub Issues para bugs y features
- **API Docs**: http://localhost:8000/docs (desarrollo)

---

**Desarrollado con ❤️ para simplificar la burocracia española**