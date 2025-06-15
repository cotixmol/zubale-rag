import logging
import asyncio
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.db import get_db_pool
from src.config.queue import request_queue
from src.config.secrets import secrets
from src.api import routes
from src.containers import AppContainer
from script.db_setup import initialize_database
from src.config.logger import setup_logging
from src.config import db

setup_logging()

logger = logging.getLogger(__name__)


async def worker():
    """The background worker that processes tasks from the queue."""
    logger.info("Background worker started.")

    container = AppContainer()
    container.db_pool.override(get_db_pool())

    while True:
        try:
            request = await request_queue.get()
            logger.info(f"Worker picked up request for user: {request.user_id}")

            query_usecase = container.query_processor()
            await query_usecase.execute(request.user_id, request.query)

            request_queue.task_done()
        except asyncio.CancelledError:
            logger.info("Worker shutting down gracefully.")
            break
        except Exception:
            logger.error("An error occurred in the worker:", exc_info=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown events.
    - Initializes the database connection pool.
    - Starts the background worker task.
    - Cleans up both on shutdown.
    """
    logger.info("Application startup...")

    logger.info("Attempting to connect to the database...")
    db.db_pool = await asyncpg.create_pool(
        dsn=secrets.DATABASE_URL, min_size=5, max_size=20
    )
    await initialize_database(db.db_pool)
    logger.info("Database connection pool created and seeded successfully.")

    logger.info("Starting background worker task.")
    worker_task = asyncio.create_task(worker())

    yield

    logger.info("Application shutdown...")

    logger.info("Stopping background worker task...")
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        logger.info("Background worker task cancelled successfully.")

    if db.db_pool:
        await db.db_pool.close()
        logger.info("Database connection pool closed.")


app = FastAPI(title="Product Query Bot", lifespan=lifespan)
app.include_router(routes.router)
