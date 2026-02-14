"""
Table extraction and parsing from OCR output.
Converts raw text/OCR into structured transaction tables.
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from loguru import logger
import pandas as pd


class TableExtractor:
    """Extracts and structures transaction tables from OCR text or CSV data."""
    
    # Common column headers for bank statements
    TRANSACTION_HEADERS = {
        'date': ['date', 'transaction date', 'posting date', 'trans date', 'dt'],
        'description': ['description', 'desc', 'memo', 'merchant', 'details', 'transaction details'],
        'debit': ['debit', 'withdrawal', 'withdrawals', 'payment', 'spent', 'charge'],
        'credit': ['credit', 'deposit', 'deposits', 'income', 'received'],
        'amount': ['amount', 'amt', 'transaction amount'],
        'balance': ['balance', 'running balance', 'closing balance'],
    }
    
    def extract_transactions(self, ocr_result: Dict[str, any]) -> List[Dict[str, any]]:
        """
        Extract transaction records from OCR result.
        
        Args:
            ocr_result: Output from OCR engine
            
        Returns:
            List of transaction dictionaries
        """
        method = ocr_result.get("method")
        
        if method == "csv":
            return self._extract_from_csv(ocr_result)
        elif method in ["pdfplumber", "deepseek_ocr"]:
            # First try to extract from structured tables
            if ocr_result.get("tables"):
                return self._extract_from_tables(ocr_result["tables"])
            # Fallback to text parsing
            return self._extract_from_text(ocr_result["text"])
        else:
            logger.error(f"Unknown extraction method: {method}")
            return []
    
    def _extract_from_csv(self, csv_data: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract transactions from CSV data."""
        df = pd.DataFrame(csv_data["data"])
        
        # Normalize column names
        column_mapping = self._map_columns(df.columns.tolist())
        df = df.rename(columns=column_mapping)
        
        transactions = []
        for _, row in df.iterrows():
            transaction = self._parse_transaction_row(row.to_dict())
            if transaction:
                transactions.append(transaction)
        
        logger.info(f"Extracted {len(transactions)} transactions from CSV")
        return transactions
    
    def _extract_from_tables(self, tables: List[List[List[str]]]) -> List[Dict[str, any]]:
        """Extract transactions from structured table data."""
        all_transactions = []
        
        for table in tables:
            if not table or len(table) < 2:
                continue
            
            # First row is usually headers
            headers = [str(h).lower().strip() for h in table[0]]
            column_mapping = self._map_columns(headers)
            
            # Parse each row
            for row in table[1:]:
                if len(row) != len(headers):
                    continue
                
                row_dict = {column_mapping.get(h, h): str(v).strip() 
                           for h, v in zip(headers, row)}
                
                transaction = self._parse_transaction_row(row_dict)
                if transaction:
                    all_transactions.append(transaction)
        
        logger.info(f"Extracted {len(all_transactions)} transactions from tables")
        return all_transactions
    
    def _extract_from_text(self, text: str) -> List[Dict[str, any]]:
        """
        Extract transactions from raw text using pattern matching.
        This is a fallback when structured tables aren't available.
        """
        transactions = []
        lines = text.split('\n')
        
        # Look for lines that match transaction patterns
        # Pattern: DATE  DESCRIPTION  AMOUNT
        transaction_pattern = re.compile(
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(.+?)\s+([-+]?\$?\d+[,\d]*\.?\d*)'
        )
        
        for line in lines:
            match = transaction_pattern.search(line)
            if match:
                date_str, description, amount_str = match.groups()
                
                transaction = {
                    'date': self.normalize_date(date_str),
                    'description': description.strip(),
                    'amount': self._parse_amount(amount_str),
                    'type': 'debit' if '-' in amount_str or 'debit' in line.lower() else 'credit',
                }
                
                transactions.append(transaction)
        
        logger.info(f"Extracted {len(transactions)} transactions from text")
        return transactions
    
    def _map_columns(self, columns: List[str]) -> Dict[str, str]:
        """Map detected columns to standard field names."""
        column_mapping = {}
        
        for col in columns:
            col_lower = col.lower().strip()
            
            # Check each standard field
            for standard_field, variations in self.TRANSACTION_HEADERS.items():
                if any(var in col_lower for var in variations):
                    column_mapping[col] = standard_field
                    break
        
        return column_mapping
    
    def _parse_transaction_row(self, row: Dict[str, any]) -> Optional[Dict[str, any]]:
        """Parse a single transaction row into standard format."""
        try:
            # Extract date
            date = row.get('date')
            if not date:
                return None
            
            normalized_date = self.normalize_date(str(date))
            if not normalized_date:
                return None
            
            # Extract description
            description = row.get('description', 'Unknown')
            
            # Extract amount (handle debit/credit columns)
            debit = row.get('debit', '')
            credit = row.get('credit', '')
            amount_field = row.get('amount', '')
            
            if debit and str(debit).strip() and str(debit).strip() != '-':
                amount = -abs(self._parse_amount(debit))  # Debit is negative
                transaction_type = 'debit'
            elif credit and str(credit).strip() and str(credit).strip() != '-':
                amount = abs(self._parse_amount(credit))  # Credit is positive
                transaction_type = 'credit'
            elif amount_field:
                amount = self._parse_amount(amount_field)
                transaction_type = 'debit' if amount < 0 else 'credit'
            else:
                return None
            
            return {
                'date': normalized_date,
                'description': str(description).strip(),
                'amount': amount,
                'type': transaction_type,
                'balance': self._parse_amount(row.get('balance', 0)),
            }
            
        except Exception as e:
            logger.debug(f"Failed to parse transaction row: {e}")
            return None
    
    def normalize_date(self, date_str: str) -> Optional[str]:
        """
        Normalize various date formats to YYYY-MM-DD.
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            Standardized date string or None if parsing fails
        """
        if not date_str or str(date_str).strip() in ['', '-', 'nan', 'None']:
            return None
        
        date_str = str(date_str).strip()
        
        # Common date formats
        formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%m/%d/%y',
            '%d/%m/%Y',
            '%d/%m/%y',
            '%m-%d-%Y',
            '%m-%d-%y',
            '%b %d, %Y',
            '%B %d, %Y',
            '%d-%b-%Y',
            '%Y%m%d',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        logger.debug(f"Could not parse date: {date_str}")
        return None
    
    def _parse_amount(self, amount_str: any) -> float:
        """
        Parse amount string to float.
        
        Handles: $1,234.56, -1234.56, (1234.56), etc.
        """
        if not amount_str:
            return 0.0
        
        amount_str = str(amount_str).strip()
        
        if amount_str in ['-', '', 'nan', 'None']:
            return 0.0
        
        # Remove currency symbols and whitespace
        amount_str = re.sub(r'[$,\s]', '', amount_str)
        
        # Handle parentheses as negative (accounting format)
        if amount_str.startswith('(') and amount_str.endswith(')'):
            amount_str = '-' + amount_str[1:-1]
        
        try:
            return float(amount_str)
        except ValueError:
            logger.debug(f"Could not parse amount: {amount_str}")
            return 0.0


# Global instance
table_extractor = TableExtractor()
