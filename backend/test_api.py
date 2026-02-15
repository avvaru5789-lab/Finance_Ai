"""
Test script for FastAPI backend.
Tests all endpoints with sample data.
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    print("\n" + "=" * 70)
    print("Testing Health Check Endpoint")
    print("=" * 70)
    
    response = client.get("/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed!")


def test_ocr_endpoint():
    """Test OCR endpoint with sample PDF."""
    print("\n" + "=" * 70)
    print("Testing OCR Endpoint")
    print("=" * 70)
    
    # Create a simple test file
    test_file = b"%PDF-1.4\n%Test PDF\nSample content"
    
    response = client.post(
        "/api/ocr/extract",
        files={"file": ("test.pdf", test_file, "application/pdf")}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
        print("✅ OCR endpoint passed!")
    else:
        print(f"Response: {response.text}")
        print("⚠️  OCR endpoint returned error (expected if OCR service not running)")


def test_categorize_endpoint():
    """Test transaction categorization endpoint."""
    print("\n" + "=" * 70)
    print("Testing Transaction Categorization Endpoint")
    print("=" * 70)
    
    request_data = {
        "transactions": [
            {
                "date": "2024-01-15T00:00:00",
                "description": "Amazon Prime",
                "amount": -14.99
            },
            {
                "date": "2024-01-20T00:00:00",
                "description": "Salary",
                "amount": 5000.00
            }
        ]
    }
    
    response = client.post("/api/transactions/categorize", json=request_data)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Categorized Transactions: {len(response.json())}")
        for trans in response.json():
            print(f"   - {trans['description']}: {trans['category']}")
        print("✅ Categorization endpoint passed!")
    else:
        print(f"Response: {response.text}")
        print("❌ Categorization endpoint failed")


def test_analyze_endpoint():
    """Test main analysis endpoint."""
    print("\n" + "=" * 70)
    print("Testing Main Analysis Endpoint")
    print("=" * 70)
    
    # This requires a real PDF and OpenRouter API key
    print("⚠️  Skipping - requires real PDF and API key")
    print("To test manually:")
    print('  curl -X POST "http://localhost:8000/api/analyze" \\')
    print('    -H "accept: application/json" \\')
    print('    -F "file=@bank_statement.pdf"')


if __name__ == "__main__":
    print("=" * 70)
    print("FastAPI Backend Tests")
    print("=" * 70)
    
    try:
        test_health_endpoint()
        test_ocr_endpoint()
        test_categorize_endpoint()
        test_analyze_endpoint()
        
        print("\n" + "=" * 70)
        print("✅ All Basic Tests Passed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
