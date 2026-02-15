"""
Integration tests for LangGraph workflow.
Tests the complete multi-agent financial analysis system.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langgraph.workflow import analyze_finances
from finance_agents.schemas import DebtAccount, Transaction, create_initial_state


# Get API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("❌ OPENROUTER_API_KEY not set in environment")
    print("Set it with: export OPENROUTER_API_KEY='your-key-here'")
    sys.exit(1)


def create_sample_data():
    """Create sample financial data for testing."""
    
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
    
    # Sample transactions
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
        ),
        Transaction(
            date=datetime(2024, 1, 22),
            description="Groceries",
            amount=-400.00,
            category="Food"
        )
    ]
    
    # Computed metrics
    metrics = {
        "total_income": 5000.00,
        "total_expenses": 3500.00,
        "net_income": 1500.00,
        "savings_rate": 30.0,
        "expense_volatility": 0.15,
        "debt_to_income_ratio": 150.0,
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
    
    return transactions, debts, metrics


def test_workflow_execution():
    """Test complete workflow execution."""
    print("\n" + "=" * 70)
    print("Testing Complete LangGraph Workflow")
    print("=" * 70)
    
    # Create sample data
    transactions, debts, metrics = create_sample_data()
    
    print(f"\n📊 Test Data:")
    print(f"   Transactions: {len(transactions)}")
    print(f"   Debt Accounts: {len(debts)}")
    print(f"   Total Income: ${metrics['total_income']:,.2f}")
    print(f"   Total Expenses: ${metrics['total_expenses']:,.2f}")
    
    # Run workflow
    print("\n🚀 Running workflow...")
    print("-" * 70)
    
    result = analyze_finances(
        transactions=transactions,
        debt_accounts=debts,
        metrics=metrics,
        analysis_id="test-workflow-001",
        openrouter_api_key=OPENROUTER_API_KEY
    )
    
    print("-" * 70)
    print("\n" + "=" * 70)
    print("Workflow Results")
    print("=" * 70)
    
    # Verify all agents ran
    print("\n✅ Agent Outputs:")
    
    if result.get("debt_analysis"):
        debt = result["debt_analysis"]
        print(f"\n  📊 Debt Analysis:")
        print(f"     Total Debt: ${debt.total_debt:,.2f}")
        print(f"     Strategy: {debt.payoff_strategy}")
        print(f"     Months to Payoff: {debt.months_to_payoff}")
        print(f"     Recommendations: {len(debt.recommendations)}")
    else:
        print("\n  ❌ Debt Analysis: FAILED")
    
    if result.get("savings_strategy"):
        savings = result["savings_strategy"]
        print(f"\n  💰 Savings Strategy:")
        print(f"     Monthly Capacity: ${savings.monthly_savings_capacity:,.2f}")
        print(f"     Emergency Fund Gap: ${savings.emergency_fund_gap:,.2f}")
        print(f"     Monthly Goal: ${savings.monthly_savings_goal:,.2f}")
        print(f"     Months to Fund: {savings.months_to_emergency_fund}")
    else:
        print("\n  ❌ Savings Strategy: FAILED")
    
    if result.get("budget_recommendations"):
        budget = result["budget_recommendations"]
        print(f"\n  📈 Budget Optimization:")
        print(f"     Monthly Savings Potential: ${budget.monthly_savings_potential:,.2f}")
        print(f"     Annual Potential: ${budget.annual_savings_potential:,.2f}")
        print(f"     Overspending Categories: {len(budget.overspending_categories)}")
        print(f"     Quick Wins: {len(budget.quick_wins)}")
    else:
        print("\n  ❌ Budget Optimization: FAILED")
    
    if result.get("risk_score"):
        risk = result["risk_score"]
        print(f"\n  ⚠️  Risk Assessment:")
        print(f"     Overall Score: {risk.overall_score}/100")
        print(f"     Risk Level: {risk.risk_level}")
        print(f"     Debt Risk: {risk.debt_risk_score}/100")
        print(f"     Savings Risk: {risk.savings_risk_score}/100")
        print(f"     Top Priorities: {len(risk.top_priorities)}")
    else:
        print("\n  ❌ Risk Assessment: FAILED")
    
    # Check for errors
    print("\n" + "=" * 70)
    if result.get("errors"):
        print(f"⚠️  Errors: {len(result['errors'])}")
        for error in result["errors"]:
            print(f"   - {error}")
    else:
        print("✅ No errors!")
    
    print(f"\n📊 Processing Status: {result.get('processing_status', 'unknown')}")
    
    # Verify completeness
    success = all([
        result.get("debt_analysis") is not None,
        result.get("savings_strategy") is not None,
        result.get("budget_recommendations") is not None,
        result.get("risk_score") is not None,
        result.get("processing_status") in ["complete", "complete_with_errors"]
    ])
    
    print("\n" + "=" * 70)
    if success:
        print("✅ WORKFLOW TEST PASSED!")
        print("=" * 70)
        print("\nAll 4 agents completed successfully!")
        print("LangGraph orchestration is working correctly.")
    else:
        print("❌ WORKFLOW TEST FAILED!")
        print("=" * 70)
        print("\nSome agents did not complete.")
        print("Check logs above for details.")
    
    return success


def test_workflow_streaming():
    """Test streaming workflow execution."""
    print("\n" + "=" * 70)
    print("Testing Streaming Workflow")
    print("=" * 70)
    
    from langgraph.workflow import analyze_finances_streaming
    
    transactions, debts, metrics = create_sample_data()
    
    print("\n🚀 Running streaming workflow...")
    
    completed_nodes = []
    for chunk in analyze_finances_streaming(
        transactions=transactions,
        debt_accounts=debts,
        metrics=metrics,
        analysis_id="test-streaming-001",
        openrouter_api_key=OPENROUTER_API_KEY
    ):
        node_name = chunk["node"]
        completed_nodes.append(node_name)
        print(f"   ✅ {node_name} completed")
    
    print(f"\n✅ Streaming test passed!")
    print(f"   Completed nodes: {completed_nodes}")
    
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("LangGraph Workflow Integration Tests")
    print("=" * 70)
    
    try:
        # Test main workflow
        workflow_success = test_workflow_execution()
        
        # Test streaming (optional)
        # streaming_success = test_workflow_streaming()
        
        if workflow_success:
            print("\n" + "=" * 70)
            print("✅ ALL TESTS PASSED!")
            print("=" * 70)
            sys.exit(0)
        else:
            print("\n" + "=" * 70)
            print("❌ TESTS FAILED!")
            print("=" * 70)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
