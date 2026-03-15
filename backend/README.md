# TramitUp Backend

Backend de TramitUp desarrollado con FastAPI, Python 3.12 y integración con Google AI (Gemini).

## 🚀 Desarrollo

### Instalación

```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### Variables de Entorno

Copia `.env.example` a `.env` y configura:

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

### Comandos

```bash
uvicorn app.main:app --reload --port 8000  # Servidor de desarrollo
python -m pytest                          # Tests
python -m pytest --cov                    # Tests con cobertura
python -m pytest -v                       # Tests verbose
```

## 🏗️ Arquitectura

### Estructura de Carpetas

```
backend/
├── app/
│   ├── api/                   # Endpoints de la API
│   │   └── v1/
│   │       ├── endpoints/     # Endpoints específicos
│   │       └── router.py      # Router principal
│   ├── core/                  # Configuración y utilidades core
│   │   ├── auth.py           # Autenticación JWT
│   │   ├── config.py         # Configuración con Pydantic
│   │   ├── exceptions.py     # Exception handlers
│   │   ├── logging.py        # Logging estructurado
│   │   └── cache.py          # Sistema de caché
│   ├── services/             # Lógica de negocio
│   │   ├── chat_service.py   # Servicio de chat
│   │   ├── subscription_service.py
│   │   └── ...
│   ├── ai/                   # Cadenas de IA
│   │   ├── chains/           # LangChain chains
│   │   └── prompts/          # Templates de prompts
│   ├── schemas/              # Modelos Pydantic
│   └── main.py               # Aplicación FastAPI
├── tests/                    # Tests
├── migrations/               # Migraciones SQL
└── requirements.txt          # Dependencias
```

### Patrones de Arquitectura

#### 1. Dependency Injection
```python
from fastapi import Depends
from app.core.auth import require_auth

@router.post("/chat")
async def chat(
    request: ChatRequest,
    user_id: str = Depends(require_auth)
):
    # user_id inyectado automáticamente
    pass
```

#### 2. Service Layer
```python
# services/chat_service.py
def run_chat(user_id: str, message: str, conversation_id: str | None = None):
    """Lógica de negocio separada del endpoint."""
    # Validaciones
    # Llamadas a IA
    # Persistencia
    return conversation_id, classification, stream
```

#### 3. Exception Handling
```python
# core/exceptions.py
class TramitUpException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

