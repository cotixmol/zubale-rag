import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.services.interfaces import GenerationServiceInterface
from src.models.query import ProductDocument


class OpenAIGenerationService(GenerationServiceInterface):
    """Service to generate answers using the OpenAI API with LangChain."""

    def __init__(self):
        self.model = ChatOpenAI(model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"))
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert product recommendation assistant. Use the provided product catalog to answer user queries accurately and helpfully.",
                ),
                (
                    "user",
                    [
                        "Product catalog:",
                        "{context}",
                        "\nWhat the user asked for: {query}",
                        "\nProvide an answer based on the Product Catalog and what the user asked for.",
                    ],
                ),
            ]
        )
        output_parser = StrOutputParser()
        self.chain = prompt_template | self.model | output_parser

    def generate_response(self, context_docs: list[ProductDocument], query: str) -> str:
        """
        Generates a response by invoking the LangChain chain.
        """
        if not context_docs:
            return "I'm sorry, I couldn't find any relevant products for your query."

        formatted_context = "\n- ".join([doc.content for doc in context_docs])

        try:
            response = self.chain.invoke({"context": formatted_context, "query": query})
            return response
        except Exception as e:
            print(f"Error calling LangChain chain: {e}")
            return "Sorry, I'm having trouble generating a response right now."
