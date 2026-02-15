"""
Main state schema for LangGraph financial analysis workflow.
This is the state that flows through all agents in the graph.
"""

from typing import List, Dict, Optional, Any
from typing_extensions import TypedDict
from datetime import datetime

from .transaction import Transaction
from .debt import DebtAccount
from .agent_outputs import (
    DebtAnalysisOutput,
    SavingsStrategyOutput,
    BudgetOutput,
    RiskScoreOutput
)


class FinancialState(TypedDict, total=False):
    """
    Main state object that flows through the LangGraph workflow.
    
    Uses TypedDict (required by LangGraph) with total=False to allow
    gradual building of state as it flows through agents.
    """
    
    # =========================================================================
    # Input Data
    # =========================================================================
    
    transactions: List[Transaction]
    """List of all financial transactions."""
    
    debt_accounts: List[DebtAccount]
    """List of debt accounts (credit cards, loans, etc.)."""
    
    user_id: Optional[str]
    """Optional user identifier."""
    
    analysis_id: str
    """Unique identifier for this analysis."""
    
    # =========================================================================
    # Computed Metrics (from financial_metrics_engine)
    # =========================================================================
    
    total_income: float
    """Total income for the period."""
    
    total_expenses: float
    """Total expenses for the period."""
    
    net_income: float
    """Income minus expenses."""
    
    savings_rate: float
    """Savings rate as percentage (0-100)."""
    
    expense_volatility: float
    """Month-to-month expense volatility score."""
    
    debt_to_income_ratio: float
    """DTI ratio as percentage."""
    
    # =========================================================================
    # Category Breakdown
    # =========================================================================
    
    expense_by_category: Dict[str, float]
    """Expenses grouped by category."""
    
    income_by_source: Dict[str, float]
    """Income grouped by source."""
    
    recurring_subscriptions: List[Dict[str, Any]]
    """Detected recurring subscriptions."""
    
    # =========================================================================
    # Agent Outputs (added as agents complete)
    # =========================================================================
    
    debt_analysis: Optional[DebtAnalysisOutput]
    """Output from Debt Analyzer Agent."""
    
    savings_strategy: Optional[SavingsStrategyOutput]
    """Output from Savings Strategy Agent."""
    
    budget_recommendations: Optional[BudgetOutput]
    """Output from Budget Optimizer Agent."""
    
    risk_score: Optional[RiskScoreOutput]
    """Output from Risk Scoring Agent."""
    
    # =========================================================================
    # Metadata
    # =========================================================================
    
    timestamp: datetime
    """When this analysis was created."""
    
    processing_status: str
    """Current status: processing, complete, error."""
    
    errors: List[str]
    """List of any errors encountered."""
    
    warnings: List[str]
    """List of warnings (non-critical issues)."""
    
    # =========================================================================
    # Raw Data (optional, for debugging)
    # =========================================================================
    
    raw_ocr_text: Optional[str]
    """Original OCR text (for debugging)."""
    
    ocr_method: Optional[str]
    """OCR method used: pdfplumber or docker_paddleocr."""


# Helper type for initial state creation
class FinancialStateInput(TypedDict):
    """Input required to create initial state."""
    
    transactions: List[Transaction]
    debt_accounts: List[DebtAccount]
    analysis_id: str
    total_income: float
    total_expenses: float
    expense_by_category: Dict[str, float]


def create_initial_state(
    transactions: List[Transaction],
    debt_accounts: List[DebtAccount],
    metrics: Dict[str, Any],
    analysis_id: str
) -> FinancialState:
    """
    Create initial FinancialState from transactions and computed metrics.
    
    Args:
        transactions: List of transactions
        debt_accounts: List of debt accounts
        metrics: Dictionary of computed metrics from financial_metrics_engine
        analysis_id: Unique analysis identifier
        
    Returns:
        FinancialState ready for graph execution
    """
    return FinancialState(
        # Input data
        transactions=transactions,
        debt_accounts=debt_accounts,
        analysis_id=analysis_id,
        
        # Computed metrics
        total_income=metrics.get("total_income", 0.0),
        total_expenses=metrics.get("total_expenses", 0.0),
        net_income=metrics.get("net_income", 0.0),
        savings_rate=metrics.get("savings_rate", 0.0),
        expense_volatility=metrics.get("expense_volatility", 0.0),
        debt_to_income_ratio=metrics.get("debt_to_income_ratio", 0.0),
        expense_by_category=metrics.get("expense_by_category", {}),
        income_by_source=metrics.get("income_by_source", {}),
        recurring_subscriptions=metrics.get("recurring_subscriptions", []),
        
        # Metadata
        timestamp=datetime.now(),
        processing_status="processing",
        errors=[],
        warnings=[],
        
        # Agent outputs (None initially)
        debt_analysis=None,
        savings_strategy=None,
        budget_recommendations=None,
        risk_score=None,
    )
