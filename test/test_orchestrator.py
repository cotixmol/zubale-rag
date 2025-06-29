import pytest
from unittest.mock import MagicMock, AsyncMock
from src.containers import AppContainer
from src.models.query import ProductDocument
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_orchestrator_full_flow():
    """
    Tests that the LangGraphOrchestrator correctly calls its dependencies in order.
    """
    container = AppContainer()

    mock_retriever = AsyncMock()
    mock_generator = MagicMock()
    mock_callback = AsyncMock()

    mock_retriever.find_similar_products.return_value = [
        ProductDocument(id=1, content="mock product", embeddings=[])
    ]
    mock_generator.generate_response.return_value = "This is a mock answer."

    with container.retrieval_service.override(
        mock_retriever
    ), container.generation_service.override(
        mock_generator
    ), container.callback_service.override(
        mock_callback
    ):
        orchestrator = container.rag_orchestrator()

        test_user_id = "test_user"
        test_query = "any query"

        await orchestrator.process_query(user_id=test_user_id, query=test_query)

    mock_retriever.find_similar_products.assert_awaited_once_with(test_query)
    mock_generator.generate_response.assert_called_once_with(
        mock_retriever.find_similar_products.return_value,
        test_query,
    )
    mock_callback.send_response.assert_awaited_once_with(
        user_id=test_user_id, answer=mock_generator.generate_response.return_value
    )


@pytest.mark.asyncio
async def test_orchestrator_handles_no_retrieved_documents():
    """
    Tests that the orchestrator correctly handles cases where the retrieval
    service finds no documents.
    """
    container = AppContainer()

    mock_retriever = AsyncMock()
    mock_generator = MagicMock()
    mock_callback = AsyncMock()

    mock_retriever.find_similar_products.return_value = []
    mock_generator.generate_response.return_value = (
        "I'm sorry, I couldn't find any relevant products."
    )

    with container.retrieval_service.override(
        mock_retriever
    ), container.generation_service.override(
        mock_generator
    ), container.callback_service.override(
        mock_callback
    ):
        # --- Get and call the new orchestrator ---
        orchestrator = container.rag_orchestrator()
        await orchestrator.process_query(
            user_id="test_user_empty", query="a query for nothing"
        )

    # --- Assertions remain the same ---
    mock_retriever.find_similar_products.assert_awaited_once()
    mock_generator.generate_response.assert_called_once_with([], "a query for nothing")
    mock_callback.send_response.assert_awaited_once_with(
        user_id="test_user_empty",
        answer="I'm sorry, I couldn't find any relevant products.",
    )


# --- Endpoint tests do not need to change ---
# They test the API layer, which remains untouched.


def test_query_endpoint_returns_422_on_missing_query_field():
    response = client.post("/query", json={"user_id": "user123"})
    assert response.status_code == 422


def test_query_endpoint_returns_422_on_missing_user_id():
    response = client.post("/query", json={"query": "some query"})
    assert response.status_code == 422
