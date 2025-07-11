import logging
import unittest
from unittest.mock import patch, MagicMock
from polysynergy_nodes.file.upload_from_data import UploadFromData

class TestUploadFromDataNode(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        self.node = UploadFromData()
        self.node.true_path = False
        self.node.false_path = False
        self.node.tenant_id = "tenant-x"
        self.node.project_id = "project-y"
        self.node.file_name = "example.txt"
        self.node.directory = "uploads"
        self.node.is_public = False

    @patch("polysynergy_nodes.file.upload_from_data.S3Service")
    def test_upload_from_base64_success(self, mock_s3_service):
        fake_url = "https://example-bucket/file.txt"
        mock_client = MagicMock()
        mock_client.upload_file.return_value = fake_url
        mock_s3_service.return_value = mock_client

        self.node.file_base64 = "aGVsbG8gd29ybGQ="  # "hello world"
        self.node.file_bytes = None

        self.node.execute()

        self.assertEqual(self.node.url, fake_url)
        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)

    @patch("polysynergy_nodes.file.upload_from_data.S3Service")
    def test_upload_from_bytes_success(self, mock_s3_service):
        fake_url = "https://example-bucket/file.txt"
        mock_client = MagicMock()
        mock_client.upload_file.return_value = fake_url
        mock_s3_service.return_value = mock_client

        self.node.file_base64 = None
        self.node.file_bytes = b"binary data"

        self.node.execute()

        self.assertEqual(self.node.url, fake_url)
        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)

    def test_missing_content(self):
        self.node.file_base64 = None
        self.node.file_bytes = None

        self.node.execute()

        self.assertIn("error", self.node.false_path)
        self.assertFalse(self.node.true_path)

    def test_missing_ids(self):
        self.node.file_base64 = "aGVsbG8gd29ybGQ="
        self.node.tenant_id = None
        self.node.project_id = None

        self.node.execute()

        self.assertIn("error", self.node.false_path)
        self.assertFalse(self.node.true_path)

if __name__ == "__main__":
    unittest.main()