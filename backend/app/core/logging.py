"""
Logging configuration for TramitUp backend.
"""
import logging
import sys
from typing import Any, Dict

import structlog
from structlog.types import Processor

from app.core.config import get_settings


def configure_logging() -> None:
    """Configure structured logging for the application."""
    settings = get_settings()
    
    # Configure structlog
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    
    if settings.environment == "development":
        # Pretty console output for development
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=True),
        ])
    else:
        # JSON output for production
        processors.extend([
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ])
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO if settings.environment == "production" else logging.DEBUG
        ),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO if settings.environment == "production" else logging.DEBUG,
    )


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


class LoggingMiddleware:
    """Middleware for logging HTTP requests and responses."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("http")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request_id = scope.get("request_id", "unknown")
        method = scope["method"]
        path = scope["path"]
        
        # Log request
        self.logger.info(
            "Request started",
            request_id=request_id,
            method=method,
            path=path,
            user_agent=dict(scope.get("headers", {})).get(b"user-agent", b"").decode(),
        )
        
        # Wrap send to capture response status
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                self.logger.info(
                    "Request completed",
                    request_id=request_id,
                    method=method,
                    path=path,
                    status_code=status_code,
                )
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


def log_error(
    logger: structlog.BoundLogger,
    error: Exception,
    context: Dict[str, Any] | None = None,
    user_id: str | None = None,
) -> None:
    """Log an error with structured context."""
    log_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
    
    if context:
        log_data.update(context)
    
    if user_id:
        log_data["user_id"] = user_id
    
    logger.error("Application error", **log_data, exc_info=True)


def log_api_call(
    logger: structlog.BoundLogger,
    service: str,
    operation: str,
    user_id: str | None = None,
    **kwargs
) -> None:
    """Log an external API call."""
    log_data = {
        "service": service,
        "operation": operation,
    }
    
    if user_id:
        log_data["user_id"] = user_id
    
    log_data.update(kwargs)
    
    logger.info("External API call", **log_data)


def log_business_event(
    logger: structlog.BoundLogger,
    event: str,
    user_id: str | None = None,
    **kwargs
) -> None:
    """Log a business event."""
    log_data = {
        "event": event,
    }
    
    if user_id:
        log_data["user_id"] = user_id
    
    log_data.update(kwargs)
    
    logger.info("Business event", **log_data)