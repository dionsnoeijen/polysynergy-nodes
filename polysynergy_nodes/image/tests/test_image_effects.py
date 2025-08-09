import unittest
from unittest.mock import Mock, patch, MagicMock
import io
from PIL import Image, ImageEnhance, ImageFilter
from polysynergy_nodes.image.image_effects import ImageEffects


class TestImageEffects(unittest.TestCase):

    def setUp(self):
        self.node = ImageEffects()
        self.node.false_path = False
        self.node.true_path = False
        self.node.processed_image = None
        self.node.image_url = None

    @patch('polysynergy_nodes.image.image_effects.S3ImageService')
    @patch('polysynergy_nodes.image.image_effects.requests')
    def test_apply_effects_complete(self, mock_requests, mock_s3_service):
        # Setup mock response for image download
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'fake_image_data'
        mock_response.raise_for_status.return_value = None
        mock_requests.get.return_value = mock_response
        
        # Create a mock PIL Image
        mock_image = MagicMock(spec=Image.Image)
        mock_image.size = (800, 600)
        mock_image.mode = 'RGB'
        mock_image.filter.return_value = mock_image
        
        # Mock enhancers
        mock_enhancer = MagicMock()
        mock_enhancer.enhance.return_value = mock_image
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/effects.jpg',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Mock image save
        def mock_save(buffer, format=None, **kwargs):
            buffer.write(b'effects_image_data')
        mock_image.save = mock_save
        
        # Mock PIL classes
        with patch('polysynergy_nodes.image.image_effects.Image.open', return_value=mock_image):
            with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Brightness', return_value=mock_enhancer):
                with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Contrast', return_value=mock_enhancer):
                    with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Color', return_value=mock_enhancer):
                        with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Sharpness', return_value=mock_enhancer):
                            # Execute with various effects
                            self.node.input_image = {"url": "https://example.com/test.jpg"}
                            self.node.brightness = 1.2
                            self.node.contrast = 1.1
                            self.node.saturation = 0.9
                            self.node.sharpness = 1.3
                            self.node.blur_radius = 0.5
                            self.node.filter_effect = "emboss"
                            self.node.quality = 85
                            
                            self.node.execute()
        
        # Assertions
        self.assertIsNotNone(self.node.processed_image)
        self.assertEqual(self.node.image_url, 'https://example.s3.amazonaws.com/effects.jpg')
        self.assertIn('url', self.node.processed_image)
        self.assertEqual(self.node.processed_image['mime_type'], 'image/jpeg')
        self.assertIn('effects', self.node.processed_image['metadata'])
        self.assertFalse(self.node.false_path)

    def test_has_any_effects(self):
        # Test default values (no effects)
        self.assertFalse(self.node.has_any_effects())
        
        # Test with brightness change
        self.node.brightness = 1.2
        self.assertTrue(self.node.has_any_effects())
        
        # Reset and test contrast
        self.node.brightness = 1.0
        self.node.contrast = 0.8
        self.assertTrue(self.node.has_any_effects())
        
        # Reset and test saturation
        self.node.contrast = 1.0
        self.node.saturation = 1.5
        self.assertTrue(self.node.has_any_effects())
        
        # Reset and test sharpness
        self.node.saturation = 1.0
        self.node.sharpness = 0.7
        self.assertTrue(self.node.has_any_effects())
        
        # Reset and test blur
        self.node.sharpness = 1.0
        self.node.blur_radius = 2.0
        self.assertTrue(self.node.has_any_effects())
        
        # Reset and test filter
        self.node.blur_radius = 0.0
        self.node.filter_effect = "smooth"
        self.assertTrue(self.node.has_any_effects())

    def test_no_effects_applied(self):
        # When no effects are applied, should skip processing
        self.node.input_image = {"url": "https://example.com/test.jpg"}
        # All default values (no effects)
        
        with patch.object(self.node, 'get_image_from_input', return_value=("https://example.com/test.jpg", {"url": "test"})):
            self.node.execute()
        
        # Should return original without processing
        self.assertEqual(self.node.processed_image, {"url": "test"})
        self.assertEqual(self.node.image_url, "https://example.com/test.jpg")
        self.assertIn("No effects applied", str(self.node.true_path))

    def test_apply_color_adjustments(self):
        # Create mock image and enhancers
        mock_image = MagicMock(spec=Image.Image)
        mock_enhanced = MagicMock(spec=Image.Image)
        
        mock_brightness_enhancer = MagicMock()
        mock_brightness_enhancer.enhance.return_value = mock_enhanced
        
        mock_contrast_enhancer = MagicMock()
        mock_contrast_enhancer.enhance.return_value = mock_enhanced
        
        mock_color_enhancer = MagicMock()
        mock_color_enhancer.enhance.return_value = mock_enhanced
        
        mock_sharpness_enhancer = MagicMock()
        mock_sharpness_enhancer.enhance.return_value = mock_enhanced
        
        with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Brightness', return_value=mock_brightness_enhancer):
            with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Contrast', return_value=mock_contrast_enhancer):
                with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Color', return_value=mock_color_enhancer):
                    with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Sharpness', return_value=mock_sharpness_enhancer):
                        # Set non-default values
                        self.node.brightness = 1.2
                        self.node.contrast = 1.1
                        self.node.saturation = 0.9
                        self.node.sharpness = 1.3
                        
                        result = self.node.apply_color_adjustments(mock_image)
                        
                        # Verify enhancers were created and used
                        mock_brightness_enhancer.enhance.assert_called_with(1.2)
                        mock_contrast_enhancer.enhance.assert_called_with(1.1)
                        mock_color_enhancer.enhance.assert_called_with(0.9)
                        mock_sharpness_enhancer.enhance.assert_called_with(1.3)

    def test_apply_color_adjustments_default_values(self):
        # When values are at default (1.0), no enhancements should be applied
        mock_image = MagicMock(spec=Image.Image)
        
        with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Brightness') as mock_brightness:
            with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Contrast') as mock_contrast:
                with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Color') as mock_color:
                    with patch('polysynergy_nodes.image.image_effects.ImageEnhance.Sharpness') as mock_sharpness:
                        # All default values (1.0)
                        result = self.node.apply_color_adjustments(mock_image)
                        
                        # No enhancers should be created
                        mock_brightness.assert_not_called()
                        mock_contrast.assert_not_called()
                        mock_color.assert_not_called()
                        mock_sharpness.assert_not_called()
                        
                        # Should return original image
                        self.assertEqual(result, mock_image)

    def test_apply_filters(self):
        # Create mock image
        mock_image = MagicMock(spec=Image.Image)
        mock_filtered = MagicMock(spec=Image.Image)
        mock_image.filter.return_value = mock_filtered
        
        # Test blur filter
        self.node.blur_radius = 2.0
        self.node.filter_effect = "none"
        
        result = self.node.apply_filters(mock_image)
        
        # Should apply Gaussian blur
        mock_image.filter.assert_called()
        
        # Reset mock
        mock_image.reset_mock()
        
        # Test other filter
        self.node.blur_radius = 0.0
        self.node.filter_effect = "emboss"
        
        result = self.node.apply_filters(mock_image)
        
        # Should apply emboss filter
        mock_image.filter.assert_called_with(ImageFilter.EMBOSS)

    def test_apply_filters_none(self):
        # When no filters are specified, should return original
        mock_image = MagicMock(spec=Image.Image)
        
        # Default values (no filters)
        self.node.blur_radius = 0.0
        self.node.filter_effect = "none"
        
        result = self.node.apply_filters(mock_image)
        
        # Should not call filter and return original
        mock_image.filter.assert_not_called()
        self.assertEqual(result, mock_image)

    def test_filter_effects_mapping(self):
        # Test that all filter effects are properly mapped
        mock_image = MagicMock(spec=Image.Image)
        mock_filtered = MagicMock(spec=Image.Image)
        mock_image.filter.return_value = mock_filtered
        
        filter_tests = [
            ("emboss", ImageFilter.EMBOSS),
            ("edge_enhance", ImageFilter.EDGE_ENHANCE),
            ("edge_enhance_more", ImageFilter.EDGE_ENHANCE_MORE),
            ("find_edges", ImageFilter.FIND_EDGES),
            ("smooth", ImageFilter.SMOOTH),
            ("smooth_more", ImageFilter.SMOOTH_MORE),
            ("sharpen", ImageFilter.SHARPEN)
        ]
        
        for filter_name, expected_filter in filter_tests:
            with self.subTest(filter=filter_name):
                mock_image.reset_mock()
                self.node.filter_effect = filter_name
                
                result = self.node.apply_filters(mock_image)
                
                mock_image.filter.assert_called_with(expected_filter)

    def test_validation_errors(self):
        # Test quality validation
        self.node.quality = 150  # Invalid
        self.node.execute()
        self.assertIn("Quality must be between", str(self.node.false_path))
        
        # Reset and test brightness validation
        self.node.false_path = False
        self.node.quality = 85
        self.node.brightness = -0.5  # Invalid
        self.node.execute()
        self.assertIn("Brightness must be between", str(self.node.false_path))
        
        # Reset and test contrast validation
        self.node.false_path = False
        self.node.brightness = 1.0
        self.node.contrast = 5.0  # Invalid
        self.node.execute()
        self.assertIn("Contrast must be between", str(self.node.false_path))
        
        # Reset and test saturation validation
        self.node.false_path = False
        self.node.contrast = 1.0
        self.node.saturation = -1.0  # Invalid
        self.node.execute()
        self.assertIn("Saturation must be between", str(self.node.false_path))
        
        # Reset and test sharpness validation
        self.node.false_path = False
        self.node.saturation = 1.0
        self.node.sharpness = 4.0  # Invalid
        self.node.execute()
        self.assertIn("Sharpness must be between", str(self.node.false_path))
        
        # Reset and test blur radius validation
        self.node.false_path = False
        self.node.sharpness = 1.0
        self.node.blur_radius = -1.0  # Invalid
        self.node.execute()
        self.assertIn("Blur radius must be between", str(self.node.false_path))
        
        # Test blur radius upper limit
        self.node.false_path = False
        self.node.blur_radius = 25.0  # Invalid
        self.node.execute()
        self.assertIn("Blur radius must be between", str(self.node.false_path))

    @patch('polysynergy_nodes.image.image_effects.os.getenv')
    def test_generate_s3_key(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'effects_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.brightness = 1.2
        self.node.contrast = 1.1
        self.node.saturation = 0.9
        self.node.sharpness = 1.3
        self.node.blur_radius = 2.5
        self.node.filter_effect = "emboss"
        
        key = self.node.generate_s3_key({})
        
        self.assertIn('tenant123', key)
        self.assertIn('project456', key)
        self.assertIn('effects_node', key)
        self.assertIn('exec789', key)
        self.assertIn('br1.2', key)
        self.assertIn('co1.1', key)
        self.assertIn('sa0.9', key)
        self.assertIn('sh1.3', key)
        self.assertIn('bl2.5', key)
        self.assertIn('femboss', key)
        self.assertIn('.jpg', key)

    @patch('polysynergy_nodes.image.image_effects.os.getenv')
    def test_generate_s3_key_no_effects(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'effects_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # All default values (no effects)
        key = self.node.generate_s3_key({})
        
        self.assertIn('tenant123', key)
        self.assertIn('project456', key)
        self.assertIn('effects_node', key)
        self.assertIn('exec789', key)
        self.assertIn('noeffects', key)
        self.assertIn('.jpg', key)


if __name__ == "__main__":
    unittest.main()