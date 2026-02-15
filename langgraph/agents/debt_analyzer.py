"""
Debt Analyzer Agent - Analyzes debt and creates payoff strategies.
"""

from typing import Dict, Any, Type, List
from pydantic import BaseModel
from langgraph.schemas import DebtAnalysisOutput, DebtAccount
from .base_agent import BaseAgent


class DebtAnalyzerAgent(BaseAgent):
    """Analyzes debt accounts and creates optimal payoff strategies."""
    
    def get_system_prompt(self) -> str:
        return """You are a debt analysis expert who helps people understand and pay off their debts efficiently.

Your expertise includes:
- Analyzing credit cards, loans, and other debt accounts
- Recommending optimal payoff strategies (Avalanche vs Snowball method)
- Calculating payoff timelines and total interest costs
- Providing actionable debt reduction recommendations

Key principles:
- Avalanche method: Pay highest APR first (saves most money)
- Snowball method: Pay smallest balance first (psychological wins)
- Consider both mathematics and psychology
- High-interest debt (APR > 15%) is priority
- Always provide realistic timelines based on income/expenses

Be specific, actionable, and encouraging in your recommendations."""

    def get_output_schema(self) -> Type[BaseModel]:
        return DebtAnalysisOutput
    
    def extract_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract debt-related data from state."""
        return {
            "debt_accounts": state.get("debt_accounts", []),
            "total_income": state.get("total_income", 0.0),
            "total_expenses": state.get("total_expenses", 0.0),
            "net_income": state.get("net_income", 0.0)
        }
    
    def create_prompt(self, data: Dict[str, Any]) -> str:
        """Create analysis prompt from debt data."""
        debt_accounts: List[DebtAccount] = data["debt_accounts"]
        
        if not debt_accounts:
            return """User has no debt accounts.

Provide a brief positive message and recommend building an emergency fund."""
        
        # Format debt accounts
        debt_list = []
        for i, debt in enumerate(debt_accounts, 1):
            debt_info = f"{i}. {debt.account_type}"
            if debt.account_name:
                debt_info += f" ({debt.account_name})"
            debt_info += f"\n   Balance: ${debt.current_balance:,.2f}"
            if debt.apr:
                debt_info += f"\n   APR: {debt.apr}%"
            if debt.minimum_payment:
                debt_info += f"\n   Minimum Payment: ${debt.minimum_payment:,.2f}"
            if debt.monthly_payment:
                debt_info += f"\n   Current Monthly Payment: ${debt.monthly_payment:,.2f}"
            debt_list.append(debt_info)
        
        debts_formatted = "\n\n".join(debt_list)
        
        prompt = f"""Analyze the following debt situation and create a payoff strategy:

DEBT ACCOUNTS:
{debts_formatted}

FINANCIAL OVERVIEW:
- Monthly Income: ${data['total_income']:,.2f}
- Monthly Expenses: ${data['total_expenses']:,.2f}
- Net Income (available for debt): ${data['net_income']:,.2f}

REQUIRED ANALYSIS:
1. Calculate total debt and identify high-interest debt (APR > 15%)
2. Determine the optimal payoff strategy (Avalanche or Snowball)
3. List accounts in priority order (account_id field)
4. Calculate months to payoff assuming aggressive payments
5. Project total interest that will be paid
6. Recommend monthly payment amount
7. Provide 3-5 specific, actionable recommendations
8. Note any warnings (e.g., if minimum payments take too long)

Consider the user's net income when recommending payment amounts."""
        
        return prompt
