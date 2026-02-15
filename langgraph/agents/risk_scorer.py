"""
Risk Scoring Agent - Calculates overall financial health and risk score.
"""

from typing import Dict, Any, Type, Optional
from pydantic import BaseModel
from langgraph.schemas import RiskScoreOutput, DebtAnalysisOutput, SavingsStrategyOutput
from .base_agent import BaseAgent


class RiskScorerAgent(BaseAgent):
    """Calculates comprehensive financial risk score."""
    
    def get_system_prompt(self) -> str:
        return """You are a financial risk assessment expert who evaluates overall financial health.

Your expertise includes:
- Debt-to-income ratio analysis
- Emergency fund adequacy
- Cash flow stability
- Credit utilization risks
- Financial vulnerability assessment

Scoring framework (0-100, higher is better):
- 80-100: Low Risk - Strong financial position
- 60-79: Medium Risk - Generally healthy with some areas to improve  
- 40-59: High Risk - Significant vulnerabilities present
- 0-39: Critical Risk - Immediate action required

Component scores:
- Debt Risk: Based on DTI ratio, high-interest debt
- Savings Risk: Based on emergency fund adequacy
- Volatility Risk: Based on income/expense consistency
- Liquidity Risk: Based on cash flow and available credit

Key risk factors:
- DTI > 40% (critical if > 50%)
- No emergency fund or < 3 months expenses
- High credit card utilization (> 30%)
- Negative cash flow
- High-interest debt (APR > 15%)

Provide clear, prioritized action items."""

    def get_output_schema(self) -> Type[BaseModel]:
        return RiskScoreOutput
    
    def extract_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract risk-related data from state."""
        return {
            "total_income": state.get("total_income", 0.0),
            "total_expenses": state.get("total_expenses", 0.0),
            "savings_rate": state.get("savings_rate", 0.0),
            "debt_to_income_ratio": state.get("debt_to_income_ratio", 0.0),
            "expense_volatility": state.get("expense_volatility", 0.0),
            "debt_accounts": state.get("debt_accounts", []),
            # Agent outputs
            "debt_analysis": state.get("debt_analysis"),
            "savings_strategy": state.get("savings_strategy"),
            "budget_recommendations": state.get("budget_recommendations")
        }
    
    def create_prompt(self, data: Dict[str, Any]) -> str:
        """Create risk scoring prompt."""
        
        # Extract info from other agent outputs
        debt_info = self._format_debt_info(data.get("debt_analysis"))
        savings_info = self._format_savings_info(data.get("savings_strategy"))
        budget_info = self._format_budget_info(data.get("budget_recommendations"))
        
        # Calculate some metrics
        monthly_debt = sum(
            debt.monthly_payment or debt.minimum_payment or 0
            for debt in data.get("debt_accounts", [])
        )
        
        prompt = f"""Assess the overall financial risk for this user:

CORE METRICS:
- Monthly Income: ${data['total_income']:,.2f}
- Monthly Expenses: ${data['total_expenses']:,.2f}
- Savings Rate: {data['savings_rate']:.1f}%
- Debt-to-Income Ratio: {data['debt_to_income_ratio']:.1f}%
- Expense Volatility: {data['expense_volatility']:.2f}
- Monthly Debt Payments: ${monthly_debt:,.2f}

DEBT ANALYSIS:
{debt_info}

SAVINGS ANALYSIS:
{savings_info}

BUDGET ANALYSIS:
{budget_info}

REQUIRED ANALYSIS:
Calculate four component scores (0-100 each, higher is better):

1. DEBT RISK SCORE:
   - Consider DTI ratio (< 36% = good, > 50% = critical)
   - High-interest debt amount
   - Credit utilization if applicable
   
2. SAVINGS RISK SCORE:
   - Emergency fund adequacy (6 months = good)
   - Savings rate (> 20% = good)
   - Current savings growth trend

3. VOLATILITY RISK SCORE:
   - Expense consistency
   - Income stability
   - Predictability of cash flow

4. LIQUIDITY RISK SCORE:
   - Available cash/credit
   - Monthly cash flow
   - Ability to handle emergencies

5. OVERALL SCORE (weighted average):
   - Debt risk: 35%
   - Savings risk: 30%
   - Liquidity risk: 20%
   - Volatility risk: 15%

6. RISK LEVEL: Low, Medium, High, or Critical

7. RISK FACTORS: List specific vulnerabilities

8. PROTECTIVE FACTORS: List strengths

9. TOP PRIORITIES: 3-5 ordered by importance

10. IMMEDIATE ACTIONS: Urgent steps needed

Provide a clear summary explaining the overall risk level."""
        
        return prompt
    
    def _format_debt_info(self, debt_analysis: Optional[DebtAnalysisOutput]) -> str:
        """Format debt analysis output."""
        if not debt_analysis:
            return "- No debt analysis available"
        
        return f"""- Total Debt: ${debt_analysis.total_debt:,.2f}
- High-Interest Debt: ${debt_analysis.high_interest_debt:,.2f}
- Payoff Strategy: {debt_analysis.payoff_strategy}
- Months to Payoff: {debt_analysis.months_to_payoff}"""
    
    def _format_savings_info(self, savings_strategy: Optional[SavingsStrategyOutput]) -> str:
        """Format savings strategy output."""
        if not savings_strategy:
            return "- No savings analysis available"
        
        return f"""- Monthly Savings Capacity: ${savings_strategy.monthly_savings_capacity:,.2f}
- Emergency Fund Gap: ${savings_strategy.emergency_fund_gap:,.2f}
- Emergency Fund Target: ${savings_strategy.emergency_fund_target:,.2f}
- Months to Emergency Fund: {savings_strategy.months_to_emergency_fund}"""
    
    def _format_budget_info(self, budget: Optional[Any]) -> str:
        """Format budget output."""
        if not budget:
            return "- No budget analysis available"
        
        return f"""- Monthly Savings Potential: ${budget.monthly_savings_potential:,.2f}
- Overspending Categories: {', '.join(budget.overspending_categories) if budget.overspending_categories else 'None'}
- Optimization Opportunities: {len(budget.optimization_opportunities)} found"""
