"""
Global exception handlers for FastAPI application.
"""
from typing import Any, Dict
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger, log_error


logger = get_logger(__name__)


class TramitUpException(Exception):
    """Base exception for TramitUp application."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(TramitUpException):
    """Authentication related errors."""
    
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(TramitUpException):
    """Authorization related errors."""
    
    def __init__(self, message: str = "No tienes permisos para esta acción"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ValidationError(TramitUpException):
    """Validation related errors."""
    
    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)


class NotFoundError(TramitUpException):
    """Resource not found errors."""
    
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class RateLimitError(TramitUpException):
    """Rate limiting errors."""
    
    def __init__(self, message: str = "Has superado el límite de solicitudes"):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS)


class ExternalServiceError(TramitUpException):
    """External service errors."""
    
    def __init__(self, service: str, message: str = "Error en servicio externo"):
        super().__init__(f"{service}: {message}", status.HTTP_502_BAD_GATEWAY)
        self.service = service


async def tramitup_exception_handler(request: Request, exc: TramitUpException) -> JSONResponse:
    """Handle custom TramitUp exceptions."""
    log_error(
        logger,
        exc,
        context={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
        },
        user_id=getattr(request.state, "user_id", None),
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    log_error(
        logger,
        exc,
        context={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
        },
        user_id=getattr(request.state, "user_id", None),
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    logger.warning(
        "Validation error",
        path=request.url.path,
        method=request.method,
        errors=exc.errors(),
        user_id=getattr(request.state, "user_id", None),
    )
    
    # Format validation errors for better UX
    formatted_errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        formatted_errors.append(f"{field}: {error['msg']}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Datos de entrada inválidos",
            "details": {
                "validation_errors": formatted_errors,
                "raw_errors": exc.errors(),
            },
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    log_error(
        logger,
        exc,
        context={
            "path": request.url.path,
            "method": request.method,
            "exception_type": type(exc).__name__,
        },
        user_id=getattr(request.state, "user_id", None),
    )
    
    # Don't expose internal errors in production
    from app.core.config import get_settings
    settings = get_settings()
    
    if settings.environment == "development":
        error_message = str(exc)
    else:
        error_message = "Error interno del servidor"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": error_message},
    )