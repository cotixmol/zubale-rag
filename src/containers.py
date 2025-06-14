from dependency_injector import containers, providers
from src.config.secrets import secrets
from src.repositories import PostgresProductRepository
from src.services import (
    ProductRetrievalService,
    StubbedGenerationService,
    WebhookCallbackService,
)
from src.usecases import QueryProcessor


class AppContainer(containers.DeclarativeContainer):
    """
    The main Dependency Injection container for the application.
    """

    config = providers.Configuration()
    config.from_pydantic(secrets)

    product_repo = providers.Singleton(PostgresProductRepository, db=None)

    retrieval_service = providers.Factory(
        ProductRetrievalService, repository=product_repo
    )

    generation_service = providers.Factory(StubbedGenerationService)

    callback_service = providers.Factory(WebhookCallbackService)

    query_processor = providers.Factory(
        QueryProcessor,
        retrieval_service=retrieval_service,
        generation_service=generation_service,
        callback_service=callback_service,
    )
