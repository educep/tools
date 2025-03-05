""""
Created by Analitika at 27/03/2024
contact@analitika.fr
"""
# External imports
import os
import gzip
import json
from io import BytesIO
from typing import Union, List
import pickle
import boto3  # AWS SDK for Python
import pandas as pd
from botocore.exceptions import ClientError
from loguru import logger
from PIL import Image

# Internal imports
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME,
)


class S3Manager:
    def __init__(self):
        """
        Initialize the S3Manager with AWS credentials.
        """
        self.s3_client = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        ).client("s3")

    def upload_json_file(self, file_name: str, data: dict, folder: str) -> int:
        """
        Upload a JSON file to an AWS S3 bucket.
        :param file_name: The name of the file to be saved in S3 (without extension)
        :param data: The data to be serialized and uploaded
        :param folder: The folder within the S3 bucket where the file will be stored
        :return: int status code (0 for success, 1 for failure)
        """
        try:
            json_data = json.dumps(data, indent=4)
            s3_file_key = f"{folder}/{file_name}"
            self.s3_client.put_object(
                Bucket=S3_BUCKET_NAME, Key=s3_file_key, Body=json_data
            )
            return 0
        except ClientError as e:
            logger.error(str(e))
            return 1

    def get_available_files(self, folder: str) -> List[str]:
        """
        List all files in a specific folder within an AWS S3 bucket.
        :param folder: The folder within the S3 bucket
        :return: List of file names
        """
        files = []
        try:
            is_truncated = True  # Pagination flag
            continuation_token = None  # Continuation token for pagination

            while is_truncated:
                list_kwargs = {
                    "Bucket": S3_BUCKET_NAME,
                    "MaxKeys": 1000,  # Set to 1000 (AWS limit per request)
                }
                if continuation_token:
                    list_kwargs["ContinuationToken"] = continuation_token

                response = self.s3_client.list_objects_v2(
                    Bucket=S3_BUCKET_NAME, Prefix=folder
                )

                if "Contents" in response:
                    for file in response["Contents"]:
                        filename = file["Key"][len(folder) + 1 :]
                        if filename:
                            files.append(filename)

                # Check if more files are available
                is_truncated = response.get("IsTruncated", False)

                # Update continuation token if more files are available
                continuation_token = response.get("NextContinuationToken", None)

        except ClientError as e:
            logger.error(str(e))
        return files

    def upload_to_s3(
        self,
        file_name: str,
        data: bytes,
        folder: str,
        content_type: str = "application/octet-stream",
    ) -> int:
        """
        Upload a file to an AWS S3 bucket.
        :param file_name: The name of the file to be saved in S3 (without extension)
        :param data: The data to be uploaded
        :param folder: The folder within the S3 bucket where the file will be stored
        :param content_type: The content type of the file
        :return: int status code (0 for success, 1 for failure)
        """
        try:
            s3_file_key = f"{folder}/{file_name}"
            self.s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_file_key,
                Body=data,
                ContentType=content_type,
            )
            return 0
        except ClientError as e:
            logger.error(str(e))
            return 1

    def delete_object_from_s3(self, file_name: str, folder: str) -> int:
        """
        Delete an object from an AWS S3 bucket.
        :param file_name: The name of the file to be deleted from S3
        :param folder: The folder within the S3 bucket where the file is stored
        :return: int status code (0 for success, 1 for failure)
        """
        try:
            s3_file_key = f"{folder}/{file_name}"
            self.s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_file_key)
            logger.info(f"Object {s3_file_key} deleted from S3.")
            return 0
        except ClientError as e:
            logger.error(str(e))
            return 1

    def check_file_exists(self, key: str) -> bool:
        """
        Check if a file exists in an S3 bucket.
        :param key: The full key of the file in the S3 bucket
        :return: True if the file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def download_from_s3(
        self, file_name: str, folder: str
    ) -> Union[bytes, str, None, pd.DataFrame, Image.Image]:
        """
        Download a file from an AWS S3 bucket, with optional decompression for gzip files.
        :param file_name: The name of the file to be downloaded from S3 (with extension)
        :param folder: The folder within the S3 bucket where the file is stored (can be composed folder/subfolder)
        :return: The file content, decompressed if it's a gzip file, or None on failure
        """
        s3_file_key = f"{folder}/{file_name}"
        if not self.check_file_exists(s3_file_key):
            logger.error(
                f"File '{s3_file_key}' does not exist in bucket '{S3_BUCKET_NAME}'."
            )
            return None

        file_stream = BytesIO()
        try:
            self.s3_client.download_fileobj(
                Bucket=S3_BUCKET_NAME, Key=s3_file_key, Fileobj=file_stream
            )
            file_stream.seek(0)
            # Handle gzip files
            if file_name.endswith(".gz"):
                with gzip.open(file_stream, "rb") as f_in:
                    return f_in.read().decode("utf-8")

            # Handle pickle files
            if file_name.endswith(".pkl"):
                return pickle.load(file_stream)

            # Handle image files
            image_extensions = (
                ".png",
                ".jpg",
                ".jpeg",
                ".bmp",
                ".gif",
                ".tiff",
                ".webp",
            )
            if file_name.lower().endswith(image_extensions):
                return Image.open(file_stream)

            # Default: return content as a string
            return file_stream.read().decode("utf-8")
        except ClientError as e:
            logger.critical(str(e))
            return None

    def rename_s3_folder(self, old_folder: str, new_folder: str) -> None:
        """
        Rename a folder in S3 by copying all objects from the old folder to the new folder
        and then deleting the old objects.
        :param old_folder: The name of the existing folder in S3
        :param new_folder: The new folder name to move the objects to
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=S3_BUCKET_NAME, Prefix=old_folder
            )
            if "Contents" not in response:
                logger.info(f"No objects found in the folder: {old_folder}")
                return

            for obj in response["Contents"]:
                old_key = obj["Key"]
                new_key = old_key.replace(old_folder, new_folder, 1)
                self.s3_client.copy_object(
                    Bucket=S3_BUCKET_NAME,
                    CopySource={"Bucket": S3_BUCKET_NAME, "Key": old_key},
                    Key=new_key,
                )
                self.s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=old_key)
                logger.info(f"Moved {old_key} to {new_key}")
            logger.info(f"Folder renamed from {old_folder} to {new_folder}")
        except ClientError as e:
            logger.info(f"Error renaming folder: {str(e)}")

    def save_to_local_disk(self, content, file_name: str, folder_path: str):
        """
        Save the downloaded content to the local disk, handling different file types properly.

        :param content: The content of the file, which could be text, bytes, or an image.
        :param file_name: The name of the file (including extension).
        :param folder_path: The local folder where the file should be saved.
        """
        os.makedirs(folder_path, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(folder_path, file_name)

        # Handle image files
        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp")
        if isinstance(content, Image.Image):
            content.save(file_path)
            return file_path

        # Handle binary files (e.g., gzip, pickle, or any other non-text files)
        if isinstance(content, bytes):
            with open(file_path, "wb") as f:
                f.write(content)
            return file_path

        # Handle text files
        if isinstance(content, str):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return file_path

        # If content is None, return None
        return None

    def download_folder(self, folder_path: str, aws_path: str):
        files = self.get_available_files(aws_path)
        for file_ in files:
            content = self.download_from_s3(file_, aws_path)
            self.save_to_local_disk(content, file_, folder_path)
        return


if __name__ == "__main__":
    s3_bucket = S3Manager()
    aws_folder = "folder"
    test_dict = {"test": "test"}
    prefix = f"{aws_folder}/00aa_test"
    exit_code_1 = s3_bucket.upload_json_file("test.json", test_dict, prefix)
    content_1 = s3_bucket.download_from_s3("test.json", prefix)
    exit_code_2 = s3_bucket.delete_object_from_s3("test.json", prefix)
    content_2 = s3_bucket.download_from_s3("test.json", prefix)
    assert content_2 is None
