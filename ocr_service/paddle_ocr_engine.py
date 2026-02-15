"""
PaddleOCR wrapper for Docker service.
Handles OCR operations without any langchain dependencies.
"""

import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from loguru import logger
from typing import List, Tuple
import io


class PaddleOCREngine:
    """Wrapper for PaddleOCR (isolated from langchain)."""
    
    def __init__(self):
        """Initialize PaddleOCR."""
        self.ocr = None
        self._initialized = False
    
    def initialize(self, lang: str = 'en', use_gpu: bool = False):
        """
        Initialize PaddleOCR model.
        
        Args:
            lang: Language code (en, ch, fr, etc.)
            use_gpu: Whether to use GPU
        """
        if self._initialized:
            logger.info("PaddleOCR already initialized")
            return
        
        logger.info(f"Initializing PaddleOCR (lang={lang}, use_gpu={use_gpu})...")
        
        try:
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=lang,
                use_gpu=use_gpu,
                show_log=False
            )
            self._initialized = True
            logger.info("✅ PaddleOCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            raise
    
    def extract_text_from_image(self, image_bytes: bytes) -> Tuple[str, List[dict]]:
        """
        Extract text from image bytes.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Tuple of (extracted_text, detection_results)
        """
        if not self._initialized:
            self.initialize()
        
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Run OCR
            result = self.ocr.ocr(img_array, cls=True)
            
            # Extract text and metadata
            text_lines = []
            detections = []
            
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 2:
                        bbox = line[0]  # Bounding box coordinates
                        text, confidence = line[1]
                        
                        if confidence > 0.5:  # Only high-confidence results
                            text_lines.append(text)
                            detections.append({
                                'text': text,
                                'confidence': float(confidence),
                                'bbox': bbox
                            })
            
            full_text = "\n".join(text_lines)
            
            logger.info(f"OCR extracted {len(text_lines)} lines of text")
            
            return full_text, detections
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise


# Global instance
paddle_engine = PaddleOCREngine()
