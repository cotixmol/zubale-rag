from .interfaces import CallbackServiceInterface
import logging
import httpx
from src.config.secrets import secrets

logger = logging.getLogger(__name__)


class WebhookCallbackService(CallbackServiceInterface):
    """Service to send the final answer to a webhook."""

    async def send_response(self, user_id: str, answer: str):
        payload = {"user_id": user_id, "answer": answer}

        logger.info(
            f"Sending response for user {user_id} to callback URL: {secrets.CALLBACK_URL}"
        )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    secrets.CALLBACK_URL, json=payload, timeout=10.0
                )
                response.raise_for_status()
            logger.info(
                f"Successfully sent callback for user {user_id}. Status: {response.status_code}"
            )
        except httpx.RequestError as e:
            logger.error(f"Failed to send callback for user {user_id}: {e}")
