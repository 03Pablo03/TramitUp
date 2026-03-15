"""
Monitoring and observability utilities for TramitUp backend.
"""

import time
from typing import Dict, Any, Optional
from functools import wraps
from contextlib import contextmanager

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


class MetricsCollector:
    """Simple in-memory metrics collector."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "requests_total": 0,
            "requests_by_endpoint": {},
            "requests_by_status": {},
            "response_times": [],
            "errors_total": 0,
            "active_users": set(),
        }
    
    def record_request(self, endpoint: str, method: str, status_code: int, response_time: float, user_id: Optional[str] = None):
        """Record request metrics."""
        self.metrics["requests_total"] += 1
        
        endpoint_key = f"{method} {endpoint}"
        self.metrics["requests_by_endpoint"][endpoint_key] = self.metrics["requests_by_endpoint"].get(endpoint_key, 0) + 1
        
        self.metrics["requests_by_status"][status_code] = self.metrics["requests_by_status"].get(status_code, 0) + 1
        
        self.metrics["response_times"].append(response_time)
        # Keep only last 1000 response times
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
        
        if status_code >= 400:
            self.metrics["errors_total"] += 1
        
        if user_id:
            self.metrics["active_users"].add(user_id)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        response_times = self.metrics["response_times"]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "requests_total": self.metrics["requests_total"],
            "requests_by_endpoint": self.metrics["requests_by_endpoint"],
            "requests_by_status": self.metrics["requests_by_status"],
            "errors_total": self.metrics["errors_total"],
            "error_rate": self.metrics["errors_total"] / max(self.metrics["requests_total"], 1),
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "active_users_count": len(self.metrics["active_users"]),
        }
    
    def reset(self):
        """Reset metrics (useful for testing)."""
        self.__init__()


# Global metrics collector instance
metrics_collector = MetricsCollector()


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to collect request metrics and logs."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Extract user ID from request if available
        user_id = getattr(request.state, 'user_id', None)
        
        response = await call_next(request)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Record metrics
        endpoint = request.url.path
        method = request.method
        status_code = response.status_code
        
        metrics_collector.record_request(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time=response_time,
            user_id=user_id
        )
        
        # Log request
        logger.info(
            "request_completed",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            response_time_ms=round(response_time * 1000, 2),
            user_id=user_id,
        )
        
        return response


def monitor_function(func_name: Optional[str] = None):
    """Decorator to monitor function execution."""
    def decorator(func):
        name = func_name or f"{func.__module__}.{func.__name__}"
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(
                    "function_completed",
                    function=name,
                    duration_ms=round(duration * 1000, 2),
                    success=True
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "function_failed",
                    function=name,
                    duration_ms=round(duration * 1000, 2),
                    error=str(e),
                    success=False
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(
                    "function_completed",
                    function=name,
                    duration_ms=round(duration * 1000, 2),
                    success=True
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "function_failed",
                    function=name,
                    duration_ms=round(duration * 1000, 2),
                    error=str(e),
                    success=False
                )
                raise
        
        return async_wrapper if hasattr(func, '__await__') else sync_wrapper
    return decorator


@contextmanager
def monitor_operation(operation_name: str, **context):
    """Context manager to monitor operations."""
    start_time = time.time()
    logger.info("operation_started", operation=operation_name, **context)
    
    try:
        yield
        duration = time.time() - start_time
        logger.info(
            "operation_completed",
            operation=operation_name,
            duration_ms=round(duration * 1000, 2),
            success=True,
            **context
        )
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "operation_failed",
            operation=operation_name,
            duration_ms=round(duration * 1000, 2),
            error=str(e),
            success=False,
            **context
        )
        raise


def get_health_status() -> Dict[str, Any]:
    """Get application health status."""
    try:
        # Basic health checks
        metrics = metrics_collector.get_metrics()
        
        # Check if error rate is too high
        error_rate_threshold = 0.1  # 10%
        is_healthy = metrics["error_rate"] < error_rate_threshold
        
        # Check if average response time is acceptable
        response_time_threshold = 5000  # 5 seconds
        is_responsive = metrics["avg_response_time_ms"] < response_time_threshold
        
        status = "healthy" if is_healthy and is_responsive else "degraded"
        
        return {
            "status": status,
            "timestamp": time.time(),
            "version": "1.0.0",
            "environment": settings.environment,
            "metrics": metrics,
            "checks": {
                "error_rate_ok": is_healthy,
                "response_time_ok": is_responsive,
            }
        }
    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "error": str(e)
        }