"""
Error handling middleware.
Global exception handlers for the API.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions with proper response format.
    
    Args:
        request: FastAPI request
        exc: HTTP exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all unhandled exceptions.
    
    Args:
        request: FastAPI request
        exc: Exception
        
    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {exc}")
    logger.exception(exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "detail": str(exc),
            "path": str(request.url)
        }
    )


def add_error_handlers(app):
    """
    Add all error handlers to FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
