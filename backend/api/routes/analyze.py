"""
Main analysis endpoint.
Complete bank statement analysis with multi-agent workflow.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from datetime import datetime
from loguru import logger
import os

from backend.api.schemas import AnalysisResponse, AnalysisSummary
from backend.services import AnalysisService

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_statement(
    file: UploadFile = File(..., description="PDF bank statement"),
    user_id: Optional[str] = Form(None, description="Optional user ID")
):
    """
    Analyze bank statement and return complete financial analysis.
    
    **Pipeline:**
    1. Extract text from PDF via OCR
    2. Parse transactions
    3. Categorize transactions
    4. Calculate financial metrics
    5. Run multi-agent analysis (Debt, Savings, Budget, Risk)
    
    **Returns:**
    - Complete financial analysis
    - Debt payoff strategy
    - Savings recommendations
    - Budget optimizations
    - Risk assessment
    
    Args:
        file: PDF bank statement file
        user_id: Optional user identifier
        
    Returns:
        Complete analysis with all agent outputs
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a PDF bank statement."
        )
    
    try:
        # Read file
        pdf_bytes = await file.read()
        logger.info(f"Received file: {file.filename} ({len(pdf_bytes)} bytes)")
        
        # Get API key from environment
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENROUTER_API_KEY not configured"
            )
        
        # Run analysis
        service = AnalysisService(api_key)
        result = await service.analyze_bank_statement(pdf_bytes, user_id)
        
        # Format response
        response = _format_analysis_response(result)
        
        logger.info(f"✅ Analysis complete: {response.analysis_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


def _format_analysis_response(result: dict) -> AnalysisResponse:
    """
    Format LangGraph result into API response.
    
    The result is a FinancialState TypedDict with flat metric fields
    (total_income, total_expenses, etc.) — NOT nested under a 'metrics' key.
    """
    # FinancialState stores metrics as flat fields, not in a 'metrics' dict
    summary = AnalysisSummary(
        total_income=result.get("total_income", 0.0),
        total_expenses=result.get("total_expenses", 0.0),
        net_income=result.get("net_income", 0.0),
        savings_rate=result.get("savings_rate", 0.0),
        debt_to_income_ratio=result.get("debt_to_income_ratio", 0.0)
    )
    
    # Convert agent outputs to dicts
    analysis = {}
    if result.get("debt_analysis"):
        analysis["debt"] = result["debt_analysis"].dict()
    if result.get("savings_strategy"):
        analysis["savings"] = result["savings_strategy"].dict()
    if result.get("budget_recommendations"):
        analysis["budget"] = result["budget_recommendations"].dict()
    if result.get("risk_score"):
        analysis["risk"] = result["risk_score"].dict()
    
    # Convert transactions and debt accounts
    transactions = []
    for t in result.get("transactions", []):
        if hasattr(t, 'dict'):
            transactions.append(t.dict())
        else:
            transactions.append(t)
    
    debt_accounts = []
    for d in result.get("debt_accounts", []):
        if hasattr(d, 'dict'):
            debt_accounts.append(d.dict())
        else:
            debt_accounts.append(d)
    
    return AnalysisResponse(
        analysis_id=result.get("analysis_id", "unknown"),
        timestamp=datetime.utcnow(),
        status=result.get("processing_status", "unknown"),
        summary=summary,
        transactions=transactions,
        debt_accounts=debt_accounts,
        analysis=analysis,
        errors=result.get("errors", []),
        warnings=[]
    )


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    """
    Retrieve a previously completed analysis by ID.
    
    TODO: Implement database storage and retrieval.
    
    Args:
        analysis_id: Analysis identifier
        
    Returns:
        Previously completed analysis
    """
    # TODO: Retrieve from database
    raise HTTPException(
        status_code=501,
        detail="Analysis retrieval not implemented yet. Store results in database first."
    )
