import logging
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .secrets import secrets
from script.db_setup import initialize_database

logger = logging.getLogger(__name__)
db_pool: asyncpg.Pool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events to manage the database connection pool.
    """
    global db_pool
    logger.info("Attempting to connect to the database...")
    db_pool = await asyncpg.create_pool(
        dsn=secrets.DATABASE_URL, min_size=5, max_size=20
    )
    await initialize_database(db_pool)

    logger.info("Database connection pool created and seeded successfully.")

    yield

    if db_pool:
        await db_pool.close()
        logger.info("API Lifespan: Database connection pool closed.")


def get_db_pool() -> asyncpg.Pool:
    if db_pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    return db_pool
