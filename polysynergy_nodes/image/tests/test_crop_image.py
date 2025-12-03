import unittest
from unittest.mock import Mock, patch, MagicMock
import io
from PIL import Image
from polysynergy_nodes.image.crop_image import CropImage


class TestCropImage(unittest.TestCase):

    def setUp(self):
        self.node = CropImage()
        self.node.false_path = False
        self.node.true_path = False
        self.node.cropped_image = None
        self.node.image_url = None

    @patch('polysynergy_nodes.image.crop_image.S3Service')
    @patch('polysynergy_nodes.image.crop_image.requests')
    def test_crop_image_pixels_mode(self, mock_requests, mock_s3_service):
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
        
        # Mock cropped image
        mock_cropped = MagicMock(spec=Image.Image)
        mock_image.crop.return_value = mock_cropped
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/cropped.jpg',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Mock image save
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'cropped_image_data')
        mock_cropped.save = mock_save
        
        # Mock PIL Image.open
        with patch('polysynergy_nodes.image.crop_image.Image.open', return_value=mock_image):
            # Execute
            self.node.input_image = {"url": "https://example.com/test.jpg"}
            self.node.crop_mode = "pixels"
            self.node.x = 100
            self.node.y = 50
            self.node.width = 400
            self.node.height = 300
            self.node.quality = 85
            
            self.node.execute()
        
        # Assertions
        self.assertIsNotNone(self.node.cropped_image)
        self.assertEqual(self.node.image_url, 'https://example.s3.amazonaws.com/cropped.jpg')
        self.assertIn('url', self.node.cropped_image)
        self.assertEqual(self.node.cropped_image['mime_type'], 'image/jpeg')
        mock_image.crop.assert_called_with((100, 50, 500, 350))  # x, y, x+w, y+h
        self.assertFalse(self.node.false_path)

    def test_calculate_crop_box_pixels(self):
        self.node.crop_mode = "pixels"
        self.node.x = 100
        self.node.y = 50
        self.node.width = 400
        self.node.height = 300
        
        left, top, right, bottom = self.node.calculate_crop_box(800, 600)
        
        self.assertEqual(left, 100)
        self.assertEqual(top, 50)
        self.assertEqual(right, 500)  # 100 + 400
        self.assertEqual(bottom, 350)  # 50 + 300

    def test_calculate_crop_box_pixels_with_bounds(self):
        self.node.crop_mode = "pixels"
        self.node.x = 700  # Near edge
        self.node.y = 500  # Near edge
        self.node.width = 200  # Would exceed bounds
        self.node.height = 200  # Would exceed bounds
        
        left, top, right, bottom = self.node.calculate_crop_box(800, 600)
        
        self.assertEqual(left, 700)
        self.assertEqual(top, 500)
        self.assertEqual(right, 800)  # Constrained to image width
        self.assertEqual(bottom, 600)  # Constrained to image height

    def test_calculate_crop_box_percentage(self):
        self.node.crop_mode = "percentage"
        self.node.x_percent = 25.0  # 25% from left
        self.node.y_percent = 20.0  # 20% from top
        self.node.width_percent = 50.0  # 50% of width
        self.node.height_percent = 60.0  # 60% of height
        
        left, top, right, bottom = self.node.calculate_crop_box(800, 600)
        
        self.assertEqual(left, 200)  # 25% of 800
        self.assertEqual(top, 120)   # 20% of 600
        self.assertEqual(right, 600) # 200 + 50% of 800
        self.assertEqual(bottom, 480) # 120 + 60% of 600

    def test_calculate_crop_box_center_square(self):
        self.node.crop_mode = "center_square"
        
        # Test with wider image (width > height)
        left, top, right, bottom = self.node.calculate_crop_box(800, 600)
        
        size = 600  # min(800, 600)
        expected_x = (800 - 600) // 2  # 100
        expected_y = (600 - 600) // 2  # 0
        
        self.assertEqual(left, expected_x)
        self.assertEqual(top, expected_y)
        self.assertEqual(right, expected_x + size)
        self.assertEqual(bottom, expected_y + size)

    def test_calculate_crop_box_center_circle(self):
        self.node.crop_mode = "center_circle"
        
        # Test with taller image (height > width)
        left, top, right, bottom = self.node.calculate_crop_box(600, 800)
        
        size = 600  # min(600, 800)
        expected_x = (600 - 600) // 2  # 0
        expected_y = (800 - 600) // 2  # 100
        
        self.assertEqual(left, expected_x)
        self.assertEqual(top, expected_y)
        self.assertEqual(right, expected_x + size)
        self.assertEqual(bottom, expected_y + size)

    def test_validate_crop_parameters_pixels(self):
        self.node.crop_mode = "pixels"
        
        # Valid parameters
        self.node.x = 0
        self.node.y = 0
        self.node.width = 100
        self.node.height = 100
        self.node.validate_crop_parameters()  # Should not raise
        
        # Invalid x
        self.node.x = -10
        with self.assertRaises(ValueError) as context:
            self.node.validate_crop_parameters()
        self.assertIn("X position cannot be negative", str(context.exception))

    def test_validate_crop_parameters_percentage(self):
        self.node.crop_mode = "percentage"
        
        # Valid parameters
        self.node.x_percent = 10.0
        self.node.y_percent = 20.0
        self.node.width_percent = 50.0
        self.node.height_percent = 60.0
        self.node.validate_crop_parameters()  # Should not raise
        
        # Invalid percentage range
        self.node.x_percent = 150.0  # > 100
        with self.assertRaises(ValueError) as context:
            self.node.validate_crop_parameters()
        self.assertIn("X percent must be between 0 and 100", str(context.exception))
        
        # Reset and test bounds check
        self.node.x_percent = 50.0
        self.node.width_percent = 60.0  # 50 + 60 = 110 > 100
        with self.assertRaises(ValueError) as context:
            self.node.validate_crop_parameters()
        self.assertIn("X percent + Width percent cannot exceed 100", str(context.exception))

    def test_no_crop_needed(self):
        # When crop area matches full image, should skip processing
        self.node.input_image = {"url": "https://example.com/test.jpg"}
        self.node.crop_mode = "pixels"
        self.node.x = 0
        self.node.y = 0
        self.node.width = 800
        self.node.height = 600
        
        with patch.object(self.node, 'get_image_from_input', return_value=("https://example.com/test.jpg", {"url": "test"})):
            with patch.object(self.node, 'download_image') as mock_download:
                mock_image = MagicMock()
                mock_image.size = (800, 600)  # Same as crop area
                mock_download.return_value = mock_image
                
                self.node.execute()
        
        # Should return original without processing
        self.assertEqual(self.node.cropped_image, {"url": "test"})
        self.assertEqual(self.node.image_url, "https://example.com/test.jpg")
        self.assertIn("No cropping needed", str(self.node.true_path))

    def test_validation_errors(self):
        # Test quality validation
        self.node.quality = 150  # Invalid
        self.node.execute()
        self.assertIn("Quality must be between", str(self.node.false_path))

    def test_invalid_crop_area(self):
        self.node.input_image = {"url": "https://example.com/test.jpg"}
        self.node.crop_mode = "pixels"
        self.node.x = 100
        self.node.y = 50
        self.node.width = 0  # Invalid - would result in empty crop
        self.node.height = 300
        
        with patch.object(self.node, 'get_image_from_input', return_value=("https://example.com/test.jpg", {"url": "test"})):
            with patch.object(self.node, 'download_image') as mock_download:
                mock_image = MagicMock()
                mock_image.size = (800, 600)
                mock_download.return_value = mock_image
                
                self.node.execute()
        
        self.assertIn("width and height must be positive", str(self.node.false_path))

    def test_crop_area_exceeds_bounds(self):
        self.node.input_image = {"url": "https://example.com/test.jpg"}
        self.node.crop_mode = "pixels"
        self.node.x = 100
        self.node.y = 50
        self.node.width = 800  # Would exceed image bounds
        self.node.height = 300
        
        with patch.object(self.node, 'get_image_from_input', return_value=("https://example.com/test.jpg", {"url": "test"})):
            with patch.object(self.node, 'download_image') as mock_download:
                mock_image = MagicMock()
                mock_image.size = (800, 600)
                mock_download.return_value = mock_image
                
                self.node.execute()
        
        self.assertIn("extends beyond image boundaries", str(self.node.false_path))

    @patch('polysynergy_nodes.image.crop_image.os.getenv')
    def test_generate_s3_key_pixels(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'crop_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.crop_mode = "pixels"
        self.node.x = 100
        self.node.y = 50
        self.node.width = 400
        self.node.height = 300
        
        key = self.node.generate_s3_key({})
        
        self.assertIn('tenant123', key)
        self.assertIn('project456', key)
        self.assertIn('crop_node', key)
        self.assertIn('exec789', key)
        self.assertIn('x100y50w400h300', key)
        self.assertIn('.jpg', key)

    @patch('polysynergy_nodes.image.crop_image.os.getenv')
    def test_generate_s3_key_percentage(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'crop_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.crop_mode = "percentage"
        self.node.x_percent = 25.0
        self.node.y_percent = 20.0
        self.node.width_percent = 50.0
        self.node.height_percent = 60.0
        
        key = self.node.generate_s3_key({})
        
        self.assertIn('tenant123', key)
        self.assertIn('project456', key)
        self.assertIn('crop_node', key)
        self.assertIn('exec789', key)
        self.assertIn('px25.0py20.0pw50.0ph60.0', key)
        self.assertIn('.jpg', key)

    @patch('polysynergy_nodes.image.crop_image.os.getenv')
    def test_generate_s3_key_center_square(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'crop_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.crop_mode = "center_square"
        
        key = self.node.generate_s3_key({})
        
        self.assertIn('tenant123', key)
        self.assertIn('project456', key)
        self.assertIn('crop_node', key)
        self.assertIn('exec789', key)
        self.assertIn('center_square', key)
        self.assertIn('.jpg', key)


if __name__ == "__main__":
    unittest.main()