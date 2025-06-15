# src/config/db.py

import logging
import asyncpg

logger = logging.getLogger(__name__)

# This global variable will be managed by the lifespan function in main.py
db_pool: asyncpg.Pool | None = None


def get_db_pool() -> asyncpg.Pool:
    """
    Returns the active database connection pool.

    Raises:
        RuntimeError: If the pool has not been initialized.
    """
    if db_pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    return db_pool