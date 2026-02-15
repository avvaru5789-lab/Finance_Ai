"""
Debt account model for credit cards, loans, and other debts.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4


class DebtAccount(BaseModel):
    """Credit card, loan, or other debt account."""
    
    # Identity
    account_id: str = Field(default_factory=lambda: str(uuid4()))
    account_type: str  # Credit Card, Loan, Mortgage, Line of Credit
    account_name: Optional[str] = None  # e.g., "Chase Sapphire", "Car Loan"
    
    # Balance info
    current_balance: float = Field(ge=0.0)
    credit_limit: Optional[float] = Field(default=None, ge=0.0)
    minimum_payment: Optional[float] = Field(default=None, ge=0.0)
    
    # Interest
    apr: Optional[float] = Field(default=None, ge=0.0, le=100.0)  # Annual Percentage Rate
    
    # Payment history
    monthly_payment: Optional[float] = Field(default=None, ge=0.0)
    payment_due_date: Optional[int] = Field(default=None, ge=1, le=31)  # Day of month
    
    # Status
    is_active: bool = True
    
    @field_validator('credit_limit')
    @classmethod
    def credit_limit_must_exceed_balance(cls, v, info):
        """Validate that credit limit >= current balance."""
        if v is not None and 'current_balance' in info.data:
            current_balance = info.data['current_balance']
            if v < current_balance:
                raise ValueError('Credit limit must be >= current balance')
        return v
    
    @field_validator('apr')
    @classmethod
    def apr_in_valid_range(cls, v):
        """Validate APR is between 0 and 100."""
        if v is not None and not 0.0 <= v <= 100.0:
            raise ValueError('APR must be between 0 and 100')
        return v
    
    @property
    def utilization_rate(self) -> Optional[float]:
        """Calculate credit utilization rate (for credit cards)."""
        if self.credit_limit and self.credit_limit > 0:
            return (self.current_balance / self.credit_limit) * 100
        return None
    
    @property
    def available_credit(self) -> Optional[float]:
        """Calculate available credit (for credit cards)."""
        if self.credit_limit is not None:
            return self.credit_limit - self.current_balance
        return None
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "account_id": "acc_123456",
                "account_type": "Credit Card",
                "account_name": "Chase Sapphire",
                "current_balance": 3500.00,
                "credit_limit": 10000.00,
                "minimum_payment": 105.00,
                "apr": 18.99,
                "monthly_payment": 500.00,
                "payment_due_date": 15,
                "is_active": True
            }
        }
