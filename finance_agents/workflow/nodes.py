"""
Node functions for LangGraph workflows.
Each node wraps an agent and handles state updates.
"""

from typing import Dict, Any, Callable
from loguru import logger

from finance_agents.schemas import FinancialState
from finance_agents.agents import (
    DebtAnalyzerAgent,
    SavingsStrategyAgent,
    BudgetOptimizerAgent,
    RiskScorerAgent
)


def create_debt_analyzer_node(openrouter_api_key: str) -> Callable:
    """
    Create debt analyzer node function.
    
    Args:
        openrouter_api_key: OpenRouter API key
        
    Returns:
        Node function that runs debt analysis
    """
    agent = DebtAnalyzerAgent(openrouter_api_key)
    
    def debt_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Run debt analysis and update state."""
        try:
            logger.info("🔍 Running Debt Analyzer Agent...")
            result = agent.analyze(state)
            state["debt_analysis"] = result
            logger.info("✅ Debt analysis complete")
        except Exception as e:
            logger.error(f"❌ Debt analysis failed: {e}")
            state["errors"].append(f"Debt analysis: {str(e)}")
            state["debt_analysis"] = None
        
        return state
    
    return debt_analyzer_node


def create_savings_strategy_node(openrouter_api_key: str) -> Callable:
    """
    Create savings strategy node function.
    
    Args:
        openrouter_api_key: OpenRouter API key
        
    Returns:
        Node function that runs savings strategy
    """
    agent = SavingsStrategyAgent(openrouter_api_key)
    
    def savings_strategy_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Run savings strategy and update state."""
        try:
            logger.info("💰 Running Savings Strategy Agent...")
            result = agent.analyze(state)
            state["savings_strategy"] = result
            logger.info("✅ Savings strategy complete")
        except Exception as e:
            logger.error(f"❌ Savings strategy failed: {e}")
            state["errors"].append(f"Savings strategy: {str(e)}")
            state["savings_strategy"] = None
        
        return state
    
    return savings_strategy_node


def create_budget_optimizer_node(openrouter_api_key: str) -> Callable:
    """
    Create budget optimizer node function.
    
    Args:
        openrouter_api_key: OpenRouter API key
        
    Returns:
        Node function that runs budget optimization
    """
    agent = BudgetOptimizerAgent(openrouter_api_key)
    
    def budget_optimizer_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Run budget optimization and update state."""
        try:
            logger.info("📊 Running Budget Optimizer Agent...")
            result = agent.analyze(state)
            state["budget_recommendations"] = result
            logger.info("✅ Budget optimization complete")
        except Exception as e:
            logger.error(f"❌ Budget optimization failed: {e}")
            state["errors"].append(f"Budget optimization: {str(e)}")
            state["budget_recommendations"] = None
        
        return state
    
    return budget_optimizer_node


def create_risk_scorer_node(openrouter_api_key: str) -> Callable:
    """
    Create risk scorer node function.
    
    Args:
        openrouter_api_key: OpenRouter API key
        
    Returns:
        Node function that runs risk scoring
    """
    agent = RiskScorerAgent(openrouter_api_key)
    
    def risk_scorer_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Run risk scoring and update state."""
        try:
            logger.info("⚠️  Running Risk Scorer Agent...")
            result = agent.analyze(state)
            state["risk_score"] = result
            logger.info("✅ Risk scoring complete")
        except Exception as e:
            logger.error(f"❌ Risk scoring failed: {e}")
            state["errors"].append(f"Risk scoring: {str(e)}")
            state["risk_score"] = None
        
        return state
    
    return risk_scorer_node


def create_finalize_node() -> Callable:
    """
    Create finalization node.
    
    Returns:
        Node function that finalizes the state
    """
    def finalize_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize state and mark as complete."""
        logger.info("🎯 Finalizing analysis...")
        
        # Update processing status
        if state.get("errors"):
            state["processing_status"] = "complete_with_errors"
            logger.warning(f"⚠️  Analysis complete with {len(state['errors'])} errors")
        else:
            state["processing_status"] = "complete"
            logger.info("✅ Analysis complete successfully")
        
        return state
    
    return finalize_node
