import asyncpg
from src.models.query import ProductDocument
from .interfaces import ProductRepositoryInterface


class PostgresProductRepository(ProductRepositoryInterface):
    """The actual implementation that talks to our PostgreSQL database."""

    def __init__(self, db):
        self._db = db  # db should be a valid async connection or pool

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
