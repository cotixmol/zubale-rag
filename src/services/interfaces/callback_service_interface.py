from abc import ABC, abstractmethod
from typing import Protocol


class CallbackServiceInterface(ABC):
    """Defines the contract for the Callback Service."""

    @abstractmethod
    async def send_response(self, user_id: str, answer: str) -> None:
        """Sends a response to the user."""
        pass
