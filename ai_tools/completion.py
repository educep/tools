"""
Created by Analitika at 28/11/2024
contact@analitika.fr

    ai.Client()
        Args:
            provider_configs (dict): A dictionary containing provider configurations.
                Each key should be a provider string (e.g., "google" or "aws-bedrock"),
                and the value should be a dictionary of configuration options for that provider.
                For example:
                {
                    "openai": {"api_key": "your_openai_api_key"},
                    "aws": {
                        "aws_access_key": "your_aws_access_key",
                        "aws_secret_key": "your_aws_secret_key",
                        "aws_region": "us-east-1"
                    }
                }

"""
# External imports


# Internal imports
import aisuite as ai
from config import provider_configs

client = ai.Client(provider_configs=provider_configs)


def content_generation(prompt: str, model: str):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content


def testing():
    models = [
        "deepseek:deepseek-chat",
        "openai:gpt-4o-mini",
        "openai:gpt-4o",
        "anthropic:claude-3-5-haiku-latest",
        "anthropic:claude-3-5-sonnet-latest",
        "anthropic:claude-3-opus-latest",
        "aws:amazon.titan-text-lite-v1",
        "aws:amazon.nova-micro-v1:0",
        "aws:amazon.nova-lite-v1:0",
        "aws:amazon.nova-pro-v1:0",
    ]

    messages = [
        {
            "role": "system",
            "content": """You must respond with ONLY valid JSON. No other text.
                          Output must have fields: 'joke', 'story_characters'.""",
        },
        {"role": "user", "content": "Cuéntame un chiste en español"},
    ]

    for model in models:
        model = "deepseek:deepseek-chat"
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, temperature=0.6
            )
            print(model, "\n", response.choices[0].message.content)
        except Exception as e:
            print(f"{model} failed to generate completion: {e}")


if __name__ == "__main__":
    testing()
