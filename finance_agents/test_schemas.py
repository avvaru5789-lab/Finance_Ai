"""
Simple test to verify all schemas load correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from finance_agents.schemas import (
    Transaction,
    DebtAccount,
    FinancialState,
    create_initial_state,
    DebtAnalysisOutput,
    SavingsStrategyOutput,
    BudgetOutput,
    RiskScoreOutput,
)
from datetime import datetime


def test_transaction():
    """Test Transaction model."""
    print("Testing Transaction...")
    
    txn = Transaction(
        date=datetime(2024, 1, 15),
        description="Amazon Prime",
        amount=-14.99,
        category="Entertainment",
        expense_type="Fixed",
        confidence=0.95,
        is_recurring=True
    )
    
    print(f"✅ Transaction created: {txn.description} - ${txn.amount}")
    print(f"   ID: {txn.id}")
    return txn


def test_debt_account():
    """Test DebtAccount model."""
    print("\nTesting DebtAccount...")
    
    debt = DebtAccount(
        account_type="Credit Card",
        account_name="Chase Sapphire",
        current_balance=3500.00,
        credit_limit=10000.00,
        minimum_payment=105.00,
        apr=18.99,
        monthly_payment=500.00,
        payment_due_date=15
    )
    
    print(f"✅ DebtAccount created: {debt.account_name}")
    print(f"   Balance: ${debt.current_balance}")
    print(f"   Utilization: {debt.utilization_rate:.1f}%")
    print(f"   Available: ${debt.available_credit}")
    return debt


def test_financial_state():
    """Test FinancialState creation."""
    print("\nTesting FinancialState...")
    
    # Create sample data
    txn = Transaction(
        date=datetime(2024, 1, 15),
        description="Test",
        amount=-100.00,
        category="Food"
    )
    
    debt = DebtAccount(
        account_type="Credit Card",
        current_balance=5000.00,
        apr=18.0
    )
    
    metrics = {
        "total_income": 5000.00,
        "total_expenses": 3500.00,
        "net_income": 1500.00,
        "savings_rate": 30.0,
        "expense_volatility": 0.15,
        "debt_to_income_ratio": 100.0,
        "expense_by_category": {"Food": 800.00, "Transport": 200.00},
        "income_by_source": {"Salary": 5000.00},
        "recurring_subscriptions": []
    }
    
    state = create_initial_state(
        transactions=[txn],
        debt_accounts=[debt],
        metrics=metrics,
        analysis_id="test-123"
    )
    
    print(f"✅ FinancialState created")
    print(f"   Analysis ID: {state['analysis_id']}")
    print(f"   Total Income: ${state['total_income']}")
    print(f"   Savings Rate: {state['savings_rate']}%")
    print(f"   Status: {state['processing_status']}")
    return state


def test_agent_outputs():
    """Test all agent output schemas."""
    print("\nTesting Agent Output Schemas...")
    
    debt_analysis = DebtAnalysisOutput(
        total_debt=25000.00,
        high_interest_debt=15000.00,
        payoff_strategy="Avalanche",
        priority_accounts=["acc_001"],
        months_to_payoff=36,
        total_interest_paid=4500.00,
        recommended_monthly_payment=850.00,
        recommendations=["Focus on high-interest debt first"]
    )
    print(f"✅ DebtAnalysisOutput: ${debt_analysis.total_debt} total debt")
    
    savings = SavingsStrategyOutput(
        monthly_savings_capacity=1200.00,
        emergency_fund_gap=9000.00,
        current_savings_rate=24.0,
        emergency_fund_target=15000.00,
        monthly_savings_goal=1000.00,
        months_to_emergency_fund=12,
        recommendations=["Build emergency fund"]
    )
    print(f"✅ SavingsStrategyOutput: ${savings.monthly_savings_goal}/mo target")
    
    budget = BudgetOutput(
        monthly_savings_potential=450.00,
        annual_savings_potential=5400.00,
        recommendations=["Reduce dining out"]
    )
    print(f"✅ BudgetOutput: ${budget.monthly_savings_potential}/mo potential")
    
    risk = RiskScoreOutput(
        overall_score=65,
        risk_level="Medium",
        debt_risk_score=55,
        savings_risk_score=70,
        volatility_risk_score=60,
        liquidity_risk_score=75,
        top_priorities=["Build emergency fund"],
        summary="Medium risk profile"
    )
    print(f"✅ RiskScoreOutput: {risk.overall_score}/100 ({risk.risk_level})")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing LangGraph Schemas")
    print("=" * 60)
    
    try:
        test_transaction()
        test_debt_account()
        test_financial_state()
        test_agent_outputs()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
