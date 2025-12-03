import unittest
from unittest.mock import Mock, patch, MagicMock
import io
from PIL import Image
from polysynergy_nodes.image.resize_image import ResizeImage


class TestResizeImage(unittest.TestCase):

    def setUp(self):
        self.node = ResizeImage()
        self.node.false_path = False
        self.node.true_path = False
        self.node.resized_image = None
        self.node.image_url = None

    @patch('polysynergy_nodes.image.resize_image.S3Service')
    @patch('polysynergy_nodes.image.resize_image.requests')
    def test_resize_image_fit_method(self, mock_requests, mock_s3_service):
        # Setup mock response for image download
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'fake_image_data'
        mock_response.raise_for_status.return_value = None
        mock_requests.get.return_value = mock_response
        
        # Create a mock PIL Image
        mock_image = MagicMock(spec=Image.Image)
        mock_image.size = (800, 600)  # Original size
        mock_image.mode = 'RGB'
        mock_image.resize.return_value = mock_image
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/resized.jpg',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Mock image save
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'resized_image_data')
        mock_image.save = mock_save
        
        # Mock PIL Image.open
        with patch('polysynergy_nodes.image.resize_image.Image.open', return_value=mock_image):
            # Execute
            self.node.input_image = {"url": "https://example.com/test.jpg"}
            self.node.width = 400
            self.node.height = 300
            self.node.resize_method = "fit"
            self.node.quality = 85
            
            self.node.execute()
        
        # Assertions
        self.assertIsNotNone(self.node.resized_image)
        self.assertEqual(self.node.image_url, 'https://example.s3.amazonaws.com/resized.jpg')
        self.assertIn('url', self.node.resized_image)
        self.assertEqual(self.node.resized_image['mime_type'], 'image/jpeg')
        self.assertFalse(self.node.false_path)

    def test_get_image_from_input_dict(self):
        # Test with image dict containing url
        test_image = {"url": "https://example.com/test.jpg", "width": 100}
        self.node.input_image = test_image
        
        url, metadata = self.node.get_image_from_input()
        
        self.assertEqual(url, "https://example.com/test.jpg")
        self.assertEqual(metadata, test_image)

    def test_get_image_from_input_string(self):
        # Test with direct URL string
        test_url = "https://example.com/test.jpg"
        self.node.input_image = test_url
        
        url, metadata = self.node.get_image_from_input()
        
        self.assertEqual(url, test_url)
        self.assertEqual(metadata, {"url": test_url})

    def test_calculate_dimensions_fit(self):
        self.node.width = 400
        self.node.height = 300
        self.node.resize_method = "fit"
        
        # Test with wider image (should constrain by width)
        width, height = self.node.calculate_dimensions(800, 400)
        self.assertEqual(width, 400)
        self.assertEqual(height, 200)  # Aspect ratio preserved
        
        # Test with taller image (should constrain by height)
        width, height = self.node.calculate_dimensions(400, 800)
        self.assertEqual(width, 150)  # Aspect ratio preserved
        self.assertEqual(height, 300)

    def test_calculate_dimensions_fill(self):
        self.node.width = 400
        self.node.height = 300
        self.node.resize_method = "fill"
        
        # Should return exact dimensions regardless of aspect ratio
        width, height = self.node.calculate_dimensions(800, 600)
        self.assertEqual(width, 400)
        self.assertEqual(height, 300)

    def test_calculate_dimensions_with_max_constraints(self):
        self.node.width = 1000
        self.node.height = 800
        self.node.max_width = 500
        self.node.max_height = 400
        self.node.resize_method = "fit"
        
        # Should be constrained by max values
        width, height = self.node.calculate_dimensions(1000, 800)
        self.assertEqual(width, 500)
        self.assertEqual(height, 400)

    def test_no_resize_needed(self):
        # When dimensions match, should skip resize
        self.node.input_image = {"url": "https://example.com/test.jpg"}
        self.node.width = 800
        self.node.height = 600
        
        with patch.object(self.node, 'get_image_from_input', return_value=("https://example.com/test.jpg", {"url": "test"})):
            with patch.object(self.node, 'download_image') as mock_download:
                mock_image = MagicMock()
                mock_image.size = (800, 600)  # Same as target
                mock_download.return_value = mock_image
                
                self.node.execute()
        
        # Should return original without processing
        self.assertEqual(self.node.resized_image, {"url": "test"})
        self.assertEqual(self.node.image_url, "https://example.com/test.jpg")
        self.assertIn("No resize needed", str(self.node.true_path))

    def test_validation_errors(self):
        # Test quality validation
        self.node.quality = 150  # Invalid
        self.node.execute()
        self.assertIn("Quality must be between", str(self.node.false_path))
        
        # Reset
        self.node.false_path = False
        self.node.quality = 85
        
        # Test negative dimensions
        self.node.width = -10
        self.node.execute()
        self.assertIn("Width and height must be non-negative", str(self.node.false_path))
        
        # Reset
        self.node.false_path = False
        self.node.width = 0
        
        # Test no dimensions specified
        self.node.width = 0
        self.node.height = 0
        self.node.max_width = 0
        self.node.max_height = 0
        self.node.execute()
        self.assertIn("At least one dimension constraint", str(self.node.false_path))

    @patch('polysynergy_nodes.image.resize_image.requests')
    def test_download_image_error(self, mock_requests):
        # Setup mock to raise exception
        mock_requests.get.side_effect = Exception("Network error")
        
        with self.assertRaises(Exception) as context:
            self.node.download_image("https://example.com/test.jpg")
        
        self.assertIn("Failed to download image", str(context.exception))

    def test_resize_image_crop_method(self):
        # Create mock image
        mock_image = MagicMock(spec=Image.Image)
        mock_image.size = (800, 600)
        
        # Mock crop result
        mock_cropped = MagicMock(spec=Image.Image)
        mock_image.crop.return_value = mock_cropped
        
        # Test crop method
        self.node.resize_method = "crop"
        result = self.node.resize_image(mock_image, 400, 400)
        
        # Should have called crop on a resized version
        mock_image.resize.assert_called()

    def test_resize_image_pad_method(self):
        # Create mock image
        mock_image = MagicMock(spec=Image.Image)
        mock_image.size = (400, 300)
        
        # Mock the resize_image_fit method
        mock_fitted = MagicMock(spec=Image.Image)
        mock_fitted.width = 300
        mock_fitted.height = 225
        
        with patch.object(self.node, 'resize_image_fit', return_value=mock_fitted):
            with patch('polysynergy_nodes.image.resize_image.Image.new') as mock_new:
                mock_padded = MagicMock(spec=Image.Image)
                mock_new.return_value = mock_padded
                
                # Test pad method
                self.node.resize_method = "pad"
                result = self.node.resize_image(mock_image, 400, 400)
                
                # Should create new image and paste fitted image
                mock_new.assert_called_with('RGB', (400, 400), (255, 255, 255))
                mock_padded.paste.assert_called()

    @patch('polysynergy_nodes.image.resize_image.os.getenv')
    def test_generate_s3_key(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'resize_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.width = 400
        self.node.height = 300
        self.node.resize_method = "fit"
        
        key = self.node.generate_s3_key({})
        
        self.assertIn('tenant123', key)
        self.assertIn('project456', key)
        self.assertIn('resize_node', key)
        self.assertIn('exec789', key)
        self.assertIn('w400h300_fit', key)
        self.assertIn('.jpg', key)


if __name__ == "__main__":
    unittest.main()