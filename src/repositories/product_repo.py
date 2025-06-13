from abc import ABC, abstractmethod
import asyncpg
from src.models.query import ProductDocument


class ProductRepository(ABC):
    @abstractmethod
    async def index_documents(self, documents: list[ProductDocument]):
        """Saves product documents, including their embeddings, to the database."""
        pass

    @abstractmethod
    async def semantic_search(
        self, embedding: list[float], top_k: int
    ) -> list[ProductDocument]:
        """Performs a semantic search to find the top_k most similar documents."""
        pass


class PostgresProductRepository:
    """The actual implementation that talks to our PostgreSQL database."""

    def __init__(self, db: asyncpg.Pool):
        self._db = db

    async def index_documents(self, documents: list[ProductDocument]):
        async with self._db.acquire() as conn:
            await conn.executemany(
                "INSERT INTO products (content, embedding) VALUES ($1, $2) ON CONFLICT (content) DO NOTHING",
                [(doc.content, doc.embedding) for doc in documents],
            )

    async def semantic_search(
        self, embedding: list[float], top_k: int
    ) -> list[ProductDocument]:
        async with self._db.acquire() as conn:
            records = await conn.fetch(
                "SELECT id, content FROM products ORDER BY embedding <=> $1 LIMIT $2",
                embedding,
                top_k,
            )
            return [ProductDocument(id=r["id"], content=r["content"]) for r in records]
