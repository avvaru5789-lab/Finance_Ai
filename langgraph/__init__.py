"""LangGraph package for multi-agent financial orchestration."""

from .schemas import (
    Transaction,
    DebtAccount,
    FinancialState,
    FinancialStateInput,
    create_initial_state,
    DebtAnalysisOutput,
    SavingsStrategyOutput,
    BudgetOutput,
    RiskScoreOutput,
)

from .agents import (
    BaseAgent,
    DebtAnalyzerAgent,
    SavingsStrategyAgent,
    BudgetOptimizerAgent,
    RiskScorerAgent,
)

__all__ = [
    # Schemas
    "Transaction",
    "DebtAccount",
    "FinancialState",
    "FinancialStateInput",
    "create_initial_state",
    "DebtAnalysisOutput",
    "SavingsStrategyOutput",
    "BudgetOutput",
    "RiskScoreOutput",
    # Agents
    "BaseAgent",
    "DebtAnalyzerAgent",
    "SavingsStrategyAgent",
    "BudgetOptimizerAgent",
    "RiskScorerAgent",
]
