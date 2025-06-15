import asyncio
from src.models import QueryRequest

request_queue: asyncio.Queue[QueryRequest] = asyncio.Queue()
