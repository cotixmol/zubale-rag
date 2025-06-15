from src.models.query import ProductDocument
from .interfaces import ProductRepositoryInterface
import logging

logger = logging.getLogger(__name__)


class PostgresProductRepository(ProductRepositoryInterface):
    """PostgreSQL implementation of Product Repository."""

    def __init__(self, db):
        self._db = db

    async def index_documents(self, documents: list[ProductDocument]):
        try:
            async with self._db.acquire() as conn:
                await conn.executemany(
                    "INSERT INTO products (content, embedding) VALUES ($1, $2) ON CONFLICT (content) DO NOTHING",
                    [(doc.content, doc.embedding) for doc in documents],
                )
        except Exception as e:
            logger.exception(f"Failed to index documents: {e}")
            raise

    async def semantic_search(
        self, embedding: list[float], top_k: int
    ) -> list[ProductDocument]:
        try:
            async with self._db.acquire() as conn:
                embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
                records = await conn.fetch(
                    "SELECT id, content FROM products ORDER BY embedding <=> $1 LIMIT $2",
                    embedding_str,
                    top_k,
                )
                return [
                    ProductDocument(id=r["id"], content=r["content"]) for r in records
                ]
        except Exception as e:
            logger.exception(f"Failed to perform semantic search: {e}")
            raise
