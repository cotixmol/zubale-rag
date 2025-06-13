import logging
from src.services.interfaces import (
    RetrievalServiceInterface,
    GenerationServiceInterface,
    CallbackServiceInterface,
)

logger = logging.getLogger(__name__)


class QueryProcessor:
    """The main use case orchestrator."""

    def __init__(
        self,
        retrieval_service: RetrievalServiceInterface,
        generation_service: GenerationServiceInterface,
        callback_service: CallbackServiceInterface,
    ):
        self._retrieval_service = retrieval_service
        self._generation_service = generation_service
        self._callback_service = callback_service
        logger.info("QueryProcessor use case initialized.")

    async def execute(self, user_id: str, query: str):
        """Executes the full RAG pipeline for a given query."""
        logger.info(f"Executing use case for user_id: {user_id}, query: '{query}'")

        context_docs = self._retrieval_service.find_similar_products(query)

        answer = self._generation_service.generate_response(context_docs, query)

        await self._callback_service.send_response(user_id, answer)

        logger.info(f"Use case execution finished for user {user_id}.")
