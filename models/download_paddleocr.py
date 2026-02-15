"""
Download and verify PaddleOCR models.
Run this script to pre-download PaddleOCR models before using the main application.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.paddle_loader import paddle_loader


def download_paddleocr_models():
    """Download PaddleOCR models."""
    
    print("=" * 70)
    print("PaddleOCR Model Downloader")
    print("=" * 70)
    print()
    print("📦 PaddleOCR will automatically download models on first use")
    print("📁 Models will be saved to: ~/.paddleocr/")
    print("⏱️  First run may take 1-2 minutes to download models")
    print()
    print("Languages supported: en, ch, fr, german, korean, japan, etc.")
    print("Current language: English (en)")
    print()
    
    try:
        print("=" * 70)
        print("Loading PaddleOCR model (this will download if not cached)...")
        print("=" * 70)
        print()
        
        # This will trigger the download
        ocr = paddle_loader.load_model(lang='en')
        
        print()
        print("=" * 70)
        print("✅ SUCCESS! PaddleOCR is ready to use")
        print("=" * 70)
        print()
        print("📍 Models cached at: ~/.paddleocr/")
        print("🎯 OCR engine is ready for PDF/image processing")
        print()
        print("Next steps:")
        print("  1. The models are now downloaded and cached")
        print("  2. Future OCR operations will be instant (no download)")
        print("  3. You can now use the OCR engine in your application")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ FAILED: {e}")
        print("=" * 70)
        print()
        print("Troubleshooting:")
        print("  1. Make sure you have internet connection")
        print("  2. Check if conda environment is activated")
        print("  3. Verify paddleocr is installed: pip list | grep paddle")
        print()
        
        return False


if __name__ == "__main__":
    success = download_paddleocr_models()
    sys.exit(0 if success else 1)
