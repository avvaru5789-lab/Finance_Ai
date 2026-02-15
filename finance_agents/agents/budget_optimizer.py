"""
Budget Optimizer Agent - Identifies spending issues and optimization opportunities.
"""

from typing import Dict, Any, Type, List
from pydantic import BaseModel
from finance_agents.schemas import BudgetOutput, Transaction
from .base_agent import BaseAgent


class BudgetOptimizerAgent(BaseAgent):
    """Analyzes spending patterns and optimizes budgets."""
    
    def get_system_prompt(self) -> str:
        return """You are a budget optimization expert who helps people spend wisely and save more.

Your expertise includes:
- Analyzing spending patterns across categories
- Identifying overspending and waste
- Finding subscription and recurring cost optimization
- Applying budgeting frameworks (50/30/20 rule)
- Creating realistic, sustainable budgets

Key principles:
- 50/30/20 rule: 50% needs, 30% wants, 20% savings/debt
- Look for "low-hanging fruit" - easy wins
- Identify forgotten subscriptions
- Compare to national averages
- Balance optimization with quality of life
- Provide specific dollar amounts and percentages

Be specific about what to cut and by how much. Focus on high-impact changes."""

    def get_output_schema(self) -> Type[BaseModel]:
        return BudgetOutput
    
    def extract_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract budget-related data from state."""
        return {
            "total_income": state.get("total_income", 0.0),
            "total_expenses": state.get("total_expenses", 0.0),
            "expense_by_category": state.get("expense_by_category", {}),
            "recurring_subscriptions": state.get("recurring_subscriptions", []),
            "transactions": state.get("transactions", [])
        }
    
    def create_prompt(self, data: Dict[str, Any]) -> str:
        """Create budget optimization prompt."""
        
        expenses = data["expense_by_category"]
        income = data["total_income"]
        
        # Calculate percentages
        expense_percentages = {}
        if income > 0:
            for category, amount in expenses.items():
                expense_percentages[category] = (amount / income) * 100
        
        # Format spending breakdown
        spending_lines = []
        for category in sorted(expenses.keys(), key=lambda x: expenses[x], reverse=True):
            amount = expenses[category]
            pct = expense_percentages.get(category, 0)
            spending_lines.append(f"- {category}: ${amount:,.2f} ({pct:.1f}% of income)")
        
        # Format subscriptions
        subs_info = "- None detected"
        if data["recurring_subscriptions"]:
            subs_lines = []
            for sub in data["recurring_subscriptions"][:10]:  # Top 10
                subs_lines.append(f"- {sub.get('description', 'Unknown')}: ${sub.get('amount', 0):.2f}/mo")
            subs_info = "\n".join(subs_lines)
        
        prompt = f"""Analyze this budget and provide optimization recommendations:

FINANCIAL OVERVIEW:
- Monthly Income: ${income:,.2f}
- Monthly Expenses: ${data['total_expenses']:,.2f}
- Spending Rate: {(data['total_expenses']/income*100) if income > 0 else 0:.1f}%

SPENDING BY CATEGORY:
{chr(10).join(spending_lines)}

RECURRING SUBSCRIPTIONS:
{subs_info}

BENCHMARKS (50/30/20 RULE):
- Needs (Housing, Food, Transport): Should be ~50% = ${income * 0.5:,.2f}
- Wants (Entertainment, Dining): Should be ~30% = ${income * 0.3:,.2f}
- Savings/Debt: Should be ~20% = ${income * 0.2:,.2f}

REQUIRED ANALYSIS:
1. Identify overspending categories (compare to benchmarks)
2. Find optimization opportunities with specific savings amounts
3. Recommend budget by category
4. Compare current vs recommended for top categories
5. Calculate monthly and annual savings potential
6. Provide 3-5 actionable recommendations
7. Identify "quick wins" - easy changes with high impact

IMPORTANT:
- Be specific about dollar amounts to cut
- Suggest realistic alternatives (e.g., reduce dining from $X to $Y)
- Highlight forgotten/unused subscriptions
- Calculate total potential savings"""
        
        return prompt
