"""
DeepSeek-OCR model loader and manager.
Handles downloading and loading the DeepSeek-OCR model from HuggingFace.
"""

import os
from pathlib import Path
from typing import Optional
from loguru import logger
from transformers import AutoModel, AutoTokenizer
import torch

from backend.config.settings import settings


class DeepSeekOCRLoader:
    """Manages loading and caching of DeepSeek-OCR model."""
    
    _model: Optional[AutoModel] = None
    _tokenizer: Optional[AutoTokenizer] = None
    _device: str = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def load_model(cls) -> tuple[AutoModel, AutoTokenizer]:
        """
        Load DeepSeek-OCR model and tokenizer.
        Downloads from HuggingFace if not cached locally.
        
        Returns:
            Tuple of (model, tokenizer)
        """
        if cls._model is not None and cls._tokenizer is not None:
            logger.info("Using cached DeepSeek-OCR model")
            return cls._model, cls._tokenizer
        
        try:
            logger.info(f"Loading DeepSeek-OCR model from: {settings.deepseek_ocr_model}")
            logger.info(f"Device: {cls._device}")
            
            # Ensure model directory exists
            Path(settings.deepseek_ocr_path).mkdir(parents=True, exist_ok=True)
            
            # Load tokenizer
            logger.info("Loading tokenizer...")
            cls._tokenizer = AutoTokenizer.from_pretrained(
                settings.deepseek_ocr_model,
                cache_dir=settings.deepseek_ocr_path,
                trust_remote_code=True
            )
            
            # Load model
            logger.info("Loading model...")
            cls._model = AutoModel.from_pretrained(
                settings.deepseek_ocr_model,
                cache_dir=settings.deepseek_ocr_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if cls._device == "cuda" else torch.float32
            )
            
            # Move to appropriate device
            cls._model = cls._model.to(cls._device)
            cls._model.eval()  # Set to evaluation mode
            
            logger.info(f"DeepSeek-OCR model loaded successfully on {cls._device}")
            
            return cls._model, cls._tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load DeepSeek-OCR model: {e}")
            raise RuntimeError(f"DeepSeek-OCR initialization failed: {e}")
    
    @classmethod
    def get_model(cls) -> tuple[AutoModel, AutoTokenizer]:
        """
        Get cached model or load if not cached.
        
        Returns:
            Tuple of (model, tokenizer)
        """
        if cls._model is None or cls._tokenizer is None:
            return cls.load_model()
        return cls._model, cls._tokenizer
    
    @classmethod
    def get_device(cls) -> str:
        """Get the device being used (cuda/cpu)."""
        return cls._device
    
    @classmethod
    def unload_model(cls) -> None:
        """Unload model from memory to free resources."""
        if cls._model is not None:
            del cls._model
            cls._model = None
            
        if cls._tokenizer is not None:
            del cls._tokenizer
            cls._tokenizer = None
            
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        logger.info("DeepSeek-OCR model unloaded from memory")


# Global instance
deepseek_loader = DeepSeekOCRLoader()
