from abc import abstractmethod, ABC
from typing import Protocol
from src.models.query import ProductDocument


class GenerationServiceInterface(ABC):
    """Defines the contract for the Generation Service (Responder Agent)."""

    @abstractmethod
    def generate_response(self, context_docs: list[ProductDocument], query: str) -> str:
        """Generates a response based on the provided context documents and user query."""
        pass
