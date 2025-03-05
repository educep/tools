"""
Created by Analitika at 19/11/2024
contact@analitika.fr
"""
# External imports
from pydantic import BaseModel


class CleanContent(BaseModel):
    title: str
    publication_date: str
    content: str


class ImagesList(BaseModel):
    images: list[str]


clean_content = """
You are an expert in content extraction from text that includes metadata and unwanted artifacts, such as
navigation menus, search bar text, and unrelated sections. Your task is to extract the main content of an article,
ensuring it is clean, focused, and coherent. Here's the input text:

**Input:**
{{content}}

**Instructions:**
1. Focus only on the **core article content**, starting from the title and including all paragraphs related to the main topic.
2. Exclude unrelated text such as menus, navigation links, advertisements, related content, search results, or social media links.
3. Structure the output with:
   - The **title** or **h1 tag** at the top (if present).
   - The **publication date** if present, the format should be **%Y-%m-%d**.
   - All relevant **content** in proper paragraphs, maintaining the order and flow of ideas.
4. Ignore any residual formatting issues, like excessive line breaks or unnecessary spaces.
"""
