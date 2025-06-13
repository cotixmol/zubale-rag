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
    """Concrete implementation of the Retrieval Service."""

    def __init__(self, repository: ProductRepositoryInterface):
        self._repository = repository
        logger.info(
            f"Loading embedding model for RetrievalService: {secrets.EMBEDDING_MODEL_NAME}"
        )
        self._model = SentenceTransformer(secrets.EMBEDDING_MODEL_NAME)

    def find_similar_products(self, query: str) -> list[ProductDocument]:
        logger.info(f"Creating embedding for query: '{query}'")
        query_embedding = self._model.encode(query).tolist()

        logger.info(f"Finding top {secrets.TOP_K} similar products in repository...")
        similar_products = self._repository.semantic_search(
            embedding=query_embedding, top_k=secrets.TOP_K
        )
        logger.info(f"Found {len(similar_products)} similar products.")
        return similar_products
