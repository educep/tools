"""
Created by Analitika at 16/12/2024
contact@analitika.fr
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
from zoneinfo import ZoneInfo

from aws import S3Manager

# Internal imports
from config.settings import AWS_FOLDER


class PromptManager:
    date_format: str = "%Y%m%d%H%M"
    subfolder: str = "prompts"

    def __init__(self) -> None:
        self.bucket = S3Manager()
        self.folder = f"{AWS_FOLDER}/{self.subfolder}"

    def parse_prompt_path(self, path: str) -> Tuple[str, str, str]:
        """Parse S3 path to extract category and name"""
        parts = path.split("/")
        category = parts[-2]
        timestamp_name = parts[-1].replace(".json", "")
        timestamp = timestamp_name[:12]  # Extract YYYYMMDDHHMM
        name = timestamp_name[13:]  # Extract name after timestamp
        return category, timestamp, name

    def get_prompts(self) -> List[Dict]:
        """
        Get all prompts from S3 bucket, keeping only the most recent version
        of each prompt (based on category and name combination)
        """
        prompts = self.bucket.get_available_files(self.folder)
        if not prompts:
            return []

        # Dictionary to store the latest version of each prompt
        # Key: (category, name), Value: prompt data
        latest_prompts = {}

        for prompt in prompts:
            if prompt.endswith(".json"):
                category, timestamp, name = self.parse_prompt_path(prompt)
                current_timestamp = datetime.strptime(timestamp, self.date_format)

                prompt_key = (category, name)
                prompt_data = {
                    "category": category,
                    "timestamp": current_timestamp,
                    "name": name,
                    "path": prompt,
                }

                # If this category/name combination hasn't been seen before, add it
                if prompt_key not in latest_prompts:
                    data = self.bucket.download_from_s3(prompt, self.folder)
                    prompt_data.update(json.loads(data))
                    latest_prompts[prompt_key] = prompt_data
                # If we've seen this combination before, keep the newer version
                else:
                    existing_timestamp = latest_prompts[prompt_key]["timestamp"]
                    if current_timestamp > existing_timestamp:
                        data = self.bucket.download_from_s3(prompt, self.folder)
                        prompt_data.update(json.loads(data))
                        latest_prompts[prompt_key] = prompt_data

        # Convert dictionary values back to a list
        return list(latest_prompts.values())

    def extract_variables(self, prompt: str) -> List[Tuple[str, str]]:
        """Extract variables from prompt text using regex"""
        pattern = r"\{\{(\w+)\}\}"
        matches = re.findall(pattern, prompt)
        # Remove duplicates while preserving order
        matches = list(dict.fromkeys(matches))
        return matches

    def save_prompt(self, category: str, name: str, prompt: str, description: str) -> str:
        """Save prompt to S3"""
        timestamp = datetime.now(ZoneInfo("Europe/Paris")).strftime(self.date_format)
        filename = f"{timestamp}_{name}.json"
        path = f"{self.folder}/{category}"

        data = {
            "prompt": prompt.strip(),
            "description": description.strip(),
            "variables": self.extract_variables(prompt),
        }

        json_bytes = json.dumps(data).encode("utf-8")
        self.bucket.upload_to_s3(filename, json_bytes, path, content_type="application/json")

        return path

    def get_prompt(self, name: str) -> Dict | None:
        """Get prompt from S3"""
        prompts = self.get_prompts()
        for prompt in prompts:
            if prompt["name"] == name:
                return prompt
        return None


def set_prompt(prompt_: str, description: str, variables: List[str]):
    return {
        "prompt": prompt_.strip(),
        "description": description,
        "variables": variables,
    }


def generate_json():
    from ai_prompts.extraction import clean_content
    from ai_prompts.generation import html_builder
    from aws import S3Manager

    # here we initialize aws folder
    bucket = S3Manager()
    now_str = datetime.now().strftime("%Y%m%d%H%M")

    filename = f"{now_str}_clean_content.json"
    path = f"{AWS_FOLDER}/prompts/extraction"
    prompt_ = set_prompt(
        clean_content,
        "Extract the content of the article from a html (scrapped url)",
        ["content"],
    )
    json_bytes = json.dumps(prompt_).encode("utf-8")
    bucket.upload_to_s3(filename, json_bytes, path, content_type="application/json")

    filename = f"{now_str}_html_builder.json"
    path = f"{AWS_FOLDER}/prompts/generation"
    prompt_ = set_prompt(
        html_builder,
        "Analyze text and format it into proper **HTML** for direct upload to **WordPress**",
        ["content"],
    )
    json_bytes = json.dumps(prompt_).encode("utf-8")
    bucket.upload_to_s3(filename, json_bytes, path, content_type="application/json")


if __name__ == "__main__":
    # create_prompt_ui()
    prompt_manager = PromptManager()
    prompts = prompt_manager.get_prompts()
