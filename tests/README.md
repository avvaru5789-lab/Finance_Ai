# AI Financial Coach - Testing Guide

## Integration Tests

### Quick Start

```bash
# 1. Set your API key
export OPENROUTER_API_KEY='your-key-here'

# 2. Run tests
./run_tests.sh
```

### What Gets Tested

#### Test 1: Component Isolation
- ✅ OCR Engine initialization
- ✅ Transaction Categorizer (3 test transactions)
- ✅ Metrics Engine calculations

#### Test 2: Simple Text Analysis
- ✅ End-to-end pipeline with sample statement
- ✅ Transaction extraction
- ✅ Categorization
- ✅ Metrics calculation
- ✅ All 4 AI agents (Debt, Savings, Budget, Risk)
- ✅ Response validation

#### Test 3: Error Handling
- ✅ Empty input handling
- ✅ Malformed text handling
- ✅ Graceful degradation

### Test Data

Sample statements in `test_data/sample_statements.py`:
- `SIMPLE_STATEMENT` - 10 transactions, basic case
- `COMPLEX_STATEMENT` - 60+ transactions, realistic
- `EDGE_CASE_HIGH_DEBT` - $90K debt scenario
- `EDGE_CASE_NO_INCOME` - Student with no income

### Expected Results

**Component Tests:**
- All components initialize ✅
- Transactions categorized correctly ✅
- Metrics calculated accurately ✅

**Integration Test:**
- Completes in < 35 seconds ⏱️
- Finds all transactions 📊
- All 4 AI analyses present 🤖
- Recommendations make sense 💡

### Test Output

```
🧪 AI Financial Coach - Integration Test Suite
📅 2024-02-15 16:45:00

============================================================
TEST 1: Component Isolation
============================================================
📄 Testing OCR Engine...
   ✅ OCR Engine initialized
🏷️  Testing Transaction Categorizer...
   ✅ Categorized 3 transactions correctly
🧮 Testing Metrics Engine...
   ✅ Metrics calculated: Income=$5000.0, Expenses=$95.0

============================================================
TEST 2: Simple Text Analysis
============================================================
✅ Analysis completed in 28.45 seconds

Transactions found: 10

Summary:
{'total_income': 5000.0,
 'total_expenses': 2875.0,
 'net_income': 2125.0,
 'savings_rate': 42.5}

============================================================
TEST SUMMARY
============================================================
✅ PASS Component Isolation
✅ PASS Simple Text Analysis
   ⏱️  Time: 28.45s
   📊 Transactions: 10
✅ PASS Error Handling

============================================================
RESULTS: 3/3 tests passed
============================================================
```

### Run Individual Test Scenarios

```python
from test_data.sample_statements import (
    SIMPLE_STATEMENT,
    COMPLEX_STATEMENT,
    EDGE_CASE_HIGH_DEBT,
    EDGE_CASE_NO_INCOME
)

# Test with different scenarios
result = await service._analyze_with_langgraph(COMPLEX_STATEMENT)
```

### Troubleshooting

**API Key Issues:**
```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set temporarily
export OPENROUTER_API_KEY='sk-...'

# Set permanently (add to ~/.zshrc or ~/.bashrc)
echo 'export OPENROUTER_API_KEY="sk-..."' >> ~/.zshrc
```

**Import Errors:**
```bash
# Ensure you're in Finance_env
conda activate Finance_env

# Install dependencies
pip install -r requirements.txt
```

**Slow Tests:**
- Expected: 25-35 seconds for full integration test
- OCR can be slow on first run
- AI agents make 4 sequential LLM calls

### Performance Benchmarks

| Stage | Expected Time |
|-------|--------------|
| Component Tests | < 1s |
| Text Analysis | 25-35s |
| Error Handling | < 5s |
| **Total** | **~ 30-40s** |

### Adding New Tests

```python
async def test_my_feature(self):
    """Test description."""
    print("\n" + "="*60)
    print("TEST X: My Feature")
    print("="*60)
    
    # Your test code here
    
    self.results.append({
        'test': 'My Feature',
        'status': '✅ PASS',
    })
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
- name: Run Integration Tests
  run: |
    export OPENROUTER_API_KEY=${{ secrets.OPENROUTER_API_KEY }}
    ./run_tests.sh
```

---

**Ready to test!** Run `./run_tests.sh` to validate your system! 🧪
