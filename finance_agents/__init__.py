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

from .workflow import (
    analyze_finances,
    analyze_finances_streaming,
    create_financial_analysis_graph,
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
    # Workflow
    "analyze_finances",
    "analyze_finances_streaming",
    "create_financial_analysis_graph",
]
