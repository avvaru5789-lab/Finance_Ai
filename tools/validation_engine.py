"""
Validation engine for financial data and agent outputs.
Ensures data completeness, consistency, and correctness.
"""

from typing import List, Dict, Optional, Tuple
from loguru import logger


class ValidationEngine:
    """Validates financial data and ensures consistency."""
    
    # Required fields for a complete financial state
    REQUIRED_FIELDS = [
        'total_income',
        'total_expenses',
        'expenses_by_category',
        'transaction_count',
    ]
    
    # Validation rules
    MIN_TRANSACTIONS = 5  # Minimum transactions for meaningful analysis
    MAX_DTI_RATIO = 200  # Maximum debt-to-income ratio (200%)
    MIN_INCOME = 0.01  # Minimum monthly income
    
    def validate_transactions(self, transactions: List[Dict[str, any]]) -> Tuple[bool, List[str]]:
        """
        Validate transaction data.
        
        Args:
            transactions: List of transactions
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if we have enough transactions
        if not transactions:
            errors.append("No transactions found")
            return False, errors
        
        if len(transactions) < self.MIN_TRANSACTIONS:
            errors.append(f"Insufficient transactions: {len(transactions)} (minimum: {self.MIN_TRANSACTIONS})")
        
        # Validate each transaction
        for i, txn in enumerate(transactions):
            txn_errors = self._validate_single_transaction(txn, i)
            errors.extend(txn_errors)
        
        # Check for data consistency
        consistency_errors = self._check_transaction_consistency(transactions)
        errors.extend(consistency_errors)
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"Transaction validation passed: {len(transactions)} transactions")
        else:
            logger.warning(f"Transaction validation failed with {len(errors)} errors")
        
        return is_valid, errors
    
    def _validate_single_transaction(self, txn: Dict[str, any], index: int) -> List[str]:
        """Validate a single transaction."""
        errors = []
        
        # Required fields
        if 'date' not in txn or not txn['date']:
            errors.append(f"Transaction {index}: Missing date")
        
        if 'amount' not in txn:
            errors.append(f"Transaction {index}: Missing amount")
        elif not isinstance(txn['amount'], (int, float)):
            errors.append(f"Transaction {index}: Invalid amount type")
        
        if 'description' not in txn or not txn['description']:
            errors.append(f"Transaction {index}: Missing description")
        
        if 'category' not in txn:
            errors.append(f"Transaction {index}: Missing category")
        
        return errors
    
    def _check_transaction_consistency(self, transactions: List[Dict[str, any]]) -> List[str]:
        """Check for consistency issues in transactions."""
        errors = []
        
        # Check for duplicate transactions
        transaction_hashes = set()
        duplicates = 0
        
        for txn in transactions:
            # Create a simple hash
            txn_hash = f"{txn.get('date')}_{txn.get('amount')}_{txn.get('description', '')[:20]}"
            if txn_hash in transaction_hashes:
                duplicates += 1
            transaction_hashes.add(txn_hash)
        
        if duplicates > len(transactions) * 0.1:  # More than 10% duplicates
            errors.append(f"High number of potential duplicate transactions: {duplicates}")
        
        # Check for unrealistic amounts
        for txn in transactions:
            amount = abs(txn.get('amount', 0))
            if amount > 100000:  # Transactions over $100k
                logger.warning(f"Unusually large transaction: ${amount:.2f} - {txn.get('description')}")
        
        return errors
    
    def validate_financial_state(self, state: Dict[str, any]) -> Tuple[bool, List[str]]:
        """
        Validate complete financial state.
        
        Args:
            state: Financial metrics and data
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in state:
                errors.append(f"Missing required field: {field}")
        
        # Validate income
        income = state.get('total_income', 0)
        if income < self.MIN_INCOME:
            errors.append(f"Income too low or missing: ${income:.2f}")
        
        # Validate expenses
        expenses = state.get('total_expenses', 0)
        if expenses < 0:
            errors.append(f"Expenses cannot be negative: ${expenses:.2f}")
        
        # Check cash flow
        cash_flow = state.get('net_cash_flow', 0)
        if income > 0 and expenses > 0:
            calculated_cash_flow = income - expenses
            if abs(cash_flow - calculated_cash_flow) > 0.01:
                errors.append(f"Cash flow mismatch: stated={cash_flow:.2f}, calculated={calculated_cash_flow:.2f}")
        
        # Validate savings rate
        savings_rate = state.get('savings_rate', 0)
        if not (-100 <= savings_rate <= 100):
            errors.append(f"Savings rate out of range: {savings_rate:.1f}%")
        
        # Validate ratios
        dti_ratio = state.get('debt_to_income_ratio', 0)
        if dti_ratio > self.MAX_DTI_RATIO:
            errors.append(f"Debt-to-income ratio extremely high: {dti_ratio:.1f}%")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info("Financial state validation passed")
        else:
            logger.warning(f"Financial state validation failed with {len(errors)} errors")
        
        return is_valid, errors
    
    def validate_agent_output(
        self,
        agent_name: str,
        output: Dict[str, any],
        required_fields: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Validate output from an AI agent.
        
        Args:
            agent_name: Name of the agent
            output: Agent output dictionary
            required_fields: List of required field names
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for required fields
        for field in required_fields:
            if field not in output or output[field] is None:
                errors.append(f"{agent_name}: Missing required field '{field}'")
        
        # Check for empty strings
        for field, value in output.items():
            if isinstance(value, str) and not value.strip():
                errors.append(f"{agent_name}: Field '{field}' is empty")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"{agent_name} output validation passed")
        else:
            logger.warning(f"{agent_name} output validation failed: {errors}")
        
        return is_valid, errors
    
    def detect_conflicts(self, agent_outputs: Dict[str, Dict[str, any]]) -> List[str]:
        """
        Detect conflicts between agent outputs.
        
        Args:
            agent_outputs: Dictionary of {agent_name: output}
            
        Returns:
            List of conflict descriptions
        """
        conflicts = []
        
        # Example: Check if debt strategy and budget optimizer conflict
        debt_strategy = agent_outputs.get('debt_analyzer', {})
        budget_optimizer = agent_outputs.get('budget_optimizer', {})
        
        debt_allocation = debt_strategy.get('monthly_allocation', 0)
        available_budget = budget_optimizer.get('available_for_debt', 0)
        
        if debt_allocation > 0 and available_budget > 0:
            if debt_allocation > available_budget * 1.5:
                conflicts.append(
                    f"Conflict: debt_analyzer recommends ${debt_allocation:.2f}/month "
                    f"but budget_optimizer only shows ${available_budget:.2f} available"
                )
        
        # Check savings strategy vs budget
        savings_plan = agent_outputs.get('savings_strategy', {})
        monthly_savings = savings_plan.get('monthly_savings', 0)
        
        if monthly_savings > 0 and available_budget > 0:
            total_allocation = debt_allocation + monthly_savings
            if total_allocation > available_budget:
                conflicts.append(
                    f"Conflict: Combined debt + savings (${total_allocation:.2f}) "
                    f"exceeds available budget (${available_budget:.2f})"
                )
        
        if conflicts:
            logger.warning(f"Detected {len(conflicts)} conflicts between agent outputs")
        
        return conflicts
    
    def validate_mathematical_consistency(self, data: Dict[str, any]) -> Tuple[bool, List[str]]:
        """
        Validate mathematical consistency of calculations.
        
        Args:
            data: Financial data with calculations
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Income - Expenses = Cash Flow
        income = data.get('total_income', 0)
        expenses = data.get('total_expenses', 0)
        cash_flow = data.get('net_cash_flow', 0)
        
        expected_cash_flow = income - expenses
        if abs(cash_flow - expected_cash_flow) > 0.01:
            errors.append(
                f"Cash flow mismatch: {cash_flow:.2f} != {income:.2f} - {expenses:.2f}"
            )
        
        # Fixed + Variable + Discretionary = Total Expenses
        fixed = data.get('fixed_expenses', 0)
        variable = data.get('variable_expenses', 0)
        discretionary = data.get('discretionary_expenses', 0)
        
        total_categorized = fixed + variable + discretionary
        if abs(total_categorized - expenses) > 0.01:
            errors.append(
                f"Expense breakdown mismatch: {total_categorized:.2f} != {expenses:.2f}"
            )
        
        # Savings rate validation
        if income > 0:
            calculated_savings_rate = ((income - expenses) / income) * 100
            stated_savings_rate = data.get('savings_rate', 0)
            
            if abs(calculated_savings_rate - stated_savings_rate) > 0.1:
                errors.append(
                    f"Savings rate mismatch: {stated_savings_rate:.1f}% != {calculated_savings_rate:.1f}%"
                )
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            logger.error(f"Mathematical consistency check failed: {errors}")
        
        return is_valid, errors


# Global instance
validation_engine = ValidationEngine()
