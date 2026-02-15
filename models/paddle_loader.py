"""
PaddleOCR model loader and manager.
Handles loading and caching of PaddleOCR for OCR tasks.
"""

import os
from typing import Optional
from loguru import logger

# CRITICAL: Import compatibility shim BEFORE paddleocr
from . import paddle_compat_fix

from paddleocr import PaddleOCR


class PaddleOCRLoader:
    """Singleton loader for PaddleOCR model."""
    
    def __init__(self):
        """Initialize the loader."""
        self.ocr = None
        self._initialized = False
    
    def load_model(self, lang: str = 'en') -> PaddleOCR:
        """
        Load PaddleOCR model.
        
        Args:
            lang: Language code (default: 'en' for English)
            
        Returns:
            PaddleOCR instance
        """
        if self._initialized and self.ocr is not None:
            logger.info("PaddleOCR already loaded, returning cached instance")
            return self.ocr
        
        try:
            logger.info(f"Loading PaddleOCR model (lang={lang})...")
            
            # Initialize PaddleOCR
            # use_angle_cls=True enables text direction detection
            # use_gpu=False for CPU (set to True if you have GPU)
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=lang,
                use_gpu=False,  # Set to True if you have GPU
                show_log=False
            )
            
            self._initialized = True
            logger.info("✅ PaddleOCR model loaded successfully")
            logger.info("   Models downloaded to: ~/.paddleocr/")
            
            return self.ocr
            
        except Exception as e:
            logger.error(f"Failed to load PaddleOCR model: {e}")
            raise
    
    def get_model(self) -> Optional[PaddleOCR]:
        """Get the loaded PaddleOCR model."""
        if not self._initialized:
            return self.load_model()
        return self.ocr
    
    def unload_model(self) -> None:
        """Unload the model to free up memory."""
        if self._initialized:
            self.ocr = None
            self._initialized = False
            logger.info("PaddleOCR model unloaded")
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._initialized


# Global singleton instance
paddle_loader = PaddleOCRLoader()
