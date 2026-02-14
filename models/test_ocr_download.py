"""
Simple script to test and download DeepSeek-OCR model.
Run this to pre-download the model before using the main application.
"""

import os
from pathlib import Path
from loguru import logger

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.deepseek_loader import deepseek_loader


def download_deepseek_ocr():
    """Download DeepSeek-OCR model from HuggingFace."""
    
    print("=" * 60)
    print("DeepSeek-OCR Model Downloader")
    print("=" * 60)
    print()
    
    print("📦 This will download the DeepSeek-OCR model from HuggingFace")
    print("⚠️  Model size: ~2-5 GB (depending on variant)")
    print("📁 Location: ./models/deepseek-ocr/")
    print()
    
    # Check if HuggingFace token is set
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if hf_token:
        print("✅ HuggingFace token found in .env")
        os.environ["HF_TOKEN"] = hf_token
    else:
        print("⚠️  No HuggingFace token in .env (will use cached login)")
    
    print()
    print("Starting download...")
    print("-" * 60)
    
    try:
        # This will trigger the download
        model, tokenizer = deepseek_loader.load_model()
        
        print("-" * 60)
        print()
        print("✅ SUCCESS! DeepSeek-OCR model downloaded")
        print(f"📍 Device: {deepseek_loader.get_device()}")
        print(f"📁 Cached at: ./models/deepseek-ocr/")
        print()
        print("You can now use the OCR engine in your application!")
        
    except Exception as e:
        print("-" * 60)
        print()
        print(f"❌ FAILED: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure you're authenticated: huggingface-cli login")
        print("2. Check your internet connection")
        print("3. Verify model name: deepseek-ai/DeepSeek-OCR")
        print("4. Try manually: huggingface-cli download deepseek-ai/DeepSeek-OCR")
        
        return False
    
    return True


if __name__ == "__main__":
    success = download_deepseek_ocr()
    sys.exit(0 if success else 1)
