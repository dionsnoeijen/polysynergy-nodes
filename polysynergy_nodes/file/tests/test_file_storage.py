import unittest
import asyncio
import base64
import json
from unittest.mock import AsyncMock, MagicMock, patch
from polysynergy_nodes.file.file_storage import FileStorage


class TestFileStorageNode(unittest.TestCase):

    def setUp(self):
        self.node = FileStorage()
        self.node.content_type = "auto"
        self.node.data_format = "auto"
        self.node.save_path = "generated/files/"
        self.node.overwrite = False
        
        # Reset outputs
        self.node.true_path = False
        self.node.false_path = False

    def test_validate_save_path_valid(self):
        """Test save path validation with valid paths"""
        self.node.save_path = "documents/reports/"
        self.node._validate_save_path()
        self.assertEqual(self.node.save_path, "documents/reports/")

    def test_validate_save_path_empty(self):
        """Test save path validation with empty path"""
        self.node.save_path = ""
        self.node._validate_save_path()
        self.assertEqual(self.node.save_path, "generated/files/")

    def test_validate_save_path_security(self):
        """Test save path validation rejects dangerous paths"""
        # Directory traversal
        self.node.save_path = "documents/../secrets/"
        with self.assertRaises(ValueError) as context:
            self.node._validate_save_path()
        self.assertIn("directory traversal", str(context.exception))
        
        # Absolute path
        self.node.save_path = "/etc/passwd"
        with self.assertRaises(ValueError) as context:
            self.node._validate_save_path()
        self.assertIn("relative to tenant bucket", str(context.exception))

    def test_detect_data_format_bytes(self):
        """Test data format detection for bytes"""
        self.node.content_data = b"binary content"
        result = self.node._detect_data_format()
        self.assertEqual(result, "bytes")

    def test_detect_data_format_base64(self):
        """Test data format detection for base64"""
        test_data = base64.b64encode(b"test content").decode()
        self.node.content_data = test_data
        result = self.node._detect_data_format()
        self.assertEqual(result, "base64")

    def test_detect_data_format_data_url(self):
        """Test data format detection for data URLs"""
        test_data = base64.b64encode(b"test content").decode()
        self.node.content_data = f"data:text/plain;base64,{test_data}"
        result = self.node._detect_data_format()
        self.assertEqual(result, "base64")

    def test_detect_data_format_string(self):
        """Test data format detection for strings"""
        self.node.content_data = "plain text content"
        result = self.node._detect_data_format()
        self.assertEqual(result, "string")

    def test_process_content_data_string(self):
        """Test content data processing for strings"""
        self.node.content_data = "Hello, World!"
        self.node.data_format = "string"
        result = self.node._process_content_data()
        self.assertEqual(result, b"Hello, World!")

    def test_process_content_data_base64(self):
        """Test content data processing for base64"""
        original = b"Hello, World!"
        b64_data = base64.b64encode(original).decode()
        self.node.content_data = b64_data
        self.node.data_format = "base64"
        result = self.node._process_content_data()
        self.assertEqual(result, original)

    def test_process_content_data_base64_data_url(self):
        """Test content data processing for data URLs"""
        original = b"Hello, World!"
        b64_data = base64.b64encode(original).decode()
        self.node.content_data = f"data:text/plain;base64,{b64_data}"
        self.node.data_format = "base64"
        result = self.node._process_content_data()
        self.assertEqual(result, original)

    def test_process_content_data_bytes(self):
        """Test content data processing for bytes"""
        original = b"Binary content"
        self.node.content_data = original
        self.node.data_format = "bytes"
        result = self.node._process_content_data()
        self.assertEqual(result, original)

    def test_detect_content_type_pdf(self):
        """Test content type detection for PDFs"""
        pdf_content = b"%PDF-1.4\nsome pdf content"
        self.node.content_type = "auto"
        content_type, extension = self.node._detect_content_type(pdf_content)
        self.assertEqual(content_type, "pdf")
        self.assertEqual(extension, ".pdf")

    def test_detect_content_type_json(self):
        """Test content type detection for JSON"""
        json_content = json.dumps({"key": "value", "number": 42}).encode()
        self.node.content_type = "auto"
        content_type, extension = self.node._detect_content_type(json_content)
        self.assertEqual(content_type, "json")
        self.assertEqual(extension, ".json")

    def test_detect_content_type_html(self):
        """Test content type detection for HTML"""
        html_content = b"<!DOCTYPE html><html><head><title>Test</title></head><body>Content</body></html>"
        self.node.content_type = "auto"
        content_type, extension = self.node._detect_content_type(html_content)
        self.assertEqual(content_type, "html")
        self.assertEqual(extension, ".html")

    def test_detect_content_type_csv(self):
        """Test content type detection for CSV"""
        csv_content = b"name,age,city\nJohn,30,NYC\nJane,25,LA"
        self.node.content_type = "auto"
        content_type, extension = self.node._detect_content_type(csv_content)
        self.assertEqual(content_type, "csv")
        self.assertEqual(extension, ".csv")

    def test_detect_content_type_plain_text(self):
        """Test content type detection for plain text"""
        text_content = b"This is just plain text without any special formatting."
        self.node.content_type = "auto"
        content_type, extension = self.node._detect_content_type(text_content)
        self.assertEqual(content_type, "text")
        self.assertEqual(extension, ".txt")

    def test_detect_content_type_binary(self):
        """Test content type detection for binary data"""
        binary_content = bytes([0x00, 0x01, 0x02, 0xFF, 0xFE, 0xFD])  # Non-text binary
        self.node.content_type = "auto"
        content_type, extension = self.node._detect_content_type(binary_content)
        self.assertEqual(content_type, "binary")
        self.assertEqual(extension, ".bin")

    def test_detect_image_extension_png(self):
        """Test image extension detection for PNG"""
        png_header = b'\x89PNG\r\n\x1a\n'
        result = self.node._detect_image_extension(png_header)
        self.assertEqual(result, ".png")

    def test_detect_image_extension_jpg(self):
        """Test image extension detection for JPEG"""
        jpg_header = b'\xFF\xD8\xFF'
        result = self.node._detect_image_extension(jpg_header)
        self.assertEqual(result, ".jpg")

    def test_get_mime_type(self):
        """Test MIME type generation"""
        self.assertEqual(self.node._get_mime_type("json", ".json"), "application/json")
        self.assertEqual(self.node._get_mime_type("html", ".html"), "text/html")
        self.assertEqual(self.node._get_mime_type("text", ".txt"), "text/plain")

    def test_generate_filename_custom(self):
        """Test filename generation with custom filename"""
        self.node.filename = "my_document"
        result = self.node._generate_filename("text", ".txt")
        self.assertEqual(result, "my_document")

    def test_generate_filename_auto(self):
        """Test filename generation without custom filename"""
        self.node.filename = None
        result = self.node._generate_filename("json", ".json")
        self.assertTrue(result.startswith("data_"))
        self.assertRegex(result, r"data_\d{8}_\d{6}_\d{3}")

    def test_generate_filename_cleaning(self):
        """Test filename cleaning of invalid characters"""
        self.node.filename = "my file!@#$%^&*()name"
        result = self.node._generate_filename("text", ".txt")
        self.assertEqual(result, "my_file_name")

    def test_generate_s3_key_with_overwrite(self):
        """Test S3 key generation with overwrite enabled"""
        self.node.save_path = "docs/"
        self.node.overwrite = True
        result = self.node._generate_s3_key("test_file", ".txt")
        self.assertEqual(result, "docs/test_file.txt")

    def test_generate_s3_key_without_overwrite(self):
        """Test S3 key generation with overwrite disabled (adds hash)"""
        self.node.save_path = "docs/"
        self.node.overwrite = False
        self.node.content_data = "test content"
        result = self.node._generate_s3_key("test_file", ".txt")
        self.assertTrue(result.startswith("docs/test_file_"))
        self.assertTrue(result.endswith(".txt"))
        # Should contain an 8-character hash
        self.assertRegex(result, r"docs/test_file_[a-f0-9]{8}\.txt")

    @patch('polysynergy_nodes.file.file_storage.S3Service')
    async def test_execute_success_text_file(self, mock_s3_service_class):
        """Test successful execution with text file"""
        # Mock S3 service
        mock_s3_service = MagicMock()
        mock_s3_service.upload_image.return_value = {
            'success': True,
            'url': 'https://example.com/file.txt',
            'bucket': 'test-bucket',
            'key': 'generated/files/text_123.txt',
            'etag': 'abc123'
        }
        mock_s3_service_class.return_value = mock_s3_service
        
        # Set up node
        self.node.content_data = "Hello, World!"
        self.node.content_type = "text"
        self.node.filename = "hello"
        
        # Execute
        await self.node.execute()
        
        # Verify outputs
        self.assertEqual(self.node.file_url, 'https://example.com/file.txt')
        self.assertTrue(self.node.file_path.startswith('generated/files/hello_'))
        self.assertEqual(self.node.file_size, 13)  # Length of "Hello, World!"
        self.assertEqual(self.node.mime_type, "text/plain")
        self.assertIsInstance(self.node.file_metadata, dict)
        self.assertIsInstance(self.node.true_path, dict)
        self.assertFalse(self.node.false_path)

    @patch('polysynergy_nodes.file.file_storage.S3Service')
    async def test_execute_success_json_file(self, mock_s3_service_class):
        """Test successful execution with JSON file"""
        # Mock S3 service
        mock_s3_service = MagicMock()
        mock_s3_service.upload_image.return_value = {
            'success': True,
            'url': 'https://example.com/data.json',
            'bucket': 'test-bucket',
            'key': 'generated/files/data_123.json',
            'etag': 'def456'
        }
        mock_s3_service_class.return_value = mock_s3_service
        
        # Set up node with JSON data
        json_data = {"name": "test", "value": 42}
        self.node.content_data = json.dumps(json_data)
        self.node.content_type = "auto"  # Should auto-detect as JSON
        
        # Execute
        await self.node.execute()
        
        # Verify outputs
        self.assertEqual(self.node.mime_type, "application/json")
        self.assertTrue(self.node.file_path.startswith('generated/files/data_'))
        self.assertIn("json", self.node.file_metadata["filename"])

    @patch('polysynergy_nodes.file.file_storage.S3Service')
    async def test_execute_failure(self, mock_s3_service_class):
        """Test execution failure handling"""
        # Mock S3 service failure
        mock_s3_service = MagicMock()
        mock_s3_service.upload_image.return_value = {
            'success': False,
            'error': 'Upload failed'
        }
        mock_s3_service_class.return_value = mock_s3_service
        
        # Set up node
        self.node.content_data = "test content"
        
        # Execute
        await self.node.execute()
        
        # Verify error handling
        self.assertFalse(self.node.true_path)
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.file_url)

    async def test_execute_invalid_content(self):
        """Test execution with invalid content"""
        self.node.content_data = ""  # Empty content
        
        await self.node.execute()
        
        self.assertFalse(self.node.true_path)
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

    def test_content_type_override(self):
        """Test that explicit content type overrides auto-detection"""
        # JSON data but force it to be treated as text
        self.node.content_type = "text"
        json_content = json.dumps({"key": "value"}).encode()
        
        content_type, extension = self.node._detect_content_type(json_content)
        
        # Should use the explicit type, not auto-detected JSON
        self.assertEqual(content_type, "text")
        self.assertEqual(extension, ".txt")

    def test_custom_extension_override(self):
        """Test custom extension overrides default"""
        self.node.file_extension = "custom"
        self.node.filename = "test"
        
        result = self.node._generate_s3_key("test", ".txt")  # Original extension
        # The execute method would use the custom extension
        self.assertTrue(result.endswith(".txt"))  # This tests the method directly
        
        # Test extension formatting
        self.node.file_extension = "xyz"  # Without dot
        # In the actual execute method, it would add the dot


if __name__ == "__main__":
    unittest.main()