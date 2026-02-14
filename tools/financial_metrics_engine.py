"""
Financial metrics calculation engine.
Computes all financial ratios and metrics deterministically (no LLM).
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics
from loguru import logger


class FinancialMetricsEngine:
    """Calculates financial health metrics and ratios."""
    
    def calculate_all_metrics(
        self,
        transactions: List[Dict[str, any]],
        monthly_income: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Calculate comprehensive financial metrics.
        
        Args:
            transactions: List of categorized transactions
            monthly_income: Optional manual income override
            
        Returns:
            Dictionary with all calculated metrics
        """
        logger.info("Calculating financial metrics...")
        
        # Basic calculations
        total_income = self._calculate_total_income(transactions)
        total_expenses = self._calculate_total_expenses(transactions)
        net_cash_flow = total_income - total_expenses
        
        # Use provided income or calculated
        income = monthly_income if monthly_income else total_income
        
        # Expense breakdown
        category_breakdown = self._get_category_breakdown(transactions)
        fixed_var = self._calculate_fixed_variable(transactions)
        
        # Calculate metrics
        savings_rate = self._calculate_savings_rate(income, total_expenses)
        discretionary_ratio = self._calculate_discretionary_ratio(fixed_var)
        spending_volatility = self._calculate_spending_volatility(transactions)
        
        # Debt metrics (if debt data available)
        debt_metrics = self._calculate_debt_metrics(transactions)
        
        metrics = {
            # Income & Expenses
            'total_income': round(income, 2),
            'total_expenses': round(total_expenses, 2),
            'net_cash_flow': round(net_cash_flow, 2),
            
            # Expense breakdown
            'expenses_by_category': category_breakdown,
            'fixed_expenses': round(fixed_var['Fixed'], 2),
            'variable_expenses': round(fixed_var['Variable'], 2),
            'discretionary_expenses': round(fixed_var['Discretionary'], 2),
            
            # Ratios & Percentages
            'savings_rate': round(savings_rate, 2),
            'expense_to_income_ratio': round((total_expenses / income * 100) if income > 0 else 0, 2),
            'discretionary_ratio': round(discretionary_ratio, 2),
            
            # Volatility
            'spending_volatility': round(spending_volatility, 2),
            
            # Debt
            **debt_metrics,
            
            # Additional metrics
            'average_transaction': round(self._calculate_average_transaction(transactions), 2),
            'transaction_count': len(transactions),
        }
        
        logger.info(f"Calculated metrics: Income=${income:.2f}, Expenses=${total_expenses:.2f}, Savings Rate={savings_rate:.1f}%")
        
        return metrics
    
    def _calculate_total_income(self, transactions: List[Dict[str, any]]) -> float:
        """Calculate total income from credit transactions."""
        total = 0.0
        for txn in transactions:
            if txn.get('category') == 'Income' or (txn.get('type') == 'credit' and txn.get('amount', 0) > 0):
                total += abs(txn.get('amount', 0))
        return total
    
    def _calculate_total_expenses(self, transactions: List[Dict[str, any]]) -> float:
        """Calculate total expenses from debit transactions."""
        total = 0.0
        for txn in transactions:
            # Exclude income, savings, and debt payments from expenses
            category = txn.get('category', '')
            if category in ['Income', 'Savings & Investments', 'Debt Payments']:
                continue
            
            if txn.get('type') == 'debit' or txn.get('amount', 0) < 0:
                total += abs(txn.get('amount', 0))
        return total
    
    def _get_category_breakdown(self, transactions: List[Dict[str, any]]) -> Dict[str, float]:
        """Get spending breakdown by category."""
        breakdown = {}
        for txn in transactions:
            category = txn.get('category', 'Other')
            
            # Only count expenses
            if category == 'Income':
                continue
            
            if txn.get('type') == 'debit' or txn.get('amount', 0) < 0:
                amount = abs(txn.get('amount', 0))
                breakdown[category] = breakdown.get(category, 0) + amount
        
        # Sort by amount
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))
    
    def _calculate_fixed_variable(self, transactions: List[Dict[str, any]]) -> Dict[str, float]:
        """Calculate fixed vs variable vs discretionary expenses."""
        from tools.transaction_categorizer import transaction_categorizer
        
        breakdown = {
            'Fixed': 0.0,
            'Variable': 0.0,
            'Discretionary': 0.0,
        }
        
        for txn in transactions:
            if txn.get('category') == 'Income':
                continue
            
            if txn.get('type') == 'debit' or txn.get('amount', 0) < 0:
                category = txn.get('category', 'Other')
                expense_type = transaction_categorizer.classify_expense_type(category)
                amount = abs(txn.get('amount', 0))
                breakdown[expense_type] += amount
        
        return breakdown
    
    def _calculate_savings_rate(self, income: float, expenses: float) -> float:
        """
        Calculate savings rate as percentage.
        
        Savings Rate = (Income - Expenses) / Income * 100
        """
        if income <= 0:
            return 0.0
        
        savings = income - expenses
        return (savings / income) * 100
    
    def _calculate_discretionary_ratio(self, fixed_var: Dict[str, float]) -> float:
        """
        Calculate discretionary spending as percentage of total expenses.
        """
        total_expenses = sum(fixed_var.values())
        if total_expenses <= 0:
            return 0.0
        
        return (fixed_var['Discretionary'] / total_expenses) * 100
    
    def _calculate_spending_volatility(self, transactions: List[Dict[str, any]]) -> float:
        """
        Calculate spending volatility (standard deviation of daily expenses).
        
        Higher volatility = less predictable spending
        """
        # Group expenses by day
        daily_expenses = {}
        
        for txn in transactions:
            if txn.get('type') != 'debit' and txn.get('amount', 0) >= 0:
                continue
            
            date = txn.get('date')
            amount = abs(txn.get('amount', 0))
            daily_expenses[date] = daily_expenses.get(date, 0) + amount
        
        if len(daily_expenses) < 2:
            return 0.0
        
        # Calculate standard deviation
        try:
            return statistics.stdev(daily_expenses.values())
        except:
            return 0.0
    
    def _calculate_average_transaction(self, transactions: List[Dict[str, any]]) -> float:
        """Calculate average transaction amount (expenses only)."""
        expense_amounts = [
            abs(txn.get('amount', 0))
            for txn in transactions
            if txn.get('type') == 'debit' or txn.get('amount', 0) < 0
        ]
        
        if not expense_amounts:
            return 0.0
        
        return sum(expense_amounts) / len(expense_amounts)
    
    def _calculate_debt_metrics(self, transactions: List[Dict[str, any]]) -> Dict[str, float]:
        """
        Calculate debt-related metrics from transactions.
        
        Note: This is basic. Full debt analysis will come from debt_analyzer_agent.
        """
        debt_payments = [
            abs(txn.get('amount', 0))
            for txn in transactions
            if txn.get('category') == 'Debt Payments'
        ]
        
        total_debt_payments = sum(debt_payments)
        
        return {
            'total_debt_payments': round(total_debt_payments, 2),
            'average_debt_payment': round(total_debt_payments / len(debt_payments), 2) if debt_payments else 0.0,
        }
    
    def calculate_liquidity_ratio(self, current_balance: float, monthly_expenses: float) -> float:
        """
        Calculate liquidity ratio (months of expenses covered).
        
        Liquidity Ratio = Current Balance / Monthly Expenses
        """
        if monthly_expenses <= 0:
            return 0.0
        
        return current_balance / monthly_expenses
    
    def calculate_debt_to_income_ratio(self, monthly_debt_payments: float, monthly_income: float) -> float:
        """
        Calculate debt-to-income ratio as percentage.
        
        DTI = (Monthly Debt Payments / Monthly Income) * 100
        """
        if monthly_income <= 0:
            return 0.0
        
        return (monthly_debt_payments / monthly_income) * 100
    
    def identify_recurring_subscriptions(self, transactions: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Identify recurring subscriptions based on transaction patterns.
        
        Returns:
            List of detected subscriptions with amounts
        """
        # Group by description
        description_amounts = {}
        
        for txn in transactions:
            desc = txn.get('description', '').strip().lower()
            amount = abs(txn.get('amount', 0))
            
            # Skip if not subscription category or too generic
            if txn.get('category') != 'Subscriptions' or len(desc) < 3:
                continue
            
            if desc not in description_amounts:
                description_amounts[desc] = []
            description_amounts[desc].append(amount)
        
        # Find recurring patterns (same amount, multiple times)
        subscriptions = []
        for desc, amounts in description_amounts.items():
            if len(amounts) >= 2:  # Appears at least twice
                # Check if amounts are similar (recurring subscription)
                avg_amount = sum(amounts) / len(amounts)
                if all(abs(amt - avg_amount) < 1.0 for amt in amounts):  # Within $1
                    subscriptions.append({
                        'description': desc,
                        'amount': round(avg_amount, 2),
                        'frequency': len(amounts),
                    })
        
        return sorted(subscriptions, key=lambda x: x['amount'], reverse=True)


# Global instance
financial_metrics_engine = FinancialMetricsEngine()
