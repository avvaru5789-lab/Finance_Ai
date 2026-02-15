"""
Test suite for financial analysis agents.
Tests each agent with sample data.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langgraph.agents import (
    DebtAnalyzerAgent,
    SavingsStrategyAgent,
    BudgetOptimizerAgent,
    RiskScorerAgent
)
from finance_agents.schemas import DebtAccount, Transaction, create_initial_state


# Get API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("❌ OPENROUTER_API_KEY not set in environment")
    print("Set it with: export OPENROUTER_API_KEY='your-key-here'")
    sys.exit(1)


def create_sample_state():
    """Create sample financial state for testing."""
    
    # Sample debt accounts
    debts = [
        DebtAccount(
            account_id="cc_001",
            account_type="Credit Card",
            account_name="Chase Sapphire",
            current_balance=5000.00,
            credit_limit=10000.00,
            apr=22.0,
            minimum_payment=150.00,
            monthly_payment=300.00
        ),
        DebtAccount(
            account_id="cc_002",
            account_type="Credit Card",
            account_name="Discover",
            current_balance=3000.00,
            credit_limit=5000.00,
            apr=18.5,
            minimum_payment=90.00
        ),
        DebtAccount(
            account_id="loan_001",
            account_type="Car Loan",
            account_name="Honda Civic",
            current_balance=12000.00,
            apr=5.5,
            monthly_payment=350.00
        )
    ]
    
    # Sample transactions (simplified for testing)
    transactions = [
        Transaction(
            date=datetime(2024, 1, 15),
            description="Salary",
            amount=5000.00,
            category="Income"
        ),
        Transaction(
            date=datetime(2024, 1, 20),
            description="Rent",
            amount=-1500.00,
            category="Housing"
        )
    ]
    
    # Computed metrics
    metrics = {
        "total_income": 5000.00,
        "total_expenses": 3500.00,
        "net_income": 1500.00,
        "savings_rate": 30.0,
        "expense_volatility": 0.15,
        "debt_to_income_ratio": 150.0,  # (5000 + 3000 + 12000) / 60000 annual * 100
        "expense_by_category": {
            "Housing": 1500.00,
            "Food": 600.00,
            "Transportation": 400.00,
            "Entertainment": 300.00,
            "Utilities": 200.00,
            "Subscriptions": 150.00,
            "Shopping": 200.00,
            "Healthcare": 150.00
        },
        "income_by_source": {
            "Salary": 5000.00
        },
        "recurring_subscriptions": [
            {"description": "Netflix", "amount": 15.99},
            {"description": "Spotify", "amount": 9.99},
            {"description": "Amazon Prime", "amount": 14.99},
            {"description": "Gym Membership", "amount": 50.00}
        ]
    }
    
    state = create_initial_state(
        transactions=transactions,
        debt_accounts=debts,
        metrics=metrics,
        analysis_id="test-run-001"
    )
    
    return state


def test_debt_analyzer():
    """Test Debt Analyzer Agent."""
    print("\n" + "=" * 60)
    print("Testing Debt Analyzer Agent")
    print("=" * 60)
    
    agent = DebtAnalyzerAgent(OPENROUTER_API_KEY)
    state = create_sample_state()
    
    print("Analyzing debt...")
    result = agent.analyze(state)
    
    print(f"\n✅ Debt Analysis Complete:")
    print(f"   Total Debt: ${result.total_debt:,.2f}")
    print(f"   High-Interest Debt: ${result.high_interest_debt:,.2f}")
    print(f"   Strategy: {result.payoff_strategy}")
    print(f"   Months to Payoff: {result.months_to_payoff}")
    print(f"   Recommended Payment: ${result.recommended_monthly_payment:,.2f}")
    print(f"   Recommendations: {len(result.recommendations)}")
    
    for i, rec in enumerate(result.recommendations, 1):
        print(f"      {i}. {rec}")
    
    return result


def test_savings_strategy():
    """Test Savings Strategy Agent."""
    print("\n" + "=" * 60)
    print("Testing Savings Strategy Agent")
    print("=" * 60)
    
    agent = SavingsStrategyAgent(OPENROUTER_API_KEY)
    state = create_sample_state()
    
    print("Creating savings strategy...")
    result = agent.analyze(state)
    
    print(f"\n✅ Savings Strategy Complete:")
    print(f"   Monthly Savings Capacity: ${result.monthly_savings_capacity:,.2f}")
    print(f"   Emergency Fund Gap: ${result.emergency_fund_gap:,.2f}")
    print(f"   Emergency Fund Target: ${result.emergency_fund_target:,.2f}")
    print(f"   Monthly Savings Goal: ${result.monthly_savings_goal:,.2f}")
    print(f"   Months to Emergency Fund: {result.months_to_emergency_fund}")
    print(f"   Recommendations: {len(result.recommendations)}")
    
    for i, rec in enumerate(result.recommendations, 1):
        print(f"      {i}. {rec}")
    
    return result


def test_budget_optimizer():
    """Test Budget Optimizer Agent."""
    print("\n" + "=" * 60)
    print("Testing Budget Optimizer Agent")
    print("=" * 60)
    
    agent = BudgetOptimizerAgent(OPENROUTER_API_KEY)
    state = create_sample_state()
    
    print("Optimizing budget...")
    result = agent.analyze(state)
    
    print(f"\n✅ Budget Optimization Complete:")
    print(f"   Monthly Savings Potential: ${result.monthly_savings_potential:,.2f}")
    print(f"   Annual Savings Potential: ${result.annual_savings_potential:,.2f}")
    print(f"   Overspending Categories: {', '.join(result.overspending_categories) if result.overspending_categories else 'None'}")
    print(f"   Optimization Opportunities: {len(result.optimization_opportunities)}")
    print(f"   Quick Wins: {len(result.quick_wins)}")
    
    if result.quick_wins:
        print("\n   Quick Wins:")
        for i, win in enumerate(result.quick_wins, 1):
            print(f"      {i}. {win}")
    
    return result


def test_risk_scorer():
    """Test Risk Scorer Agent."""
    print("\n" + "=" * 60)
    print("Testing Risk Scorer Agent")
    print("=" * 60)
    
    # First run other agents to get their outputs
    state = create_sample_state()
    
    print("Running prerequisite analyses...")
    debt_agent = DebtAnalyzerAgent(OPENROUTER_API_KEY)
    savings_agent = SavingsStrategyAgent(OPENROUTER_API_KEY)
    budget_agent = BudgetOptimizerAgent(OPENROUTER_API_KEY)
    
    state["debt_analysis"] = debt_agent.analyze(state)
    state["savings_strategy"] = savings_agent.analyze(state)
    state["budget_recommendations"] = budget_agent.analyze(state)
    
    print("Calculating risk score...")
    agent = RiskScorerAgent(OPENROUTER_API_KEY)
    result = agent.analyze(state)
    
    print(f"\n✅ Risk Score Complete:")
    print(f"   Overall Score: {result.overall_score}/100")
    print(f"   Risk Level: {result.risk_level}")
    print(f"   Debt Risk: {result.debt_risk_score}/100")
    print(f"   Savings Risk: {result.savings_risk_score}/100")
    print(f"   Volatility Risk: {result.volatility_risk_score}/100")
    print(f"   Liquidity Risk: {result.liquidity_risk_score}/100")
    print(f"\n   Top Priorities:")
    for i, priority in enumerate(result.top_priorities, 1):
        print(f"      {i}. {priority}")
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing All Financial Agents")
    print("=" * 60)
    
    try:
        # Test each agent
        debt_result = test_debt_analyzer()
        savings_result = test_savings_strategy()
        budget_result = test_budget_optimizer()
        risk_result = test_risk_scorer()
        
        print("\n" + "=" * 60)
        print("✅ ALL AGENT TESTS PASSED!")
        print("=" * 60)
        print("\nAll 4 agents are working correctly with structured output.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
