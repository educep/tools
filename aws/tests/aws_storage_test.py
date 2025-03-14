"""
Created by Analitika at 19/08/2024
contact@analitika.fr
"""


# External imports
import json
import unittest
from unittest.mock import MagicMock, patch

from aws import S3Manager

# Internal imports
from config import settings

"""
This is a test class for the S3Manager class. It tests the upload, download, and delete operations
on S3 using mocked responses from the S3Manager class.
"""


class TestS3Manager(unittest.TestCase):
    # Declare class attributes with type annotations
    s3_manager: S3Manager
    test_dict: dict
    file_name: str
    prefix: str

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test case environment. Load environment variables and initialize the S3Manager.
        """
        cls.s3_manager = S3Manager()
        cls.test_dict = {"test": "test"}
        cls.file_name = "test.json"
        cls.prefix = f"{settings.AWS_FOLDER}/00aa_test"

    @patch.object(S3Manager, "upload_json_file")
    @patch.object(S3Manager, "download_from_s3")
    @patch.object(S3Manager, "delete_object_from_s3")
    def test_s3_operations(
        self,
        mock_delete: MagicMock,
        mock_download: MagicMock,
        mock_upload: MagicMock,
    ) -> None:
        """
        Test the upload, download, and delete operations on S3.
        python -m unittest .\test\test_aws_storage.py
        """
        # Mocking the S3 responses
        mock_upload.return_value = 0
        mock_download.side_effect = [
            json.dumps(self.test_dict),  # Return the data after the first download
            None,  # Return None after the deletion
        ]
        mock_delete.return_value = 0

        # Test upload
        exit_code_1 = self.s3_manager.upload_json_file(self.file_name, self.test_dict, self.prefix)
        self.assertEqual(exit_code_1, 0)
        mock_upload.assert_called_once_with(self.file_name, self.test_dict, self.prefix)

        # Test download
        content_1 = self.s3_manager.download_from_s3(self.file_name, self.prefix)
        self.assertEqual(content_1, json.dumps(self.test_dict))
        mock_download.assert_called_with(self.file_name, self.prefix)

        # Test delete
        exit_code_2 = self.s3_manager.delete_object_from_s3(self.file_name, self.prefix)
        self.assertEqual(exit_code_2, 0)
        mock_delete.assert_called_once_with(self.file_name, self.prefix)

        # Test download after deletion
        content_2 = self.s3_manager.download_from_s3(self.file_name, self.prefix)
        self.assertIsNone(content_2)
        self.assertEqual(mock_download.call_count, 2)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up the test environment. Delete the test folder in S3.
        """
        with patch.object(S3Manager, "rename_s3_folder") as mock_rename:
            cls.s3_manager.rename_s3_folder(cls.prefix, f"{cls.prefix}_deleted")
            mock_rename.assert_called_once_with(cls.prefix, f"{cls.prefix}_deleted")


if __name__ == "__main__":
    unittest.main()
