"""
Response schemas for API endpoints.
Defines all response models with proper typing.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    services: Dict[str, str] = Field(..., description="Service statuses")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalysisSummary(BaseModel):
    """Summary of financial metrics."""
    total_income: float = Field(..., description="Total income")
    total_expenses: float = Field(..., description="Total expenses")
    net_income: float = Field(..., description="Net income (income - expenses)")
    savings_rate: float = Field(..., description="Savings rate as percentage")
    debt_to_income_ratio: float = Field(..., description="Debt to income ratio")


class TransactionResponse(BaseModel):
    """Transaction with categorization."""
    id: str
    date: datetime
    description: str
    amount: float
    category: str
    confidence: Optional[float] = None


class AnalysisResponse(BaseModel):
    """Complete financial analysis response."""
    analysis_id: str = Field(..., description="Unique analysis ID")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    status: str = Field(..., description="Processing status")
    
    summary: AnalysisSummary = Field(..., description="Financial summary")
    transactions: List[Dict[str, Any]] = Field(..., description="All transactions")
    debt_accounts: List[Dict[str, Any]] = Field(..., description="Debt accounts")
    
    analysis: Dict[str, Any] = Field(..., description="Agent analysis results")
    
    errors: List[str] = Field(default_factory=list, description="Processing errors")
    warnings: List[str] = Field(default_factory=list, description="Warnings")
    
    class Config:
        schema_extra = {
            "example": {
                "analysis_id": "uuid-here",
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "complete",
                "summary": {
                    "total_income": 5000.00,
                    "total_expenses": 3500.00,
                    "net_income": 1500.00,
                    "savings_rate": 30.0,
                    "debt_to_income_ratio": 100.0
                },
                "transactions": [],
                "debt_accounts": [],
                "analysis": {
                    "debt": {},
                    "savings": {},
                    "budget": {},
                    "risk": {}
                },
                "errors": [],
                "warnings": []
            }
        }


class OCRResponse(BaseModel):
    """OCR extraction response."""
    text: str = Field(..., description="Extracted text")
    method: str = Field(..., description="OCR method used")
    pages: int = Field(..., description="Number of pages processed")
    confidence: Optional[float] = Field(None, description="OCR confidence score")


class ErrorResponse(BaseModel):
    """Error response."""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    detail: Optional[str] = Field(None, description="Detailed error information")
