import json
import os

import requests

from aisuite.framework import ChatCompletionResponse
from aisuite.provider import Provider


class AzureProvider(Provider):
    def __init__(self, **config):
        self.base_url = config.get("base_url") or os.getenv("AZURE_BASE_URL")
        self.api_key = config.get("api_key") or os.getenv("AZURE_API_KEY")
        if not self.api_key:
            raise ValueError("For Azure, api_key is required.")
        if not self.base_url:
            raise ValueError(
                "For Azure, base_url is required. Check your deployment page for a URL like this - https://<model-deployment-name>.<region>.models.ai.azure.com"
            )

    def chat_completions_create(self, model, messages, **kwargs):
        url = f"https://{model}.westus3.models.ai.azure.com/v1/chat/completions"
        url = f"https://{self.base_url}/chat/completions"
        if self.base_url:
            url = f"{self.base_url}/chat/completions"

        # Remove 'stream' from kwargs if present
        kwargs.pop("stream", None)
        data = {"messages": messages, **kwargs}

        body = json.dumps(data).encode("utf-8")
        headers = {"Content-Type": "application/json", "Authorization": self.api_key}

        try:
            response = requests.post(url, headers=headers, data=body, timeout=30)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            result = response.content
            resp_json = json.loads(result)
            completion_response = ChatCompletionResponse()
            # TODO: Add checks for fields being present in resp_json.
            completion_response.choices[0].message.content = resp_json["choices"][0]["message"][
                "content"
            ]
            return completion_response

        except requests.exceptions.RequestException as error:
            error_message = f"The request failed: {str(error)}"
            if hasattr(error, "response") and error.response:
                error_message += f"\nStatus code: {error.response.status_code}"
                error_message += f"\nResponse: {error.response.text}"
            raise Exception(error_message)
