"""
Request schemas for API endpoints.
Defines all request models with validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class TransactionInput(BaseModel):
    """Raw transaction for categorization."""
    date: datetime = Field(..., description="Transaction date")
    description: str = Field(..., description="Transaction description", min_length=1)
    amount: float = Field(..., description="Transaction amount")
    
    @validator('description')
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-15T00:00:00",
                "description": "Amazon Prime",
                "amount": -14.99
            }
        }


class CategorizeRequest(BaseModel):
    """Request to categorize transactions."""
    transactions: List[TransactionInput] = Field(..., description="Transactions to categorize")
    
    @validator('transactions')
    def transactions_not_empty(cls, v):
        if not v:
            raise ValueError('At least one transaction is required')
        return v


class AnalyzeRequest(BaseModel):
    """Request for bank statement analysis."""
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    # Note: PDF file is uploaded via multipart/form-data, not JSON
