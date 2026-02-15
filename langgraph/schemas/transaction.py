"""
Transaction model for financial data.
Represents individual financial transactions.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4


class Transaction(BaseModel):
    """Individual financial transaction."""
    
    # Identity
    id: str = Field(default_factory=lambda: str(uuid4()))
    date: datetime
    description: str
    
    # Amounts
    amount: float
    currency: str = "USD"
    
    # Categorization
    category: str
    expense_type: Optional[str] = None  # Fixed/Variable/Discretionary
    
    # Metadata
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    is_recurring: bool = False
    merchant: Optional[str] = None
    
    @field_validator('amount')
    @classmethod
    def amount_must_be_nonzero(cls, v):
        """Validate that amount is non-zero."""
        if v == 0:
            raise ValueError('Transaction amount cannot be zero')
        return v
    
    @field_validator('date')
    @classmethod
    def date_must_be_past_or_present(cls, v):
        """Validate that date is not in the future."""
        if v > datetime.now():
            raise ValueError('Transaction date cannot be in the future')
        return v
    
    @field_validator('confidence')
    @classmethod
    def confidence_in_range(cls, v):
        """Validate confidence is between 0 and 1."""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "date": "2024-01-15T10:30:00",
                "description": "Amazon Prime Monthly",
                "amount": -14.99,
                "currency": "USD",
                "category": "Entertainment",
                "expense_type": "Fixed",
                "confidence": 0.95,
                "is_recurring": True,
                "merchant": "Amazon"
            }
        }
