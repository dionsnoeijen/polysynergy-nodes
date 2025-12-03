import unittest
import asyncio
from unittest.mock import Mock, patch, MagicMock
import io
from polysynergy_nodes.qr.generate_qr_code import GenerateQRCode


class TestGenerateQRCode(unittest.TestCase):

    def setUp(self):
        self.node = GenerateQRCode()
        self.node.false_path = False
        self.node.true_path = False
        self.node.qr_image = None
        self.node.image_url = None
        self.node.file_path = None
        self.node.rerender = True
        self.node.save_path = "generated/qr_codes/"

    @patch('polysynergy_nodes.qr.generate_qr_code.S3Service')
    @patch('polysynergy_nodes.qr.generate_qr_code.qrcode')
    def test_generate_simple_qr_code(self, mock_qrcode, mock_s3_service):
        # Setup mocks
        mock_qr_instance = MagicMock()
        mock_qr_instance.version = 1
        mock_qr_instance.modules = [[True, False] * 10] * 10  # Mock QR modules
        
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        mock_img.save = MagicMock()
        
        mock_qr_instance.make_image.return_value = mock_img
        mock_qrcode.QRCode.return_value = mock_qr_instance
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/test.png',
            'bucket': 'test-bucket',
            'key': 'test/test.png'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Execute
        self.node.data = "https://example.com"
        self.node.size = 400
        self.node.border = 4
        self.node.error_correction = "M"
        self.node.fill_color = "#000000"
        self.node.back_color = "#FFFFFF"
        
        # Mock save method to capture image data
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'fake_image_data')
        mock_img.save = mock_save
        
        asyncio.run(self.node.execute())
        
        # Assertions
        self.assertIsNotNone(self.node.qr_image)
        self.assertEqual(self.node.image_url, 'https://example.s3.amazonaws.com/test.png')
        self.assertIn('url', self.node.qr_image)
        self.assertIn('mime_type', self.node.qr_image)
        self.assertEqual(self.node.qr_image['mime_type'], 'image/png')
        self.assertEqual(self.node.qr_image['width'], 400)
        self.assertEqual(self.node.qr_image['height'], 400)
        self.assertFalse(self.node.false_path)

    def test_empty_data_validation(self):
        self.node.data = ""
        self.node.size = 400
        
        asyncio.run(self.node.execute())
        
        self.assertIn("error", self.node.false_path)
        self.assertIsNone(self.node.qr_image)
        self.assertIsNone(self.node.image_url)
        self.assertIsNone(self.node.file_path)

    def test_invalid_size_too_small(self):
        self.node.data = "test data"
        self.node.size = 50  # Too small
        
        asyncio.run(self.node.execute())
        
        self.assertIn("error", self.node.false_path)
        self.assertIn("Size must be between", str(self.node.false_path))

    def test_invalid_size_too_large(self):
        self.node.data = "test data"
        self.node.size = 3000  # Too large
        
        asyncio.run(self.node.execute())
        
        self.assertIn("error", self.node.false_path)
        self.assertIn("Size must be between", str(self.node.false_path))

    def test_invalid_border_negative(self):
        self.node.data = "test data"
        self.node.size = 400
        self.node.border = -1  # Invalid
        
        asyncio.run(self.node.execute())
        
        self.assertIn("error", self.node.false_path)
        self.assertIn("Border must be between", str(self.node.false_path))

    def test_invalid_border_too_large(self):
        self.node.data = "test data"
        self.node.size = 400
        self.node.border = 25  # Too large
        
        asyncio.run(self.node.execute())
        
        self.assertIn("error", self.node.false_path)
        self.assertIn("Border must be between", str(self.node.false_path))

    @patch('polysynergy_nodes.qr.generate_qr_code.S3Service')
    @patch('polysynergy_nodes.qr.generate_qr_code.qrcode')
    def test_s3_upload_failure(self, mock_qrcode, mock_s3_service):
        # Setup mocks
        mock_qr_instance = MagicMock()
        mock_qr_instance.version = 1
        mock_qr_instance.modules = [[True, False] * 10] * 10
        
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        
        mock_qr_instance.make_image.return_value = mock_img
        mock_qrcode.QRCode.return_value = mock_qr_instance
        
        # Mock S3 upload failure
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': False,
            'error': 'S3 upload failed'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Mock save method
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'fake_image_data')
        mock_img.save = mock_save
        
        # Execute
        self.node.data = "https://example.com"
        self.node.size = 400
        
        asyncio.run(self.node.execute())
        
        # Assertions
        self.assertIn("error", self.node.false_path)
        self.assertIn("S3", str(self.node.false_path))
        self.assertIsNone(self.node.qr_image)
        self.assertIsNone(self.node.image_url)
        self.assertIsNone(self.node.file_path)

    def test_error_correction_levels(self):
        levels = ["L", "M", "Q", "H"]
        for level in levels:
            with self.subTest(level=level):
                self.node.error_correction = level
                result = self.node.get_error_correction_level()
                self.assertIsNotNone(result)

    @patch('polysynergy_nodes.qr.generate_qr_code.os.getenv')
    def test_generate_s3_key(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'qr_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Test timestamped key
        key = self.node.generate_s3_key(with_timestamp=True)
        self.assertIn('generated/qr_codes/', key)
        self.assertIn('qr_', key)
        self.assertIn('.png', key)
        
        # Test cached key
        self.node.data = "test data"
        self.node.error_correction = "M"
        self.node.fill_color = "#000000"
        self.node.back_color = "#FFFFFF"
        self.node.border = 4
        
        cached_key = self.node.generate_s3_key(with_timestamp=False)
        self.assertIn('generated/qr_codes/', cached_key)
        self.assertIn('cached_qr_', cached_key)
        self.assertIn('.png', cached_key)

    @patch('polysynergy_nodes.qr.generate_qr_code.S3Service')
    @patch('polysynergy_nodes.qr.generate_qr_code.qrcode')
    def test_long_data_truncation_in_metadata(self, mock_qrcode, mock_s3_service):
        # Setup mocks
        mock_qr_instance = MagicMock()
        mock_qr_instance.version = 1
        mock_qr_instance.modules = [[True, False] * 10] * 10
        
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        
        mock_qr_instance.make_image.return_value = mock_img
        mock_qrcode.QRCode.return_value = mock_qr_instance
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/test.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Mock save method
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'fake_image_data')
        mock_img.save = mock_save
        
        # Execute with long data
        long_data = "x" * 200
        self.node.data = long_data
        self.node.size = 400
        
        asyncio.run(self.node.execute())
        
        # Check metadata truncation
        self.assertIsNotNone(self.node.qr_image)
        metadata_data = self.node.qr_image['metadata']['generation']['data']
        self.assertIn("...", metadata_data)
        self.assertEqual(len(metadata_data), 103)  # 100 chars + "..."

    @patch('polysynergy_nodes.qr.generate_qr_code.S3Service')
    @patch('polysynergy_nodes.qr.generate_qr_code.qrcode')
    def test_custom_colors(self, mock_qrcode, mock_s3_service):
        # Setup mocks
        mock_qr_instance = MagicMock()
        mock_qr_instance.version = 1
        mock_qr_instance.modules = [[True, False] * 10] * 10
        
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        
        mock_qr_instance.make_image.return_value = mock_img
        mock_qrcode.QRCode.return_value = mock_qr_instance
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/test.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Mock save method
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'fake_image_data')
        mock_img.save = mock_save
        
        # Execute with custom colors
        self.node.data = "test"
        self.node.size = 400
        self.node.fill_color = "#FF0000"  # Red
        self.node.back_color = "#0000FF"  # Blue
        
        asyncio.run(self.node.execute())
        
        # Verify make_image was called with custom colors
        mock_qr_instance.make_image.assert_called_with(
            fill_color="#FF0000",
            back_color="#0000FF"
        )
        self.assertIsNotNone(self.node.qr_image)

    def test_save_path_validation(self):
        """Test save path validation and cleaning"""
        # Test valid path
        self.node.save_path = "custom/qr/"
        self.node._validate_save_path()
        self.assertEqual(self.node.save_path, "custom/qr/")
        
        # Test path with spaces and special chars
        self.node.save_path = "custom folder/my qr-codes!"
        self.node._validate_save_path()
        self.assertEqual(self.node.save_path, "custom_folder/my_qr-codes/")
        
        # Test empty path defaults to qr_codes
        self.node.save_path = ""
        self.node._validate_save_path()
        self.assertEqual(self.node.save_path, "generated/qr_codes/")
        
        # Test directory traversal rejection
        with self.assertRaises(ValueError) as cm:
            self.node.save_path = "../dangerous/"
            self.node._validate_save_path()
        self.assertIn("directory traversal", str(cm.exception))
        
        # Test absolute path rejection
        with self.assertRaises(ValueError) as cm:
            self.node.save_path = "/absolute/path/"
            self.node._validate_save_path()
        self.assertIn("must be relative", str(cm.exception))


if __name__ == "__main__":
    unittest.main()