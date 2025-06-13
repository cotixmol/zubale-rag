#DB Pool using asyncpg# Wrapper for asyncio.Queue# src/config/db.py
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .secrets import secrets

db_pool: asyncpg.Pool | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events to manage the database connection pool.
    """
    print("API Lifespan: Startup event triggered.")
    print("API Lifespan: Attempting to connect to the database...")
    
    global db_pool
    db_pool = await asyncpg.create_pool(
        dsn=secrets.DATABASE_URL,
        min_size=5,
        max_size=20
    )
    # This print statement is our proof that the connection was successful.
    print("API Lifespan: Database connection pool created successfully.")
    
    yield
    
    print("API Lifespan: Shutdown event triggered.")
    if db_pool:
        await db_pool.close()
        print("API Lifespan: Database connection pool closed.")