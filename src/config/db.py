import logging
import asyncpg

logger = logging.getLogger(__name__)
db_pool: asyncpg.Pool | None = None


def get_db_pool() -> asyncpg.Pool:
    """
    Returns the active database connection pool.
    """
    if db_pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    return db_pool
