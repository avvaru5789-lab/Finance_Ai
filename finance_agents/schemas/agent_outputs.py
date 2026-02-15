"""
Agent output schemas for debt, savings, budget, and risk analysis.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class DebtAnalysisOutput(BaseModel):
    """Output from Debt Analyzer Agent."""
    
    # Summary
    total_debt: float = Field(ge=0.0)
    high_interest_debt: float = Field(ge=0.0)  # APR > 15%
    avg_apr: Optional[float] = Field(default=None, ge=0.0)
    
    # Strategy
    payoff_strategy: str  # Avalanche, Snowball, Custom
    priority_accounts: List[str]  # Account IDs in priority order
    
    # Projections
    months_to_payoff: int = Field(ge=0)
    total_interest_paid: float = Field(ge=0.0)
    recommended_monthly_payment: float = Field(ge=0.0)
    
    # Recommendations
    recommendations: List[str]
    warnings: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_debt": 25000.00,
                "high_interest_debt": 15000.00,
                "avg_apr": 16.5,
                "payoff_strategy": "Avalanche",
                "priority_accounts": ["acc_001", "acc_002"],
                "months_to_payoff": 36,
                "total_interest_paid": 4500.00,
                "recommended_monthly_payment": 850.00,
                "recommendations": [
                    "Focus on high-interest credit card first",
                    "Consider balance transfer to 0% APR card"
                ],
                "warnings": ["Minimum payments will take 15 years"]
            }
        }


class SavingsStrategyOutput(BaseModel):
    """Output from Savings Strategy Agent."""
    model_config = ConfigDict(extra="forbid")
    
    # Current State
    monthly_savings_capacity: float
    emergency_fund_gap: float  # How much more needed for 3-6 months
    current_savings_rate: float = Field(ge=-100.0, le=100.0)  # Percentage
    
    # Strategy
    emergency_fund_target: float = Field(ge=0.0)
    monthly_savings_goal: float = Field(ge=0.0)
    
    # Timeline
    months_to_emergency_fund: int = Field(ge=0)
    
    # Recommendations
    recommendations: List[str]
    challenges: List[str] = Field(default_factory=list)


class OptimizationOpportunity(BaseModel):
    """A single budget optimization opportunity."""
    model_config = ConfigDict(extra="forbid")
    category: str
    current: float
    recommended: float
    savings: float


class BudgetOutput(BaseModel):
    """Output from Budget Optimizer Agent."""
    model_config = ConfigDict(extra="forbid")
    
    # Spending Analysis
    overspending_categories: List[str] = Field(default_factory=list)
    optimization_opportunities: List[OptimizationOpportunity] = Field(default_factory=list)
    
    # Savings Potential
    monthly_savings_potential: float = Field(ge=0.0)
    annual_savings_potential: float = Field(ge=0.0)
    
    # Recommendations
    recommendations: List[str]
    quick_wins: List[str] = Field(default_factory=list)  # Easy changes


class RiskScoreOutput(BaseModel):
    """Output from Risk Scoring Agent."""
    
    # Overall Score
    overall_score: int = Field(ge=0, le=100)
    risk_level: str  # Low, Medium, High, Critical
    
    # Component Scores
    debt_risk_score: int = Field(ge=0, le=100)
    savings_risk_score: int = Field(ge=0, le=100)
    volatility_risk_score: int = Field(ge=0, le=100)
    liquidity_risk_score: int = Field(ge=0, le=100)
    
    # Factors
    risk_factors: List[str] = Field(default_factory=list)
    protective_factors: List[str] = Field(default_factory=list)
    
    # Priorities
    top_priorities: List[str]  # Ordered by importance
    immediate_actions: List[str] = Field(default_factory=list)
    
    # Summary
    summary: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "overall_score": 65,
                "risk_level": "Medium",
                "debt_risk_score": 55,
                "savings_risk_score": 70,
                "volatility_risk_score": 60,
                "liquidity_risk_score": 75,
                "risk_factors": [
                    "High credit card debt ($15K)",
                    "Low emergency fund ($2K vs $15K needed)"
                ],
                "protective_factors": [
                    "Steady income",
                    "Positive savings rate (24%)"
                ],
                "top_priorities": [
                    "Build emergency fund to $15K",
                    "Pay down high-interest debt"
                ],
                "immediate_actions": [
                    "Set up automatic savings transfer"
                ],
                "summary": "Medium risk profile. Strong income but needs emergency fund."
            }
        }
