import pytest
from unittest.mock import MagicMock, AsyncMock
from src.containers import AppContainer
from src.models.query import ProductDocument


@pytest.mark.asyncio
async def test_query_processor_orchestration():
    """
    Tests that the QueryProcessor correctly calls its dependencies in order.
    """
    container = AppContainer()

    mock_retriever = MagicMock()
    mock_generator = MagicMock()
    mock_callback = AsyncMock()

    mock_retriever.find_similar_products.return_value = [
        ProductDocument(id=1, content="mock product")
    ]
    mock_generator.generate_response.return_value = "This is a mock answer."

    with container.retrieval_service.override(
        mock_retriever
    ), container.generation_service.override(
        mock_generator
    ), container.callback_service.override(
        mock_callback
    ):

        query_usecase = container.query_processor()

        test_user_id = "test_user"
        test_query = "any query"
        await query_usecase.execute(user_id=test_user_id, query=test_query)

    mock_retriever.find_similar_products.assert_called_once_with(test_query)

    mock_generator.generate_response.assert_called_once_with(
        mock_retriever.find_similar_products.return_value,
        test_query,
    )

    mock_callback.send_response.assert_awaited_once_with(
        test_user_id, mock_generator.generate_response.return_value
    )
