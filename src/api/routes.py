from fastapi import APIRouter, status, HTTPException
from src.models.query import QueryRequest
from src.config.queue import request_queue
import logging
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/query", status_code=status.HTTP_202_ACCEPTED)
async def accept_query(request: QueryRequest):
    """
    Accepts a user query, validates it, and adds it to the background
    processing queue. Responds immediately with 202 Accepted.
    """
    try:
        logger.info(
            f"Received query for user_id: {request.user_id}. Enqueuing for processing."
        )
        await request_queue.put(request)
        return {"message": "Request received and is being processed."}
    except Exception as e:
        logger.error(f"Failed to enqueue request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enqueue request for processing.",
        )


# --- ENDPOINT TO SIMULATE A CALLBACK ROUTE ---
@router.post("/callback", status_code=status.HTTP_200_OK)
async def receive_callback(payload: Dict[str, Any]):
    """
    A simple test endpoint to receive and log the final answer from the worker.
    """
    logger.info(f"Received callback with payload:\n{payload}")
    return {"status": "callback received"}
