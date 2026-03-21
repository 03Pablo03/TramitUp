from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.config import get_settings
from app.core.logging import configure_logging, LoggingMiddleware
from app.core.monitoring import MonitoringMiddleware
from app.core.exceptions import (
    TramitUpException,
    tramitup_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.api.v1.router import api_router
from app.api.v1.endpoints.monitoring import router as monitoring_router


def create_app() -> FastAPI:
    # Configure logging first
    configure_logging()
    
    app = FastAPI(
        title="TramitUp API",
        description="API de información jurídica - Entiende tus derechos y cómo ejercerlos",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add exception handlers
    app.add_exception_handler(TramitUpException, tramitup_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    settings = get_settings()

    # CORS: en producción solo el dominio configurado; en desarrollo también localhost
    allowed_origins = [settings.frontend_url] if settings.frontend_url else []
    if not settings.is_production:
        allowed_origins += [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
        ]
    # Eliminar duplicados preservando orden
    seen: set[str] = set()
    cors_origins: list[str] = []
    for o in allowed_origins:
        if o and o not in seen:
            seen.add(o)
            cors_origins.append(o)

    # Add middleware
    app.add_middleware(MonitoringMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(monitoring_router, prefix="", tags=["monitoring"])
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()


# Legacy health check endpoint (kept for backward compatibility)
@app.get("/health-legacy")
def health_check_legacy():
    return {"status": "ok", "service": "tramitup-api"}


@app.get("/health/supabase")
def health_supabase():
    """Comprueba si el backend puede conectar con Supabase."""
    try:
        from app.core.supabase_client import get_supabase_client
        from app.core.config import get_settings
        settings = get_settings()
        if not settings.supabase_url:
            return {"ok": False, "error": "SUPABASE_URL no configurada en .env"}
        supabase = get_supabase_client()
        supabase.table("profiles").select("id").limit(1).execute()
        return {"ok": True, "supabase": "conectado", "url": settings.supabase_url}
    except Exception as e:
        return {"ok": False, "error": str(e), "supabase": "no conecta"}
