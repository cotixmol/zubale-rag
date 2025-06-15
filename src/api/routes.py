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
    Validates an user query and adds it to the queue for processing.
    Responds with 202 Accepted.
    """
    try:
        logger.info(
            f"Query; {request.query} - User: {request.user_id} - Enqueuing for processing."
        )
        await request_queue.put(request)
        return {"message": "Request received and is being processed."}

    except Exception as e:
        logger.error(f"Failed to enqueue request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enqueue request for processing.",
        )


# This enpoint simulates the callback from the worker after processing the query.
@router.post("/callback", status_code=status.HTTP_200_OK)
async def receive_callback(payload: Dict[str, Any]):
    """
    A test endpoint to receive and log the final answer from the worker.
    """
    logger.info(f"Callback Payload:\n{payload}")
    return {"status": "Success", "message": "Callback received successfully."}
