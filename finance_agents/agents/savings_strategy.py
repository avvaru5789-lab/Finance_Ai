"""
Savings Strategy Agent - Creates emergency fund and savings strategies.
"""

from typing import Dict, Any, Type
from pydantic import BaseModel
from finance_agents.schemas import SavingsStrategyOutput
from .base_agent import BaseAgent


class SavingsStrategyAgent(BaseAgent):
    """Analyzes income/expenses and creates savings strategies."""
    
    def get_system_prompt(self) -> str:
        return """You are a savings strategy expert who helps people build emergency funds and achieve financial security.

Your expertise includes:
- Emergency fund planning (3-6 months of expenses)
- Calculating realistic savings capacity
- Creating achievable savings goals
- Allocating savings across different purposes
- Building sustainable savings habits

Key principles:
- Emergency fund is top priority (3-6 months expenses)
- Automate savings for consistency
- Start small and build momentum
- Balance emergency fund with other goals
- Be realistic about savings capacity
- Consider irregular expenses

Provide specific, actionable recommendations with timelines."""

    def get_output_schema(self) -> Type[BaseModel]:
        return SavingsStrategyOutput
    
    def extract_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract savings-related data from state."""
        return {
            "total_income": state.get("total_income", 0.0),
            "total_expenses": state.get("total_expenses", 0.0),
            "net_income": state.get("net_income", 0.0),
            "savings_rate": state.get("savings_rate", 0.0),
            "expense_by_category": state.get("expense_by_category", {}),
            "debt_accounts": state.get("debt_accounts", [])
        }
    
    def create_prompt(self, data: Dict[str, Any]) -> str:
        """Create savings strategy prompt."""
        
        # Calculate emergency fund target (6 months of expenses)
        emergency_fund_target = data["total_expenses"] * 6
        
        # Check if user has high-interest debt
        has_high_interest_debt = any(
            debt.apr and debt.apr > 15
            for debt in data.get("debt_accounts", [])
        )
        
        prompt = f"""Create a comprehensive savings strategy for this user:

FINANCIAL OVERVIEW:
- Monthly Income: ${data['total_income']:,.2f}
- Monthly Expenses: ${data['total_expenses']:,.2f}
- Net Income: ${data['net_income']:,.2f}
- Current Savings Rate: {data['savings_rate']:.1f}%

EMERGENCY FUND TARGET:
- Recommended: ${emergency_fund_target:,.2f} (6 months of expenses)

EXPENSE BREAKDOWN:
{self._format_expenses(data['expense_by_category'])}

DEBT SITUATION:
- High-interest debt present: {"Yes" if has_high_interest_debt else "No"}

REQUIRED ANALYSIS:
1. Calculate monthly savings capacity (realistic amount user can save)
2. Determine emergency fund gap (how much more is needed)
3. Calculate current savings rate percentage
4. Set emergency fund target (typically 6 months)
5. Recommend monthly savings goal
6. Allocate savings:
   - Emergency fund
   - Short-term goals
   - Long-term investments (if emergency fund is met)
7. Calculate months to reach emergency fund
8. Provide 3-5 specific recommendations
9. Note any challenges or trade-offs

IMPORTANT:
- If user has high-interest debt, balance debt payoff with emergency fund
- Minimum $1,000 emergency fund even while paying debt
- Be realistic about savings capacity
- Suggest automation strategies"""
        
        return prompt
    
    def _format_expenses(self, expenses: Dict[str, float]) -> str:
        """Format expense breakdown for prompt."""
        if not expenses:
            return "- No expense breakdown available"
        
        sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        lines = []
        for category, amount in sorted_expenses[:8]:  # Top 8 categories
            lines.append(f"- {category}: ${amount:,.2f}")
        
        return "\n".join(lines)
