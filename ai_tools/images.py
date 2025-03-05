"""
Created by Analitika at 03/12/2024
contact@analitika.fr
"""
# External imports
from __future__ import annotations
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional, Literal
import io
import base64
from PIL import Image
from datetime import datetime

# Internal imports
from config import OPENAI_API_KEY, AWS_FOLDER, S3_BUCKET_NAME, AWS_REGION
from ai_prompts import ImagePrompt, PromptManager
from ai_tools.aws_bedrock import BedrockClient
from aws import S3Manager

bucket = S3Manager()


# Custom field type for PIL Images
class PILImageField:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):  # Added field parameter
        try:
            # Handle Streamlit's UploadedFile
            if hasattr(v, "getvalue"):  # Streamlit's UploadedFile has getvalue method
                image_bytes = v.getvalue()
                return Image.open(io.BytesIO(image_bytes))
            # Keep existing validation logic
            elif isinstance(v, Image.Image):
                return v
            elif isinstance(v, bytes):
                return Image.open(io.BytesIO(v))
            elif isinstance(v, io.BytesIO):
                return Image.open(v)
            elif v is None:
                return None
            raise ValueError("Invalid image type")
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")


class ImageData(BaseModel):
    prompt: str
    caption: str
    alt_text: str
    url: Optional[str] = None
    image: Optional[PILImageField] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            Image.Image: lambda img: base64.b64encode(
                (
                    lambda: (
                        buffer := io.BytesIO(),
                        img.save(buffer, format=getattr(img, "format", "PNG")),
                        buffer.getvalue(),
                    )[2]
                )()
            ).decode("utf-8")
            if img
            else None
        }

    def dict(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        if d.get("image") and isinstance(d["image"], Image.Image):
            buffer = io.BytesIO()
            image_format = getattr(d["image"], "format", "PNG")
            d["image"].save(buffer, format=image_format)
            d["image"] = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return d

    @classmethod
    def from_streamlit_upload(
        cls, uploaded_file, prompt: str, caption: str, alt_text: str
    ):
        """
        Create ImageData instance from Streamlit's uploaded file
        """
        if not uploaded_file:
            raise ValueError("No file uploaded")

        # Validate file type
        file_type = uploaded_file.type
        if not file_type.startswith("image/"):
            raise ValueError(f"Invalid file type: {file_type}. Must be an image.")

        return cls(
            prompt=prompt,
            caption=caption,
            alt_text=alt_text,
            image=uploaded_file,  # PILImageField will handle conversion
        )


class ImageGeneration:
    img_model: str
    resolutions: Literal["1024x1024", "1792x1024", "1024x1792"] = "1024x1024"
    response_format: Literal["b64_json", "url"] = "b64_json"
    height: int = (1024,)
    width: int = (1024,)

    def __init__(
        self,
        selected_image_model: str,
        resolutions: Literal["1024x1024", "1792x1024", "1024x1792"] = "1024x1024",
    ):
        provider, img_model = selected_image_model.split(":", maxsplit=1)
        if provider not in ["openai", "aws"]:
            raise ValueError("Invalid provider. Must be 'openai' or 'aws'.")
        self.provider = provider
        self.img_model = img_model
        if resolutions not in ["1024x1024", "1792x1024", "1024x1792"]:
            raise ValueError(
                "Invalid resolution. Must be 1024x1024, 1792x1024, or 1024x1792."
            )

        self.resolutions = resolutions
        height, width = resolutions.split("x")
        self.height = int(height)
        self.width = int(width)

    def openai_generate_image(
        self,
        image_prompt: ImagePrompt,
        response_format: Literal["b64_json", "url"] = "b64_json",
    ) -> str | io.BytesIO:
        """
        Generate an image using OpenAI's API or AWS Nova, source :
        https://cookbook.openai.com/articles/what_is_new_with_dalle_3
        :param image_prompt: data for the image generation
        :param response_format: format type of the response
        :return: ImageData
        """
        # strict is the first sentence taken from openai model documentation to avoid prompt rewriting
        strict = """I NEED to test how the tool works with extremely simple prompts.
                    DO NOT add any detail, just use it AS-IS:\n"""
        prompt = strict + image_prompt.prompt
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.images.generate(
            model=self.img_model,
            prompt=prompt,
            size=self.resolutions,  # 1024x1024, 1792x1024, or 1024x1792 for dall-e-3 models.
            quality="standard",
            style="vivid",  # vivid or natural
            user="educep",
            response_format=response_format,  # url or b64_json
            n=1,
        )
        if response_format == "url":
            return response.data[0].url
        else:
            # Convert bytes to image
            image_bytes = base64.b64decode(response.data[0].b64_json)
            image = io.BytesIO(image_bytes)
            # image = Image.open(io.BytesIO(image_bytes))

        return image

    def generate_image_prompt(
        self, prompt: str, user_model: str = "gpt-4o-mini"
    ) -> ImagePrompt:
        """
        Generate an image prompt using **OpenAI**'s API
        :param prompt: prompt to be used for the image generation
        :param user_model: model to be used for the image generation
        :return: ImagePrompt
        """
        if user_model not in ["gpt-4o-mini", "gpt-4o"]:
            raise NotImplementedError("Only available for OpenAI's models")

        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.beta.chat.completions.parse(
            model=user_model,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            response_format=ImagePrompt,
        )
        return completion.choices[0].message.parsed

    def generate_image(
        self,
        content: str,
    ) -> ImageData:
        """
        Generate an image using OpenAI's API or AWS Nova, source :
        https://cookbook.openai.com/articles/what_is_new_with_dalle_3
        :param content: content to be used for the image prompt generation
        :param selected_image_model: model to be used for the image generation
        :param response_format: format type of the response
        :return: ImageData
        """
        pm = PromptManager()
        image_generation = pm.get_prompt("image_generation")["prompt"]
        prompt = image_generation.replace("{{content}}", content)
        # strict is the first sentence taken from openai model documentation to avoid prompt rewriting
        image_prompt = self.generate_image_prompt(prompt)
        print(image_prompt)

        if self.provider == "openai":
            image = self.openai_generate_image(image_prompt, self.response_format)
        elif self.provider == "aws":
            completion = BedrockClient()
            config = BedrockClient.configure_text_to_image_params(
                text=image_prompt.prompt,
                width=self.width,
                height=self.height,
            )
            image = completion.generate_image(
                model_id=self.img_model, body=json.dumps(config)
            )
        else:
            raise NotImplementedError("Only available for OpenAI and AWS models")

        # Save the image to a local file
        # image.save(f"output_image_{self.provider}.jpg")

        image_data = ImageData(
            prompt=image_prompt.prompt,
            caption=image_prompt.caption,
            alt_text=image_prompt.alt_text,
            # url=response.data[0].url,
            # image_bytes=response.data[0].b64_json,
        )

        # We now store everything, we store errors in DB
        file_name_s3 = (
            self.provider
            + "_generated_image_"
            + datetime.now().strftime("%Y%m%d%H%M%S")
            + ".png"
        )
        folder = f"{AWS_FOLDER}/images"
        bucket.upload_to_s3(file_name_s3, image, folder, content_type=f"image/png")

        if self.response_format == "url":
            image_data.url = image
        elif self.response_format == "b64_json":
            url_aws = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{folder}/{file_name_s3}"
            image_data.image = image
            image_data.url = url_aws

        return image_data


def test_generate_image():
    """
    Test the generate_image function
    :return: None
    """
    content = "A cute baby sea otter wearing a beret"
    # genimage = ImageGeneration(selected_image_model="openai:dall-e-3")
    # image_data = genimage.generate_image(content)

    genimage = ImageGeneration(selected_image_model="aws:amazon.nova-canvas-v1:0")
    image_data = genimage.generate_image(content)

    from wordpress_api import Post, Media, Category, Tag
    from config import WP_URL, WP_USERNAME, WP_ACCESSKEY
    from wordpress_api import WordPressAPI

    api = WordPressAPI(WP_URL, WP_USERNAME, WP_ACCESSKEY)
    media_data = Media(
        title="title",
        alt_text="alt_text",
        caption="caption",
        description="title",
        status="publish",
        meta={},
    )
    new_media = api.create_media(image_data.image, media=media_data)


if __name__ == "__main__":
    test_generate_image()
