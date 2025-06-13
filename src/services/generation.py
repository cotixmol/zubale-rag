from .interfaces import GenerationServiceInterface
import logging
from src.models.query import ProductDocument

logger = logging.getLogger(__name__)


class StubbedGenerationService(GenerationServiceInterface):
    """Concrete implementation of the Generation Service with a stubbed LLM."""

    def _ai_generate(self, prompt: str) -> str:
        """This is our stubbed LLM function as required by the assessment."""
        logger.info("Stubbed LLM function called.")

        return f"This is a generated answer based on the prompt:\n---\n{prompt}\n---"

    def generate_response(self, context_docs: list[ProductDocument], query: str) -> str:
        logger.info(f"Generating response from {len(context_docs)} context documents.")

        if not context_docs:
            return "I'm sorry, I couldn't find any relevant products for your query."

        formatted_context = "\n- ".join([doc.content for doc in context_docs])

        prompt = f"""
        Context from product catalog:
        - {formatted_context}
        
        User's question: {query}
        
        Please answer the user's question based ONLY on the provided context.
        """
        logger.info("Constructed prompt for LLM.")

        generated_answer = self._ai_generate(prompt=prompt)
        logger.info("Generated answer successfully.")

        return generated_answer
