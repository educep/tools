import os

import openai

from aisuite.provider import Provider  # LLMError


class DeepseekProvider(Provider):
    def __init__(self, **config: dict) -> None:
        """
        Initialize the OpenAI provider with the given configuration.
        Pass the entire configuration dictionary to the OpenAI client constructor.
        """
        # Ensure API key is provided either in config or via environment variable
        config.setdefault("api_key", os.getenv("DEEPSEEK_API_KEY"))
        if not config["api_key"]:
            raise ValueError(
                "DeepSeek API key is missing. Please provide it in the config or set the DEEPSEEK_API_KEY environment variable."
            )

        # Pass the entire config to the OpenAI client constructor
        self.client = openai.OpenAI(**config)

    def chat_completions_create(self, model: str, messages: list[str], **kwargs):
        # Any exception raised by OpenAI will be returned to the caller.
        # Maybe we should catch them and raise a custom LLMError.
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,  # Pass any additional arguments to the OpenAI API
        )