# Manejador global
@app.exception_handler(TramitUpException)
async def tramitup_exception_handler(request: Request, exc: TramitUpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
```

## 🔐 Autenticación

### JWT con Supabase
```python
import jwt
from fastapi import HTTPException

def _verify_jwt(token: str) -> dict | None:
    """Verifica JWT de Supabase."""
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            audience="authenticated",
            algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError:
        return None

async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Dependency que requiere autenticación válida."""
    if not credentials:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    payload = _verify_jwt(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return payload["sub"]  # user_id
```

## 🤖 Integración con IA

### Google AI (Gemini)
```python
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuración
genai.configure(api_key=settings.google_api_key)

# Chat con streaming
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,
    streaming=True
)

# Uso en cadenas
def create_chat_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente legal especializado en normativa española..."),
        ("human", "{input}")
    ])
    
    return prompt | llm | StrOutputParser()
```

### Streaming con Server-Sent Events
```python
from sse_starlette.sse import EventSourceResponse

async def generate_sse(user_id: str, request: ChatRequest):
    """Generador SSE para streaming de chat."""
    # Verificar rate limit
    allowed, _ = check_rate_limit(user_id, get_user_plan(user_id))
    if not allowed:
        yield {"data": json.dumps([{"type": "error", "message": "Rate limit exceeded"}])}
        return
    
    # Ejecutar cadena de IA
    conv_id, classification, stream = run_chat(user_id, request.message)
    
    yield {"data": json.dumps([{"type": "conversation_id", "id": conv_id}])}
    yield {"data": json.dumps([{"type": "classification", "category": classification}])}
    
    for chunk in stream:
        yield {"data": json.dumps([{"type": "chunk", "content": chunk}])}

@router.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(require_auth)):
    return EventSourceResponse(
        generate_sse(user_id, request),
        media_type="text/event-stream"
    )
```

## 💾 Base de Datos

### Supabase Integration
```python
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """Cliente Supabase con service role."""
    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )

# Uso en servicios
def get_user_profile(user_id: str) -> dict | None:
    supabase = get_supabase_client()
    result = supabase.table("profiles").select("*").eq("id", user_id).execute()
    return result.data[0] if result.data else None
```

### Caché
```python
from app.core.cache import cached

@cached(ttl=300, key_prefix="user_profile")
def get_user_plan(user_id: str) -> str:
    """Obtiene plan del usuario con caché de 5 minutos."""
    # Lógica de base de datos
    pass
```

## 📊 Logging y Monitoreo

### Logging Estructurado
```python
import structlog
from app.core.logging import get_logger

logger = get_logger(__name__)

@router.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(require_auth)):
    logger.info(
        "Chat request started",
        user_id=user_id,
        message_length=len(request.message),
        conversation_id=request.conversation_id
    )
    
    try:
        result = await process_chat(request, user_id)
        logger.info("Chat request completed", user_id=user_id, success=True)
        return result
    except Exception as e:
        logger.error(
            "Chat request failed",
            user_id=user_id,
            error=str(e),
            exc_info=True
        )
        raise
```

### Health Checks
```python
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "tramitup-api"}

@app.get("/health/supabase")
def health_supabase():
    """Verifica conectividad con Supabase."""
    try:
        supabase = get_supabase_client()
        supabase.table("profiles").select("id").limit(1).execute()
        return {"ok": True, "supabase": "connected"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
```

## 🧪 Testing

### Configuración
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}

@pytest.fixture
def mock_supabase():
    with patch('app.core.supabase_client.get_supabase_client') as mock:
        yield mock
```

### Tests de Endpoints
```python
def test_chat_endpoint_success(client, auth_headers, mock_supabase):
    """Test successful chat request."""
    # Mock Supabase responses
    mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value = {
        "data": [{"plan": "free"}]
    }
    
    response = client.post(
        "/api/v1/chat",
        json={"message": "Test message"},
        headers=auth_headers
    )
    
    assert response.status_code == 200

def test_chat_endpoint_unauthorized(client):
    """Test chat without authentication."""
    response = client.post("/api/v1/chat", json={"message": "Test"})
    assert response.status_code == 401
```

### Tests de Servicios
```python
from app.services.subscription_service import get_user_plan

def test_get_user_plan_free_user(mock_supabase):
    """Test getting plan for free user."""
    mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value = {
        "data": [{"plan": "free"}]
    }
    
    plan = get_user_plan("user-123")
    assert plan == "free"

def test_get_user_plan_no_user(mock_supabase):
    """Test getting plan for non-existent user."""
    mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value = {
        "data": []
    }
    
    plan = get_user_plan("non-existent")
    assert plan == "free"  # Default fallback
```

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Railway/Render
```bash
# Configurar variables de entorno en la plataforma
# Usar el Dockerfile incluido
# Configurar health check en /health
```

## ⚡ Performance

### Rate Limiting
```python
from app.core.rate_limit import check_rate_limit, consume_rate_limit

def check_rate_limit(user_id: str, plan: str) -> tuple[bool, int]:
    """Verifica si el usuario puede hacer más requests."""
    limit = get_daily_limit(plan)
    used = get_usage_today(user_id)
    return used < limit, limit - used

def consume_rate_limit(user_id: str, plan: str) -> None:
    """Consume un request del límite diario."""
    # Incrementar contador en base de datos
    pass
```

### Caché
```python
from app.core.cache import cached, invalidate_cache_pattern

@cached(ttl=300)  # 5 minutos
def expensive_operation(param: str):
    # Operación costosa
    pass

# Invalidar caché cuando sea necesario
invalidate_cache_pattern("user_profile")
```

## 🔧 Configuración

### Pydantic Settings
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str
    supabase_url: str
    environment: str = "development"
    
    # Performance settings
    max_chat_length: int = 2000
    rate_limit_free: int = 2
    rate_limit_pro: int = 100
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = ["development", "test", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    class Config:
        env_file = ".env"
```

## 🐛 Debugging

### Logs en Desarrollo
```python
import structlog

logger = structlog.get_logger(__name__)

# En desarrollo, logs coloridos
if settings.environment == "development":
    structlog.configure(
        processors=[
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    )
```

### Error Tracking
```python
from app.core.exceptions import log_error

try:
    result = risky_operation()
except Exception as e:
    log_error(
        logger,
        e,
        context={"operation": "risky_operation", "user_id": user_id}
    )
    raise
```

---

Para más información, consulta la documentación principal del proyecto.