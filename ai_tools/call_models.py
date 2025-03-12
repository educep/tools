"""
Created by Analitika at 27/03/2024
contact@analitika.fr
"""
from typing import Type

# External imports
from openai import OpenAI
from pydantic import BaseModel

# Internal imports
from config.settings import COMPLETIONS_MODEL, EMBEDDINGS_MODEL, OPENAI_API_KEY

# Configure logging
client = OpenAI(api_key=OPENAI_API_KEY)


def get_embeddings(
    text: list,
    model: str = EMBEDDINGS_MODEL,
    dimension: int = 1536,
) -> list:
    """
    text = ["this is a text", "this is divided into parts"]
    model = EMBEDDINGS_MODEL
    dimension = 1536 dimension of the small model
    """

    if not model:
        raise KeyError("model not provided")
    response = client.embeddings.create(input=text, model=model, dimensions=dimension)
    return [data.embedding for data in response.data]


def generate_answer(prompt: str, user_model: Type[BaseModel]):
    """
    ai_client: is the client to use: in this project we can use 2: Haskn to treat their Content Library,
                ANK for the rest
    prompt: is the prompt to send to the model
    temperature=0,  # Controls the randomness in the output generation. The hotter, the more random.
                      A temperature of 1 is a standard setting for creative or varied outputs.
    max_tokens=500, # The maximum length of the model's response.
    top_p=1,        # (or nucleus sampling) this parameter controls the cumulative probability distribution
                      of token selection. A value of 1 means no truncation, allowing all tokens to be considered
                      for selection based on their probability.
    frequency_penalty=0,  # Adjusts the likelihood of the model repeating the same line verbatim.
                            Setting this to 0 means there's no penalty for frequency, allowing the model to freely
                            repeat information as needed.
    presence_penalty=0,  # Alters the likelihood of introducing new concepts into the text.
                           A penalty of 0 implies no adjustment, meaning the model is neutral about introducing
                           new topics or concepts.
    from ai_prompts import CleanContent
    aa =  generate_answer("say hello", CleanContent)
    """

    try:
        completion = client.beta.chat.completions.parse(
            model=COMPLETIONS_MODEL,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            response_format=user_model,
        )

        # Attempt to parse the response
        # response_ = response.model_dump()
        # return response_["choices"][0]["message"]["content"]
        return completion.choices[0].message.parsed
    except KeyError as e:
        # Handle any issues with missing keys in the response
        print(f"KeyError: {e} - The expected key is not in the response.")
        return "An error occurred: the response structure was not as expected."

    except Exception as e:
        # Handle any other general exceptions (e.g., network errors, API issues)
        print(f"An error occurred: {e}")
        return "An error occurred while generating the response."
