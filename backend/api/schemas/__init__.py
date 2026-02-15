"""
API schemas package.
"""

from .requests import (
    TransactionInput,
    CategorizeRequest,
    AnalyzeRequest,
)

from .responses import (
    HealthResponse,
    AnalysisSummary,
    TransactionResponse,
    AnalysisResponse,
    OCRResponse,
    ErrorResponse,
)

__all__ = [
    # Requests
    "TransactionInput",
    "CategorizeRequest",
    "AnalyzeRequest",
    # Responses
    "HealthResponse",
    "AnalysisSummary",
    "TransactionResponse",
    "AnalysisResponse",
    "OCRResponse",
    "ErrorResponse",
]
