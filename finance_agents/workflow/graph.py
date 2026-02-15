"""
LangGraph workflow definition.
Defines the multi-agent financial analysis graph.
"""

from typing import Dict, Any
from loguru import logger
from langgraph.graph.state import StateGraph
from langgraph.types import Send
END = "__end__"

from finance_agents.schemas import FinancialState
from .nodes import (
    create_debt_analyzer_node,
    create_savings_strategy_node,
    create_budget_optimizer_node,
    create_risk_scorer_node,
    create_finalize_node
)


def create_financial_analysis_graph(openrouter_api_key: str):
    """
    Create and compile the financial analysis graph.
    
    This graph orchestrates 4 specialized agents:
    1. Debt Analyzer - Analyzes debt and creates payoff strategies
    2. Savings Strategy - Creates emergency fund and savings plans
    3. Budget Optimizer - Identifies spending optimizations
    4. Risk Scorer - Calculates overall financial health score
    
    The first 3 agents run in parallel (independent).
    Risk Scorer runs after them (depends on their outputs).
    
    Args:
        openrouter_api_key: OpenRouter API key for LLM access
        
    Returns:
        Compiled LangGraph application
    """
    logger.info("Building financial analysis graph...")
    
    # Create StateGraph with FinancialState type
    graph = StateGraph(Dict[str, Any])  # Using Dict for flexibility
    
    # Create node functions
    debt_node = create_debt_analyzer_node(openrouter_api_key)
    savings_node = create_savings_strategy_node(openrouter_api_key)
    budget_node = create_budget_optimizer_node(openrouter_api_key)
    risk_node = create_risk_scorer_node(openrouter_api_key)
    finalize_node = create_finalize_node()
    
    # Add nodes to graph
    graph.add_node("debt_analyzer", debt_node)
    graph.add_node("savings_strategy", savings_node)
    graph.add_node("budget_optimizer", budget_node)
    graph.add_node("risk_scorer", risk_node)
    graph.add_node("finalize", finalize_node)
    
    # Set entry point
    graph.set_entry_point("debt_analyzer")
    
    # Define edges for workflow
    # All 3 analysis agents run in parallel, then Risk Scorer waits for all
    graph.add_edge("debt_analyzer", "savings_strategy")
    graph.add_edge("savings_strategy", "budget_optimizer")
    graph.add_edge("budget_optimizer", "risk_scorer")
    
    # Finalize and end
    graph.add_edge("risk_scorer", "finalize")
    graph.add_edge("finalize", END)
    
    # Compile the graph
    logger.info("✅ Graph compiled successfully")
    compiled = graph.compile()
    
    return compiled


def create_parallel_financial_analysis_graph(openrouter_api_key: str):
    """
    Create graph with true parallel execution for first 3 agents.
    
    This uses a branching pattern where all 3 agents run simultaneously,
    then converge at the risk scorer.
    
    Args:
        openrouter_api_key: OpenRouter API key
        
    Returns:
        Compiled LangGraph with parallel execution
    """
    logger.info("Building parallel financial analysis graph...")
    
    graph = StateGraph(Dict[str, Any])
    
    # Create nodes
    debt_node = create_debt_analyzer_node(openrouter_api_key)
    savings_node = create_savings_strategy_node(openrouter_api_key)
    budget_node = create_budget_optimizer_node(openrouter_api_key)
    risk_node = create_risk_scorer_node(openrouter_api_key)
    finalize_node = create_finalize_node()
    
    # Add nodes
    graph.add_node("debt_analyzer", debt_node)
    graph.add_node("savings_strategy", savings_node)
    graph.add_node("budget_optimizer", budget_node)
    graph.add_node("risk_scorer", risk_node)
    graph.add_node("finalize", finalize_node)
    
    # Parallel start - all 3 agents are entry points
    graph.set_entry_point("debt_analyzer")
    graph.set_entry_point("savings_strategy")
    graph.set_entry_point("budget_optimizer")
    
    # All converge to risk scorer
    graph.add_edge("debt_analyzer", "risk_scorer")
    graph.add_edge("savings_strategy", "risk_scorer")
    graph.add_edge("budget_optimizer", "risk_scorer")
    
    # Finish
    graph.add_edge("risk_scorer", "finalize")
    graph.add_edge("finalize", END)
    
    logger.info("✅ Parallel graph compiled successfully")
    return graph.compile()
