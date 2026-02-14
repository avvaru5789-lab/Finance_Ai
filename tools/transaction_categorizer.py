"""
Transaction categorizer using rule-based logic.
Categorizes transactions into spending categories without using LLMs.
"""

import re
from typing import List, Dict, Optional
from loguru import logger


class TransactionCategorizer:
    """Rule-based transaction categorization (deterministic, no LLM)."""
    
    # Category definitions with keyword patterns
    CATEGORIES = {
        'Income': {
            'keywords': [
                'salary', 'payroll', 'wage', 'income', 'payment received',
                'direct deposit', 'transfer from', 'deposit', 'refund',
                'bonus', 'commission', 'reimbursement', 'dividend', 'interest earned'
            ],
            'type': 'credit',  # Income is always credit
        },
        'Housing': {
            'keywords': [
                'rent', 'mortgage', 'property tax', 'hoa', 'homeowners association',
                'property management', 'lease', 'apartment', 'condo fee'
            ],
        },
        'Utilities': {
            'keywords': [
                'electric', 'electricity', 'gas', 'water', 'sewer', 'trash',
                'internet', 'wifi', 'phone', 'mobile', 'cable', 'utility',
                'verizon', 'att', 'tmobile', 'comcast', 'xfinity'
            ],
        },
        'Food & Dining': {
            'keywords': [
                'restaurant', 'cafe', 'coffee', 'starbucks', 'dunkin',
                'mcdonald', 'burger', 'pizza', 'chipotle', 'subway',
                'food', 'grocery', 'supermarket', 'whole foods', 'trader joe',
                'safeway', 'kroger', 'walmart', 'target', 'costco',
                'uber eats', 'doordash', 'grubhub', 'postmates', 'dining'
            ],
        },
        'Transportation': {
            'keywords': [
                'gas', 'fuel', 'shell', 'chevron', 'exxon', 'bp', '76',
                'uber', 'lyft', 'taxi', 'parking', 'toll', 'metro',
                'transit', 'bus', 'train', 'subway', 'car payment',
                'auto insurance', 'dmv', 'vehicle', 'repair', 'mechanic'
            ],
        },
        'Entertainment': {
            'keywords': [
                'movie', 'theater', 'cinema', 'spotify', 'apple music',
                'entertainment', 'game', 'steam', 'playstation', 'xbox',
                'concert', 'event', 'ticket', 'amusement', 'recreation'
            ],
        },
        'Shopping': {
            'keywords': [
                'amazon', 'ebay', 'walmart', 'target', 'best buy',
                'home depot', 'lowes', 'ikea', 'clothing', 'apparel',
                'shoes', 'electronics', 'retail', 'store', 'shop',
                'mall', 'macys', 'nordstrom', 'gap', 'old navy'
            ],
        },
        'Healthcare': {
            'keywords': [
                'pharmacy', 'cvs', 'walgreens', 'rite aid', 'medical',
                'doctor', 'hospital', 'dental', 'dentist', 'health',
                'insurance', 'clinic', 'prescription', 'medicine'
            ],
        },
        'Subscriptions': {
            'keywords': [
                'netflix', 'hulu', 'disney', 'amazon prime', 'youtube premium',
                'subscription', 'membership', 'annual fee', 'monthly fee',
                'spotify', 'apple tv', 'hbo', 'paramount', 'peacock',
                'gym', 'fitness', 'planet fitness', '24 hour fitness'
            ],
        },
        'Insurance': {
            'keywords': [
                'insurance', 'geico', 'state farm', 'allstate', 'progressive',
                'policy', 'premium', 'health insurance', 'life insurance'
            ],
        },
        'Debt Payments': {
            'keywords': [
                'credit card payment', 'loan payment', 'student loan',
                'payment to', 'chase payment', 'bank of america payment',
                'capital one payment', 'discover payment', 'amex payment'
            ],
        },
        'Savings & Investments': {
            'keywords': [
                'transfer to savings', 'investment', 'brokerage', 'fidelity',
                'vanguard', 'charles schwab', 'etrade', 'robinhood',
                '401k', 'ira', 'retirement', 'savings account'
            ],
        },
        'Personal Care': {
            'keywords': [
                'salon', 'haircut', 'spa', 'beauty', 'cosmetics',
                'hygiene', 'personal care', 'barber'
            ],
        },
        'Education': {
            'keywords': [
                'tuition', 'school', 'university', 'college', 'course',
                'textbook', 'education', 'learning', 'udemy', 'coursera'
            ],
        },
        'Pets': {
            'keywords': [
                'pet', 'vet', 'veterinary', 'petsmart', 'petco',
                'dog', 'cat', 'animal'
            ],
        },
        'Travel': {
            'keywords': [
                'airline', 'flight', 'hotel', 'airbnb', 'booking',
                'travel', 'vacation', 'resort', 'marriott', 'hilton',
                'delta', 'united', 'american airlines', 'southwest'
            ],
        },
        'Fees & Charges': {
            'keywords': [
                'fee', 'charge', 'atm', 'overdraft', 'late fee',
                'service charge', 'maintenance fee', 'penalty'
            ],
        },
        'Cash & ATM': {
            'keywords': [
                'atm withdrawal', 'cash', 'withdrawal'
            ],
        },
        'Taxes': {
            'keywords': [
                'irs', 'tax', 'federal tax', 'state tax', 'tax payment'
            ],
        },
    }
    
    def categorize_transaction(self, transaction: Dict[str, any]) -> str:
        """
        Categorize a single transaction based on description.
        
        Args:
            transaction: Transaction dict with 'description', 'amount', 'type'
            
        Returns:
            Category name
        """
        description = str(transaction.get('description', '')).lower()
        transaction_type = transaction.get('type', 'debit')
        amount = transaction.get('amount', 0)
        
        # Check if it's income (positive/credit transactions)
        if transaction_type == 'credit' and amount > 0:
            # Check for income keywords
            if self._matches_keywords(description, self.CATEGORIES['Income']['keywords']):
                return 'Income'
        
        # For debit transactions, check all expense categories
        for category, config in self.CATEGORIES.items():
            if category == 'Income':
                continue  # Skip income for debit transactions
            
            keywords = config.get('keywords', [])
            if self._matches_keywords(description, keywords):
                return category
        
        # Default category
        return 'Other' if transaction_type == 'debit' else 'Income'
    
    def categorize_transactions(self, transactions: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Categorize a list of transactions.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Same list with 'category' field added
        """
        categorized = []
        category_counts = {}
        
        for txn in transactions:
            category = self.categorize_transaction(txn)
            txn['category'] = category
            categorized.append(txn)
            
            category_counts[category] = category_counts.get(category, 0) + 1
        
        logger.info(f"Categorized {len(categorized)} transactions")
        logger.info(f"Category distribution: {category_counts}")
        
        return categorized
    
    def _matches_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords."""
        text = text.lower()
        return any(keyword.lower() in text for keyword in keywords)
    
    def get_spending_by_category(self, transactions: List[Dict[str, any]]) -> Dict[str, float]:
        """
        Calculate total spending by category.
        
        Args:
            transactions: List of categorized transactions
            
        Returns:
            Dictionary of {category: total_amount}
        """
        category_totals = {}
        
        for txn in transactions:
            category = txn.get('category', 'Other')
            amount = abs(txn.get('amount', 0))
            
            # Only count debits/expenses (negative amounts)
            if txn.get('type') == 'debit' or txn.get('amount', 0) < 0:
                category_totals[category] = category_totals.get(category, 0) + amount
        
        return dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))
    
    def classify_expense_type(self, category: str) -> str:
        """
        Classify expense as Fixed, Variable, or Discretionary.
        
        Args:
            category: Transaction category
            
        Returns:
            Expense type
        """
        fixed_categories = {
            'Housing', 'Insurance', 'Debt Payments', 'Subscriptions',
            'Utilities'  # Partially fixed
        }
        
        discretionary_categories = {
            'Entertainment', 'Shopping', 'Dining', 'Travel',
            'Personal Care', 'Food & Dining'  # Partially discretionary
        }
        
        if category in fixed_categories:
            return 'Fixed'
        elif category in discretionary_categories:
            return 'Discretionary'
        else:
            return 'Variable'
    
    def get_fixed_vs_variable(self, transactions: List[Dict[str, any]]) -> Dict[str, float]:
        """
        Calculate fixed vs variable vs discretionary expenses.
        
        Returns:
            Dictionary with expense breakdown
        """
        breakdown = {
            'Fixed': 0.0,
            'Variable': 0.0,
            'Discretionary': 0.0,
        }
        
        for txn in transactions:
            # Only count expenses
            if txn.get('type') != 'debit' and txn.get('amount', 0) >= 0:
                continue
            
            category = txn.get('category', 'Other')
            expense_type = self.classify_expense_type(category)
            amount = abs(txn.get('amount', 0))
            
            breakdown[expense_type] += amount
        
        return breakdown


# Global instance
transaction_categorizer = TransactionCategorizer()
