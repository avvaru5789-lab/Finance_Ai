"""
LangGraph schemas for financial analysis.

This package contains all data models for the multi-agent financial coach system.
"""

from .transaction import Transaction
from .debt import DebtAccount
from .state import FinancialState, FinancialStateInput, create_initial_state
from .agent_outputs import (
    DebtAnalysisOutput,
    SavingsStrategyOutput,
    BudgetOutput,
    RiskScoreOutput
)

__all__ = [
    # Core models
    "Transaction",
    "DebtAccount",
    
    # State
    "FinancialState",
    "FinancialStateInput",
    "create_initial_state",
    
    # Agent outputs
    "DebtAnalysisOutput",
    "SavingsStrategyOutput",
    "BudgetOutput",
    "RiskScoreOutput",
]
