from aisuite.framework.chat_completion_response import ChatCompletionResponse
from aisuite.provider import Provider


class GcpProvider(Provider):
    def __init__(self) -> None:
        pass

    def chat_completions_create(self, model: str, messages: list[dict]) -> ChatCompletionResponse:
        raise ValueError("GCP Provider not yet implemented.")
