"""
OCR Engine using DeepSeek-OCR for PDF and image processing.
Extracts text and tables from financial documents.
"""

import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from loguru import logger
from PIL import Image
import torch

# PDF processing
from pdf2image import convert_from_path
import pdfplumber

from models.deepseek_loader import deepseek_loader


class OCREngine:
    """Handles OCR extraction from PDFs and images using DeepSeek-OCR."""
    
    def __init__(self):
        """Initialize OCR engine with DeepSeek model."""
        self.model = None
        self.tokenizer = None
        self.device = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Load DeepSeek-OCR model (lazy loading)."""
        if self._initialized:
            return
        
        try:
            logger.info("Initializing DeepSeek-OCR model...")
            self.model, self.tokenizer = deepseek_loader.load_model()
            self.device = deepseek_loader.get_device()
            self._initialized = True
            logger.info(f"OCR engine initialized on {self.device}")
        except Exception as e:
            logger.error(f"Failed to initialize OCR engine: {e}")
            raise
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text and tables from a PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text, tables, and metadata
        """
        self.initialize()
        
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Try pdfplumber first for text-based PDFs (faster)
        try:
            text_content = self._extract_with_pdfplumber(pdf_path)
            if text_content and len(text_content.strip()) > 100:
                logger.info("Successfully extracted with pdfplumber (text-based PDF)")
                return {
                    "method": "pdfplumber",
                    "text": text_content,
                    "pages": self._count_pages(pdf_path),
                    "tables": self._extract_tables_pdfplumber(pdf_path),
                }
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
        
        # Fallback to DeepSeek-OCR for scanned PDFs
        logger.info("Using DeepSeek-OCR for image-based PDF")
        return self._extract_with_deepseek_ocr(pdf_path)
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber (for text-based PDFs)."""
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        return "\n\n".join(text_content)
    
    def _extract_tables_pdfplumber(self, pdf_path: str) -> List[List[List[str]]]:
        """Extract tables using pdfplumber."""
        all_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
        
        return all_tables
    
    def _extract_with_deepseek_ocr(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text using DeepSeek-OCR (for scanned/image-based PDFs).
        
        This is slower but works on scanned documents.
        """
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=200)
        
        all_text = []
        all_tables = []
        
        for i, image in enumerate(images):
            logger.info(f"Processing page {i+1}/{len(images)} with DeepSeek-OCR")
            
            # Run OCR on the image
            page_text = self._ocr_image(image)
            all_text.append(page_text)
            
            # TODO: Implement table detection with DeepSeek-OCR
            # For now, we'll extract tables in the table_extractor.py
        
        return {
            "method": "deepseek_ocr",
            "text": "\n\n".join(all_text),
            "pages": len(images),
            "tables": all_tables,
        }
    
    def _ocr_image(self, image: Image.Image) -> str:
        """
        Run DeepSeek-OCR on a single image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text
        """
        try:
            # Prepare image for DeepSeek-OCR
            # Note: DeepSeek-OCR API may vary - adjust based on actual model
            
            # Convert PIL image to tensor
            # This is a simplified version - adjust based on DeepSeek-OCR's actual API
            
            # For now, use a placeholder since we don't have the exact DeepSeek-OCR API
            # You'll need to check the HuggingFace model card for the correct usage
            
            logger.warning("DeepSeek-OCR integration pending - using placeholder")
            return "[OCR text will appear here after DeepSeek-OCR integration]"
            
            # TODO: Replace with actual DeepSeek-OCR inference:
            # inputs = self.tokenizer(image, return_tensors="pt").to(self.device)
            # outputs = self.model.generate(**inputs)
            # text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # return text
            
        except Exception as e:
            logger.error(f"OCR failed on image: {e}")
            return ""
    
    def extract_from_csv(self, csv_path: str) -> Dict[str, any]:
        """
        Extract data from CSV file (no OCR needed).
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            Dictionary with CSV data
        """
        import pandas as pd
        
        logger.info(f"Reading CSV: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            
            return {
                "method": "csv",
                "data": df.to_dict(orient='records'),
                "columns": df.columns.tolist(),
                "rows": len(df),
            }
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            raise
    
    def _count_pages(self, pdf_path: str) -> int:
        """Count number of pages in PDF."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        except:
            return 0
    
    def cleanup(self) -> None:
        """Free up model memory."""
        if self._initialized:
            deepseek_loader.unload_model()
            self._initialized = False
            logger.info("OCR engine cleaned up")


# Global instance
ocr_engine = OCREngine()
