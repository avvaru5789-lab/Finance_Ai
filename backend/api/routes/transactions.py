"""
Transaction categorization endpoints.
"""

from fastapi import APIRouter, HTTPException
from loguru import logger

from backend.api.schemas import CategorizeRequest, TransactionResponse
from tools.transaction_categorizer import TransactionCategorizer

router = APIRouter()


@router.post("/categorize", response_model=list[TransactionResponse])
async def categorize_transactions(request: CategorizeRequest):
    """
    Categorize a list of transactions.
    
    Args:
        request: List of transactions to categorize
        
    Returns:
        Categorized transactions with confidence scores
    """
    try:
        logger.info(f"Categorizing {len(request.transactions)} transactions")
        
        # Convert to dict format
        transactions = [t.dict() for t in request.transactions]
        
        categorizer = TransactionCategorizer()
        categorized = categorizer.categorize(transactions)
        
        # Convert to response format
        responses = []
        for i, trans in enumerate(categorized):
            responses.append(TransactionResponse(
                id=f"trans_{i}",
                date=trans["date"],
                description=trans["description"],
                amount=trans["amount"],
                category=trans.get("category", "Uncategorized"),
                confidence=trans.get("confidence")
            ))
        
        logger.info(f"Categorization complete")
        return responses
        
    except Exception as e:
        logger.error(f"Categorization failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Transaction categorization failed: {str(e)}"
        )
