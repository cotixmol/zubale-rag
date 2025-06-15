from .interfaces import RetrievalServiceInterface
import logging
from sentence_transformers import SentenceTransformer
from src.models.query import ProductDocument
from src.repositories.interfaces.product_repo_interface import (
    ProductRepositoryInterface,
)
from src.config.secrets import secrets

logger = logging.getLogger(__name__)


class ProductRetrievalService(RetrievalServiceInterface):
    """Service to retrieve similar products based on a query using semantic search."""

    def __init__(self, repository: ProductRepositoryInterface):
        self._repository = repository
        self._model = SentenceTransformer(secrets.EMBEDDING_MODEL_NAME)

    async def find_similar_products(self, query: str) -> list[ProductDocument]:
        logger.info(f"Embedding Model for RetrievalService: {self._model}")
        query_embedding = self._model.encode(query).tolist()
        similar_products = await self._repository.semantic_search(
            embedding=query_embedding, top_k=secrets.TOP_K
        )
        return similar_products
