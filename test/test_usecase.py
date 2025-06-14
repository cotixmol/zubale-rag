import pytest
from unittest.mock import MagicMock, AsyncMock
from src.containers import AppContainer
from src.usecases.process_query import QueryProcessor
from src.models.query import ProductDocument

# Mark the test as an asyncio test
@pytest.mark.asyncio
async def test_query_processor_orchestration():
    """
    Tests that the QueryProcessor correctly calls its dependencies in order.
    """
    # 1. Create an instance of our DI container for the test
    container = AppContainer()

    # 2. Create mock services that we can control
    mock_retriever = MagicMock()
    mock_generator = MagicMock()
    # The callback is an async function, so we use AsyncMock
    mock_callback = AsyncMock()

    # 3. Define the return values for our mocks
    mock_retriever.find_similar_products.return_value = [
        ProductDocument(id=1, content="mock product")
    ]
    mock_generator.generate_response.return_value = "This is a mock answer."

    # 4. Use the container's override feature. The 'with' block ensures
    #    the override is only active for the duration of this test.
    with container.retrieval_service.override(mock_retriever), \
         container.generation_service.override(mock_generator), \
         container.callback_service.override(mock_callback):
        
        # 5. Get the use case from the container. The container will
        #    automatically inject our MOCK services instead of the real ones.
        query_usecase = container.query_processor()
        
        # 6. Execute the use case
        test_user_id = "test_user"
        test_query = "any query"
        await query_usecase.execute(user_id=test_user_id, query=test_query)

    # 7. Assert that our mocks were called correctly, proving the
    #    orchestration logic works.
    mock_retriever.find_similar_products.assert_called_once_with(test_query)
    
    mock_generator.generate_response.assert_called_once_with(
        mock_retriever.find_similar_products.return_value, # context
        test_query # query
    )
    
    mock_callback.send_response.assert_awaited_once_with(
        test_user_id, # user_id
        mock_generator.generate_response.return_value # answer
    )