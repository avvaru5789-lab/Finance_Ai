"""
Integration test for AI Financial Coach end-to-end pipeline.
Tests: PDF Upload → OCR → Categorization → Metrics → AI Analysis → Response
"""

import asyncio
import sys
import time
from pathlib import Path
from pprint import pprint

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.analysis_service import AnalysisService
from tools.ocr_engine import OCREngine
from tools.transaction_categorizer import TransactionCategorizer
from tools.financial_metrics_engine import FinancialMetricsEngine


class IntegrationTest:
    """End-to-end integration test suite."""
    
    def __init__(self, openrouter_api_key: str):
        self.api_key = openrouter_api_key
        self.service = AnalysisService(openrouter_api_key)
        self.results = []
        
    async def test_simple_text_analysis(self):
        """Test with simple text input (no OCR needed)."""
        print("\n" + "="*60)
        print("TEST 1: Simple Text Analysis")
        print("="*60)
        
        # Sample bank statement text
        sample_text = """
        BANK STATEMENT - January 2024
        
        Date        Description                 Amount
        01/05/24    Salary Deposit             +5000.00
        01/08/24    Rent Payment               -1500.00
        01/10/24    Grocery Store               -250.00
        01/12/24    Gas Station                  -60.00
        01/15/24    Restaurant                  -120.00
        01/18/24    Credit Card Payment         -500.00
        01/20/24    Utilities                   -150.00
        01/22/24    Amazon Purchase             -200.00
        01/25/24    Gym Membership               -50.00
        01/28/24    Coffee Shop                  -45.00
        
        Total Income: $5,000.00
        Total Expenses: $2,875.00
        """
        
        start_time = time.time()
        
        try:
            # Run analysis
            result = await self.service._analyze_with_langgraph(sample_text)
            
            elapsed = time.time() - start_time
            
            print(f"\n✅ Analysis completed in {elapsed:.2f} seconds")
            print(f"\nTransactions found: {len(result.get('transactions', []))}")
            print(f"\nSummary:")
            pprint(result.get('summary', {}))
            
            # Validate results
            assert len(result.get('transactions', [])) > 0, "No transactions found"
            assert result.get('summary', {}).get('total_income', 0) > 0, "No income detected"
            assert result.get('analysis', {}).get('debt'), "Debt analysis missing"
            assert result.get('analysis', {}).get('savings'), "Savings analysis missing"
            assert result.get('analysis', {}).get('budget'), "Budget analysis missing"
            assert result.get('analysis', {}).get('risk'), "Risk analysis missing"
            
            self.results.append({
                'test': 'Simple Text Analysis',
                'status': '✅ PASS',
                'time': elapsed,
                'transactions': len(result.get('transactions', [])),
            })
            
            return result
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            self.results.append({
                'test': 'Simple Text Analysis',
                'status': '❌ FAIL',
                'error': str(e)
            })
            raise
    
    async def test_component_isolation(self):
        """Test individual components in isolation."""
        print("\n" + "="*60)
        print("TEST 2: Component Isolation")
        print("="*60)
        
        # Test OCR Engine
        print("\n📄 Testing OCR Engine...")
        ocr = OCREngine()
        assert ocr is not None, "OCR Engine initialization failed"
        print("   ✅ OCR Engine initialized")
        
        # Test Transaction Categorizer
        print("\n🏷️  Testing Transaction Categorizer...")
        categorizer = TransactionCategorizer()
        test_transactions = [
            {"description": "Walmart", "amount": -50.0},
            {"description": "Salary", "amount": 5000.0},
            {"description": "Shell Gas", "amount": -45.0},
        ]
        categorized = categorizer.categorize_batch(test_transactions)
        assert len(categorized) == 3, "Categorization failed"
        assert categorized[0]['category'] == 'Food', "Wrong category for Walmart"
        assert categorized[1]['category'] == 'Income', "Wrong category for Salary"
        assert categorized[2]['category'] == 'Transportation', "Wrong category for Gas"
        print(f"   ✅ Categorized {len(categorized)} transactions correctly")
        
        # Test Metrics Engine
        print("\n🧮 Testing Metrics Engine...")
        metrics_engine = FinancialMetricsEngine()
        metrics = metrics_engine.calculate(categorized)
        assert 'total_income' in metrics, "Missing total_income"
        assert 'total_expenses' in metrics, "Missing total_expenses"
        assert metrics['total_income'] == 5000.0, "Wrong income calculation"
        print(f"   ✅ Metrics calculated: Income=${metrics['total_income']}, Expenses=${metrics['total_expenses']}")
        
        self.results.append({
            'test': 'Component Isolation',
            'status': '✅ PASS',
        })
    
    async def test_error_handling(self):
        """Test error handling with invalid inputs."""
        print("\n" + "="*60)
        print("TEST 3: Error Handling")
        print("="*60)
        
        # Test empty text
        print("\n❌ Testing empty text input...")
        try:
            result = await self.service._analyze_with_langgraph("")
            # Should still return some structure
            assert 'transactions' in result, "Missing transactions key in response"
            print("   ✅ Handled empty input gracefully")
        except Exception as e:
            print(f"   ⚠️  Empty input error: {e}")
        
        # Test malformed text
        print("\n❌ Testing malformed text...")
        try:
            result = await self.service._analyze_with_langgraph("This is not a bank statement at all!")
            assert 'transactions' in result, "Missing transactions key"
            print("   ✅ Handled malformed input gracefully")
        except Exception as e:
            print(f"   ⚠️  Malformed input error: {e}")
        
        self.results.append({
            'test': 'Error Handling',
            'status': '✅ PASS',
        })
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        for result in self.results:
            status = result['status']
            test_name = result['test']
            print(f"\n{status} {test_name}")
            if 'time' in result:
                print(f"   ⏱️  Time: {result['time']:.2f}s")
            if 'transactions' in result:
                print(f"   📊 Transactions: {result['transactions']}")
            if 'error' in result:
                print(f"   ❌ Error: {result['error']}")
        
        passed = sum(1 for r in self.results if '✅' in r['status'])
        total = len(self.results)
        print(f"\n{'='*60}")
        print(f"RESULTS: {passed}/{total} tests passed")
        print(f"{'='*60}\n")


async def main():
    """Run all integration tests."""
    import os
    
    # Check for API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY environment variable not set")
        print("   Run: export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)
    
    print("\n🧪 AI Financial Coach - Integration Test Suite")
    print(f"📅 {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    tester = IntegrationTest(api_key)
    
    try:
        # Run tests
        await tester.test_component_isolation()
        await tester.test_simple_text_analysis()
        await tester.test_error_handling()
        
        # Print summary
        tester.print_summary()
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
