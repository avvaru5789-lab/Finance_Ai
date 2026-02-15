"""
FastAPI Application - AI Financial Coach Backend

Main entry point for the FastAPI backend server.
Provides REST API for bank statement analysis using multi-agent LangGraph workflow.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


from backend.api.routes import health, analyze, ocr, transactions
from backend.api.middleware import add_error_handlers

# Initialize FastAPI app
app = FastAPI(
    title="AI Financial Coach API",
    description="""
    Multi-agent financial analysis system powered by LangGraph.
    
    ## Features
    - **PDF Upload**: Upload bank statements for analysis
    - **OCR Processing**: Extract text from PDFs
    - **Transaction Categorization**: Automatically categorize expenses
    - **Multi-Agent Analysis**:
        - Debt Analyzer: Payoff strategies
        - Savings Strategy: Emergency fund planning
        - Budget Optimizer: Spending optimizations
        - Risk Scorer: Financial health assessment
    
    ## Pipeline
    PDF → OCR → Parse → Categorize → Metrics → LangGraph → JSON Response
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["OCR"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])

# Add error handlers
add_error_handlers(app)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("=" * 70)
    logger.info("🚀 AI Financial Coach API Starting...")
    logger.info("=" * 70)
    logger.info(f"Version: {app.version}")
    logger.info(f"CORS Origins: {cors_origins}")
    logger.info(f"OpenRouter API Key: {'✅ Set' if os.getenv('OPENROUTER_API_KEY') else '❌ Missing'}")
    logger.info(f"OCR Service URL: {os.getenv('OCR_SERVICE_URL', 'http://localhost:8001')}")
    logger.info("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("🛑 AI Financial Coach API Shutting Down...")


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
