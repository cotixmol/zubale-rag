from abc import abstractmethod, ABC
from typing import Protocol
from src.models.query import ProductDocument


class RetrievalServiceInterface(ABC):
    """Defines the contract for the Retrieval Service (Retriever Agent)."""

    @abstractmethod
    def find_similar_products(self, query: str) -> list[ProductDocument]:
        """Finds and returns a list of products similar to the user query."""
        pass
