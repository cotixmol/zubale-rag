from .interfaces import CallbackServiceInterface
import logging
import httpx
from src.config.secrets import secrets

logger = logging.getLogger(__name__)


class WebhookCallbackService(CallbackServiceInterface):
    """Service to send the final answer to a webhook."""

    async def send_response(self, user_id: str, answer: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    secrets.CALLBACK_URL,
                    json={"user_id": user_id, "answer": answer},
                    timeout=10.0,
                )
                response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Failed to send callback for user {user_id}: {e}")
