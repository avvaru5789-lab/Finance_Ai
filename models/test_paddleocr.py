"""
Quick test to verify PaddleOCR installation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.paddle_loader import paddle_loader

def test_paddleocr():
    """Test PaddleOCR loading."""
    
    print("=" * 60)
    print("PaddleOCR Installation Test")
    print("=" * 60)
    print()
    
    try:
        print("Loading PaddleOCR model...")
        ocr = paddle_loader.load_model()
        
        print("✅ SUCCESS! PaddleOCR loaded successfully")
        print()
        print("PaddleOCR is ready to use!")
        print("No model downloads needed - PaddleOCR downloads models automatically on first use")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


if __name__ == "__main__":
    success = test_paddleocr()
    sys.exit(0 if success else 1)
