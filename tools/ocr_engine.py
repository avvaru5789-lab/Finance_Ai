"""
OCR Engine using Docker PaddleOCR service for PDF and image processing.
Extracts text and tables from financial documents.
"""

import os
import httpx
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
from PIL import Image
import io

# PDF processing
from pdf2image import convert_from_path
import pdfplumber


class OCREngine:
    """Handles OCR extraction from PDFs and images using Docker PaddleOCR service."""
    
    def __init__(self, ocr_service_url: str = "http://localhost:8001"):
        """
        Initialize OCR engine.
        
        Args:
            ocr_service_url: URL of Docker OCR service
        """
        self.ocr_service_url = ocr_service_url
        self._service_available = None
    
    def _check_ocr_service(self) -> bool:
        """Check if Docker OCR service is available."""
        if self._service_available is not None:
            return self._service_available
        
        try:
            response = httpx.get(f"{self.ocr_service_url}/health", timeout=2.0)
            self._service_available = response.status_code == 200
            if self._service_available:
                logger.info("✅ Docker OCR service is available")
            return self._service_available
        except Exception as e:
            logger.warning(f"Docker OCR service not available: {e}")
            self._service_available = False
            return False
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text and tables from a PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text, tables, and metadata
        """
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
        
        # Fallback to Docker OCR service for scanned PDFs
        if self._check_ocr_service():
            logger.info("Using Docker PaddleOCR service for image-based PDF")
            return self._extract_with_docker_ocr(pdf_path)
        else:
            logger.error("Docker OCR service unavailable and pdfplumber failed")
            return {
                "method": "failed",
                "text": "",
                "pages": self._count_pages(pdf_path),
                "tables": [],
                "error": "OCR service unavailable"
            }
    
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
    
    def _extract_with_docker_ocr(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text using Docker PaddleOCR service (for scanned/image-based PDFs).
        
        This converts PDF to images and sends to Docker service.
        """
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=200)
        
        all_text = []
        all_detections = []
        
        for i, image in enumerate(images):
            logger.info(f"Processing page {i+1}/{len(images)} with Docker OCR")
            
            # Run OCR via Docker service
            page_text, detections = self._ocr_image_via_docker(image)
            all_text.append(page_text)
            all_detections.extend(detections)
        
        return {
            "method": "docker_paddleocr",
            "text": "\n\n".join(all_text),
            "pages": len(images),
            "tables": [],  # Table extraction handled by table_extractor
            "detections": all_detections
        }
    
    def _ocr_image_via_docker(self, image: Image.Image) -> tuple[str, List[dict]]:
        """
        Run OCR on a single image via Docker service.
        
        Args:
            image: PIL Image object
            
        Returns:
            Tuple of (extracted_text, detections)
        """
        try:
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Send to Docker OCR service
            files = {"file": ("image.png", img_byte_arr, "image/png")}
            
            response = httpx.post(
                f"{self.ocr_service_url}/ocr/image",
                files=files,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["text"], result.get("detections", [])
            else:
                logger.error(f"OCR service returned error: {response.status_code}")
                return "", []
            
        except Exception as e:
            logger.error(f"OCR failed via Docker service: {e}")
            return "", []
    
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


# Global instance
ocr_engine = OCREngine()
