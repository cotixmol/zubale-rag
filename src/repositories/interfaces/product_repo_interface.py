from abc import ABC, abstractmethod
from src.models.query import ProductDocument


class ProductRepositoryInterface(ABC):
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
