"""
Health check endpoint.
"""

from fastapi import APIRouter
from datetime import datetime
import os

from backend.api.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and version information.
    """
    # Check OCR service availability
    ocr_service_url = os.getenv("OCR_SERVICE_URL", "http://localhost:8001")
    ocr_status = "available"  # TODO: Implement actual health check
    
    # Check database connection
    db_status = "connected"  # TODO: Implement actual DB check
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "ocr_service": ocr_status,
            "database": db_status
        },
        timestamp=datetime.utcnow()
    )
