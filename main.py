from fastapi import FastAPI
from src.config.db import lifespan

app = FastAPI(
    title="Docker Test API",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """
    A simple root endpoint to confirm the API is running and accessible.
    """
    return {"status": "API is running successfully!"}