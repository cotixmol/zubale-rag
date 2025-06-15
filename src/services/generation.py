from .interfaces import GenerationServiceInterface
import logging
from src.models.query import ProductDocument

logger = logging.getLogger(__name__)


class StubbedGenerationService(GenerationServiceInterface):
    """Service to generate answers based on product documents and user queries."""

    def _ai_generate(self, prompt: str) -> str:
        ##TODO: Replace this stubbed method with actual LLM generation logic.
        ai_stubbed_generation = f"""
        LLM stubbed generated answer based on the prompt: 
        {prompt}
        """
        return ai_stubbed_generation

    def generate_response(self, context_docs: list[ProductDocument], query: str) -> str:
        if not context_docs:
            return "I'm sorry, I couldn't find any relevant products for your query."

        formatted_context_docs = "\n- ".join([doc.content for doc in context_docs])

        prompt = f"""
        Product catalog:
        - {formatted_context_docs}
        
        What the user asked for: {query}
        
        Provide an answer based on the Product Catalog and the what the user asked for.
        """

        generated_answer = self._ai_generate(prompt=prompt)

        return generated_answer
