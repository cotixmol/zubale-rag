import asyncio
from src.models.query import QueryRequest

request_queue: asyncio.Queue[QueryRequest] = asyncio.Queue()
