"""
High-level executor for financial analysis workflow.
Provides simple API to run complete analysis.
"""

from typing import List, Dict, Any
from loguru import logger

from finance_agents.schemas import (
    Transaction,
    DebtAccount,
    FinancialState,
    create_initial_state
)
from .graph import create_financial_analysis_graph, create_parallel_financial_analysis_graph


def analyze_finances(
    transactions: List[Transaction],
    debt_accounts: List[DebtAccount],
    metrics: Dict[str, Any],
    analysis_id: str,
    openrouter_api_key: str,
    use_parallel: bool = False
) -> FinancialState:
    """
    Run complete financial analysis with all agents.
    
    This is the main entry point for the financial analysis workflow.
    It creates the initial state, builds the LangGraph, and executes
    all agents to produce a complete financial analysis.
    
    Args:
        transactions: List of financial transactions
        debt_accounts: List of debt accounts (credit cards, loans)
        metrics: Computed financial metrics (income, expenses, etc.)
        analysis_id: Unique identifier for this analysis
        openrouter_api_key: OpenRouter API key for LLM access
        use_parallel: Whether to use parallel execution (experimental)
        
    Returns:
        Complete FinancialState with all agent outputs
        
    Example:
        >>> result = analyze_finances(
        ...     transactions=[...],
        ...     debt_accounts=[...],
        ...     metrics={
        ...         "total_income": 5000.00,
        ...         "total_expenses": 3500.00,
        ...         ...
        ...     },
        ...     analysis_id="uuid-here",
        ...     openrouter_api_key="your-key"
        ... )
        >>> print(result["risk_score"].overall_score)
        65
    """
    logger.info("=" * 70)
    logger.info("Starting Financial Analysis Workflow")
    logger.info("=" * 70)
    logger.info(f"Analysis ID: {analysis_id}")
    logger.info(f"Transactions: {len(transactions)}")
    logger.info(f"Debt Accounts: {len(debt_accounts)}")
    logger.info(f"Parallel Mode: {use_parallel}")
    
    # Create initial state
    logger.info("Creating initial state...")
    state = create_initial_state(
        transactions=transactions,
        debt_accounts=debt_accounts,
        metrics=metrics,
        analysis_id=analysis_id
    )
    
    # Create and compile graph
    logger.info("Building LangGraph...")
    if use_parallel:
        from .graph import create_parallel_financial_analysis_graph
        graph = create_parallel_financial_analysis_graph(openrouter_api_key)
    else:
        graph = create_financial_analysis_graph(openrouter_api_key)
    
    # Run the workflow
    logger.info("Executing workflow...")
    logger.info("-" * 70)
    
    try:
        result = graph.invoke(state)
        
        logger.info("-" * 70)
        logger.info("=" * 70)
        logger.info("Financial Analysis Complete!")
        logger.info("=" * 70)
        
        # Log summary
        if result.get("debt_analysis"):
            logger.info(f"✅ Debt Analysis: Total debt ${result['debt_analysis'].total_debt:,.2f}")
        if result.get("savings_strategy"):
            logger.info(f"✅ Savings Strategy: ${result['savings_strategy'].monthly_savings_goal:,.2f}/mo goal")
        if result.get("budget_recommendations"):
            logger.info(f"✅ Budget: ${result['budget_recommendations'].monthly_savings_potential:,.2f}/mo potential")
        if result.get("risk_score"):
            logger.info(f"✅ Risk Score: {result['risk_score'].overall_score}/100 ({result['risk_score'].risk_level})")
        
        if result.get("errors"):
            logger.warning(f"⚠️  {len(result['errors'])} errors occurred")
            for error in result["errors"]:
                logger.warning(f"   - {error}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Workflow execution failed: {e}")
        raise


def analyze_finances_streaming(
    transactions: List[Transaction],
    debt_accounts: List[DebtAccount],
    metrics: Dict[str, Any],
    analysis_id: str,
    openrouter_api_key: str
):
    """
    Run financial analysis with streaming updates.
    
    Yields intermediate results as each agent completes.
    Useful for real-time UI updates.
    
    Args:
        transactions: List of transactions
        debt_accounts: List of debt accounts
        metrics: Computed metrics
        analysis_id: Analysis ID
        openrouter_api_key: API key
        
    Yields:
        Dict with node name and updated state
    """
    logger.info("Starting streaming financial analysis...")
    
    # Create initial state
    state = create_initial_state(
        transactions=transactions,
        debt_accounts=debt_accounts,
        metrics=metrics,
        analysis_id=analysis_id
    )
    
    # Create graph
    graph = create_financial_analysis_graph(openrouter_api_key)
    
    # Stream execution
    for chunk in graph.stream(state):
        node_name = list(chunk.keys())[0]
        logger.info(f"✅ Node '{node_name}' completed")
        yield {
            "node": node_name,
            "state": chunk[node_name]
        }
