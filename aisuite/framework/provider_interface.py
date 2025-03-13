"""The shared interface for model providers."""

from typing import List, Optional


class ProviderInterface:
    """Defines the expected behavior for provider-specific interfaces."""

    def chat_completion_create(
        self,
        messages: Optional[List[str]] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
    ) -> None:
        """Create a chat completion using the specified messages, model, and temperature.

        This method must be implemented by subclasses to perform completions.

        Args:
        ----
            messages (list): The chat history.
            model (str): The identifier of the model to be used in the completion.
            temperature (float): The temperature to use in the completion.

        Raises:
        ------
            NotImplementedError: If this method has not been implemented by a subclass.

        """
        raise NotImplementedError(
            "Provider Interface has not implemented chat_completion_create()"
        )
