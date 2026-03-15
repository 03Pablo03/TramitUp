"""
Monitoring and health check endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.monitoring import get_health_status, metrics_collector
from app.core.auth import require_auth

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for load balancers and monitoring systems.
    
    Returns:
        Dict containing health status and basic metrics
    """
    return get_health_status()


@router.get("/metrics")
async def get_metrics(current_user=Depends(require_auth)) -> Dict[str, Any]:
    """
    Get application metrics (requires authentication).
    
    Returns:
        Dict containing detailed application metrics
    """
    return metrics_collector.get_metrics()


@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check for Kubernetes deployments.
    
    Returns:
        Simple ready status
    """
    # Add more sophisticated readiness checks here
    # (database connectivity, external service availability, etc.)
    return {"status": "ready"}


@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes deployments.
    
    Returns:
        Simple alive status
    """
    return {"status": "alive"}