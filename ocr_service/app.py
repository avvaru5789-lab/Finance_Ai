"""
FastAPI server for PaddleOCR service.
Exposes OCR functionality via REST API.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger
import sys

from paddle_ocr_engine import paddle_engine

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")

# Create FastAPI app
app = FastAPI(
    title="PaddleOCR Service",
    description="Isolated OCR microservice using PaddleOCR",
    version="1.0.0"
)


class OCRResponse(BaseModel):
    """OCR response model."""
    text: str
    confidence: float
    detections: List[dict]
    lines_found: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


@app.on_event("startup")
async def startup_event():
    """Initialize PaddleOCR on startup."""
    logger.info("Starting PaddleOCR service...")
    try:
        paddle_engine.initialize(lang='en', use_gpu=False)
        logger.info("✅ PaddleOCR service ready")
    except Exception as e:
        logger.error(f"Failed to initialize PaddleOCR: {e}")
        raise


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "service": "PaddleOCR",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/ocr/image": "POST - OCR from image",
            "/docs": "API documentation"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="paddleocr",
        version="1.0.0"
    )


@app.post("/ocr/image", response_model=OCRResponse)
async def ocr_image(file: UploadFile = File(...)):
    """
    Perform OCR on uploaded image.
    
    Args:
        file: Image file (PNG, JPG, etc.)
        
    Returns:
        OCR results with text and detections
    """
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        logger.info(f"Processing image: {file.filename} ({len(image_bytes)} bytes)")
        
        # Run OCR
        text, detections = paddle_engine.extract_text_from_image(image_bytes)
        
        # Calculate average confidence
        avg_confidence = 0.0
        if detections:
            avg_confidence = sum(d['confidence'] for d in detections) / len(detections)
        
        return OCRResponse(
            text=text,
            confidence=avg_confidence,
            detections=detections,
            lines_found=len(detections)
        )
        
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.post("/ocr/pdf")
async def ocr_pdf(file: UploadFile = File(...)):
    """
    Perform OCR on uploaded PDF.
    
    Note: This endpoint converts PDF pages to images first.
    For text-based PDFs, use pdfplumber in the main application.
    """
    # TODO: Implement PDF to image conversion if needed
    raise HTTPException(
        status_code=501,
        detail="PDF OCR not yet implemented. Use pdfplumber in main app for text-based PDFs."
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
