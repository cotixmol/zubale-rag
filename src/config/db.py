import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .secrets import secrets
from script.db_setup import initialize_database

db_pool: asyncpg.Pool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events to manage the database connection pool.
    """
    print("API Lifespan: Attempting to connect to the database...")

    global db_pool
    db_pool = await asyncpg.create_pool(
        dsn=secrets.DATABASE_URL, min_size=5, max_size=20
    )
    print("API Lifespan: Database connection pool created successfully.")

    await initialize_database(db_pool)

    yield

    print("API Lifespan: Shutdown event triggered.")
    if db_pool:
        await db_pool.close()
        print("API Lifespan: Database connection pool closed.")
