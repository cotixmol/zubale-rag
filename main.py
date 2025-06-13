import logging
import asyncio
from fastapi import FastAPI
from src.config.db import lifespan, get_db_pool
from src.config.queue import request_queue
from src.api import routes
from src.usecases.process_query import QueryProcessor

from src.repositories.product_repo import PostgresProductRepository
from src.services import (
    ProductRetrievalService,
    StubbedGenerationService,
    WebhookCallbackService,
)

logger = logging.getLogger(__name__)


async def worker():
    """The background worker that processes tasks from the queue."""
    logger.info("Background worker started.")

    product_repo = PostgresProductRepository(pool=get_db_pool())

    query_usecase = QueryProcessor(
        retrieval_service=ProductRetrievalService(repository=product_repo),
        generation_service=StubbedGenerationService(),
        callback_service=WebhookCallbackService(),
    )

    while True:
        try:
            request = await request_queue.get()
            logger.info(f"Worker picked up request for user: {request.user_id}")

            await query_usecase.execute(request.user_id, request.query)

            request_queue.task_done()
        except asyncio.CancelledError:
            logger.info("Worker shutting down.")
            break
        except Exception:
            logger.error("An error occurred in the worker:", exc_info=True)


app = FastAPI(title="Product Query Bot", lifespan=lifespan)
app.include_router(routes.router)
