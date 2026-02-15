"""
OCR extraction endpoints.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from loguru import logger
import io

from backend.api.schemas import OCRResponse
from tools.ocr_engine import OCREngine

router = APIRouter()


@router.post("/extract", response_model=OCRResponse)
async def extract_text(
    file: UploadFile = File(..., description="PDF file to extract text from")
):
    """
    Extract text from PDF using OCR.
    
    Args:
        file: PDF file upload
        
    Returns:
        Extracted text and metadata
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Read file content
        pdf_bytes = await file.read()
        logger.info(f"Processing PDF: {file.filename} ({len(pdf_bytes)} bytes)")
        
        # Create OCR engine and extract
        ocr_engine = OCREngine()
        result = ocr_engine.extract_from_pdf(io.BytesIO(pdf_bytes))
        
        logger.info(f"OCR extraction complete: {len(result['text'])} characters")
        
        return OCRResponse(
            text=result["text"],
            method=result["method"],
            pages=result.get("pages", 1),
            confidence=result.get("confidence")
        )
        
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"OCR extraction failed: {str(e)}"
        )
