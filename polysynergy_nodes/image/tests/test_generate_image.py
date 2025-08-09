import unittest
import asyncio
from unittest.mock import Mock, patch, MagicMock
import base64
from polysynergy_nodes.image.generate_image import GenerateImage


class TestGenerateImage(unittest.TestCase):

    def setUp(self):
        self.node = GenerateImage()
        self.node.false_path = False
        self.node.true_path = False
        self.node.generated_image = None
        self.node.image_url = None
        self.node.save_path = "generated/images/"  # Set default save_path

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_image_dall_e_2(self, mock_getenv, mock_openai, mock_s3_service):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key',
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create mock response with b64_json
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/generated.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Execute
        self.node.prompt = "A beautiful sunset over mountains"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        
        asyncio.run(self.node.execute())
        
        # Assertions
        self.assertIsNotNone(self.node.generated_image)
        self.assertEqual(self.node.image_url, 'https://example.s3.amazonaws.com/generated.png')
        self.assertIn('url', self.node.generated_image)
        self.assertEqual(self.node.generated_image['mime_type'], 'image/png')
        self.assertEqual(self.node.generated_image['width'], 1024)
        self.assertEqual(self.node.generated_image['height'], 1024)
        
        # Verify OpenAI was called with correct parameters
        mock_client.images.generate.assert_called_with(
            model="dall-e-2",
            prompt="A beautiful sunset over mountains",
            size="1024x1024",
            response_format="b64_json",
            n=1
        )
        
        self.assertFalse(self.node.false_path)

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_image_dall_e_3(self, mock_getenv, mock_openai, mock_s3_service):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key',
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create mock response
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/generated.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Execute with DALL-E 3 parameters
        self.node.prompt = "A futuristic cityscape at night"
        self.node.model = "dall-e-3"
        self.node.size = "1792x1024"
        self.node.quality = "hd"
        self.node.style = "natural"
        
        asyncio.run(self.node.execute())
        
        # Verify OpenAI was called with DALL-E 3 specific parameters
        mock_client.images.generate.assert_called_with(
            model="dall-e-3",
            prompt="A futuristic cityscape at night",
            size="1792x1024",
            response_format="b64_json",
            n=1,
            quality="hd",
            style="natural"
        )
        
        # Check output dimensions
        self.assertEqual(self.node.generated_image['width'], 1792)
        self.assertEqual(self.node.generated_image['height'], 1024)
        self.assertFalse(self.node.false_path)

    def test_validate_parameters_empty_prompt(self):
        self.node.prompt = ""
        
        with self.assertRaises(ValueError) as context:
            self.node.validate_parameters()
        
        self.assertIn("Prompt cannot be empty", str(context.exception))

    def test_validate_parameters_dall_e_2_invalid_size(self):
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1792x1024"  # Invalid for DALL-E 2
        
        with self.assertRaises(ValueError) as context:
            self.node.validate_parameters()
        
        self.assertIn("DALL-E 2 only supports sizes", str(context.exception))

    def test_validate_parameters_dall_e_3_invalid_size(self):
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-3"
        self.node.size = "256x256"  # Invalid for DALL-E 3
        
        with self.assertRaises(ValueError) as context:
            self.node.validate_parameters()
        
        self.assertIn("DALL-E 3 only supports sizes", str(context.exception))

    def test_parse_dimensions(self):
        # Test various size formats
        self.node.size = "1024x1024"
        width, height = self.node.parse_dimensions()
        self.assertEqual(width, 1024)
        self.assertEqual(height, 1024)
        
        self.node.size = "1792x1024"
        width, height = self.node.parse_dimensions()
        self.assertEqual(width, 1792)
        self.assertEqual(height, 1024)
        
        self.node.size = "256x256"
        width, height = self.node.parse_dimensions()
        self.assertEqual(width, 256)
        self.assertEqual(height, 256)

    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_s3_key(self, mock_getenv):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        
        key = self.node.generate_s3_key()
        
        self.assertIn('generate_node', key)
        self.assertIn('exec789', key)
        self.assertIn('dalle2', key)
        self.assertIn('1024x1024', key)
        self.assertIn('.png', key)

    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_get_openai_client_missing_api_key(self, mock_getenv):
        # Mock missing API key
        mock_getenv.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.node.get_openai_client()
        
        self.assertIn("OPENAI_API_KEY environment variable is required", str(context.exception))

    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_image_openai_error(self, mock_getenv, mock_openai):
        # Mock environment variable
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key'
        }.get(key, default)
        
        # Set required attributes
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.quality = "standard"
        self.node.style = "natural"
        
        # Mock OpenAI client to raise exception
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.images.generate.side_effect = Exception("OpenAI API error")
        
        with self.assertRaises(Exception) as context:
            asyncio.run(self.node.generate_image_with_openai())
        
        self.assertIn("OpenAI image generation failed", str(context.exception))

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_s3_upload_failure(self, mock_getenv, mock_openai, mock_s3_service):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key'
        }.get(key, default)
        
        # Mock OpenAI success
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 upload failure
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': False,
            'error': 'S3 upload failed'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Execute
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        
        asyncio.run(self.node.execute())
        
        # Should have error
        self.assertIn("error", self.node.false_path)
        self.assertIn("Failed to upload", str(self.node.false_path))
        self.assertIsNone(self.node.generated_image)
        self.assertIsNone(self.node.image_url)

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_long_prompt_truncation(self, mock_getenv, mock_openai, mock_s3_service):
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key'
        }.get(key, default)
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/generated.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Execute with very long prompt
        long_prompt = "A" * 300  # 300 character prompt
        self.node.prompt = long_prompt
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        
        asyncio.run(self.node.execute())
        
        # Check that prompt is truncated in metadata but full prompt is sent to OpenAI
        metadata_prompt = self.node.generated_image['metadata']['generation']['prompt']
        self.assertIn("...", metadata_prompt)
        self.assertEqual(len(metadata_prompt), 203)  # 200 chars + "..."
        
        # But full prompt should be sent to OpenAI
        mock_client.images.generate.assert_called_with(
            model="dall-e-2",
            prompt=long_prompt,  # Full prompt
            size="1024x1024",
            response_format="b64_json",
            n=1
        )

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_rerender_enabled_generates_new_image(self, mock_getenv, mock_openai, mock_s3_service):
        """Test that when rerender=True, a new image is always generated"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key',
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/generated_new.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Set rerender to True (default behavior)
        self.node.prompt = "A beautiful sunset"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.rerender = True
        
        asyncio.run(self.node.execute())
        
        # Should generate new image
        mock_client.images.generate.assert_called_once()
        mock_s3_instance.upload_image.assert_called_once()
        
        # Check that generated_image metadata shows not cached
        self.assertIsNotNone(self.node.generated_image)
        self.assertFalse(self.node.generated_image['metadata']['generation']['cached'])

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_rerender_disabled_reuses_existing_image(self, mock_getenv, mock_s3_service):
        """Test that when rerender=False and image exists, it reuses existing image"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Mock S3 service to simulate existing image
        mock_s3_instance = MagicMock()
        mock_s3_instance.get_image_metadata.return_value = {
            'success': True,
            'metadata': {'model': 'dall-e-2'},
            'size': 1024000
        }
        mock_s3_instance.get_image_url.return_value = 'https://example.s3.amazonaws.com/cached_image.png'
        mock_s3_service.return_value = mock_s3_instance
        
        # Set rerender to False
        self.node.prompt = "A beautiful sunset"
        self.node.model = "dall-e-2" 
        self.node.size = "1024x1024"
        self.node.rerender = False
        
        asyncio.run(self.node.execute())
        
        # Should NOT call OpenAI (no image generation)
        # Should call S3 to check for existing image
        mock_s3_instance.get_image_metadata.assert_called_once()
        mock_s3_instance.get_image_url.assert_called_once()
        
        # Check that generated_image metadata shows cached
        self.assertIsNotNone(self.node.generated_image)
        self.assertTrue(self.node.generated_image['metadata']['generation']['cached'])
        self.assertEqual(self.node.image_url, 'https://example.s3.amazonaws.com/cached_image.png')

    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_rerender_disabled_generates_if_no_existing_image(self, mock_getenv, mock_openai, mock_s3_service):
        """Test that when rerender=False but no existing image, it generates new one"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key',
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 service - no existing image found, but upload succeeds
        mock_s3_instance = MagicMock()
        mock_s3_instance.get_image_metadata.return_value = {
            'success': False,
            'error': 'Image not found'
        }
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/new_generated.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Set rerender to False
        self.node.prompt = "A beautiful sunset"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.rerender = False
        
        asyncio.run(self.node.execute())
        
        # Should check for existing image first
        mock_s3_instance.get_image_metadata.assert_called_once()
        
        # Should generate new image since existing one not found
        mock_client.images.generate.assert_called_once()
        mock_s3_instance.upload_image.assert_called_once()
        
        # Check that generated_image metadata shows not cached (newly generated)
        self.assertIsNotNone(self.node.generated_image)
        self.assertFalse(self.node.generated_image['metadata']['generation']['cached'])

    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_s3_key_with_timestamp(self, mock_getenv):
        """Test S3 key generation with timestamp (rerender=True)"""
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456', 
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        
        key = self.node.generate_s3_key(with_timestamp=True)
        
        # Should contain timestamp and unique elements
        self.assertIn('generated_', key)
        self.assertIn('dalle2', key)
        self.assertIn('1024x1024', key)
        # Should be unique each time due to timestamp
        import time
        time.sleep(0.001)  # Small delay to ensure different timestamp
        key2 = self.node.generate_s3_key(with_timestamp=True)
        self.assertNotEqual(key, key2)

    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_s3_key_without_timestamp(self, mock_getenv):
        """Test S3 key generation without timestamp (rerender=False)"""
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node', 
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.prompt = "A beautiful sunset"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.quality = "standard"
        self.node.style = "natural"
        
        key = self.node.generate_s3_key(with_timestamp=False)
        
        # Should contain hash and stable elements
        self.assertIn('cached_', key)
        self.assertIn('dalle2', key)
        self.assertIn('1024x1024', key)
        
        # Should be consistent for same parameters
        key2 = self.node.generate_s3_key(with_timestamp=False)
        self.assertEqual(key, key2)
        
        # Should change if prompt changes
        self.node.prompt = "A different sunset"
        key3 = self.node.generate_s3_key(with_timestamp=False)
        self.assertNotEqual(key, key3)
    
    def test_validate_save_path_default(self):
        """Test that default save path validation works"""
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = ""  # Empty path should default
        
        self.node.validate_parameters()
        
        self.assertEqual(self.node.save_path, "generated/images/")
    
    def test_validate_save_path_custom(self):
        """Test that custom save path validation works"""
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "custom/path"
        
        self.node.validate_parameters()
        
        self.assertEqual(self.node.save_path, "custom/path/")
    
    def test_validate_save_path_directory_traversal_attack(self):
        """Test that directory traversal attacks are prevented"""
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "../secret/files"
        
        with self.assertRaises(ValueError) as context:
            self.node.validate_parameters()
        
        self.assertIn("directory traversal not allowed", str(context.exception))
    
    def test_validate_save_path_absolute_path_attack(self):
        """Test that absolute paths are prevented"""
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "/etc/passwd"
        
        with self.assertRaises(ValueError) as context:
            self.node.validate_parameters()
        
        self.assertIn("must be relative", str(context.exception))
    
    def test_validate_save_path_invalid_characters(self):
        """Test that invalid characters are prevented"""
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "path<with>invalid:chars"
        
        with self.assertRaises(ValueError) as context:
            self.node.validate_parameters()
        
        self.assertIn("invalid characters", str(context.exception))
    
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_s3_key_custom_path(self, mock_getenv):
        """Test S3 key generation with custom save path"""
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "custom/images/"
        
        key = self.node.generate_s3_key(with_timestamp=True)
        
        # Should use custom path directly, not nested structure
        self.assertIn('custom/images/', key)
        self.assertNotIn('tenant123', key)  # No tenant/project structure in custom path
        self.assertNotIn('project456', key)
        self.assertIn('generated_dalle2_1024x1024', key)
    
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_generate_s3_key_default_path_structure(self, mock_getenv):
        """Test S3 key generation with default path maintains original structure"""
        mock_getenv.side_effect = lambda key, default=None: {
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "generated/images/"  # Default path
        
        key = self.node.generate_s3_key(with_timestamp=True)
        
        # Should maintain original nested structure for default path
        self.assertIn('generated/images/', key)
        self.assertIn('generate_node', key)
        self.assertIn('exec789', key)
        self.assertIn('generated_dalle2_1024x1024', key)
    
    @patch('polysynergy_nodes.image.generate_image.S3ImageService')
    @patch('polysynergy_nodes.image.generate_image.OpenAI')
    @patch('polysynergy_nodes.image.generate_image.os.getenv')
    def test_custom_save_path_end_to_end(self, mock_getenv, mock_openai, mock_s3_service):
        """Test that custom save path works end-to-end"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'OPENAI_API_KEY': 'test-api-key',
            'TENANT_ID': 'tenant123',
            'PROJECT_ID': 'project456',
            'NODE_ID': 'generate_node',
            'EXECUTION_ID': 'exec789'
        }.get(key, default)
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        fake_image_b64 = base64.b64encode(b'fake_image_data').decode('utf-8')
        mock_response_data = MagicMock()
        mock_response_data.b64_json = fake_image_b64
        
        mock_response = MagicMock()
        mock_response.data = [mock_response_data]
        mock_client.images.generate.return_value = mock_response
        
        # Mock S3 upload
        mock_s3_instance = MagicMock()
        mock_s3_instance.upload_image.return_value = {
            'success': True,
            'url': 'https://example.s3.amazonaws.com/my-custom-path/generated_dalle2_1024x1024_20240101_120000_123.png',
            'bucket': 'test-bucket'
        }
        mock_s3_service.return_value = mock_s3_instance
        
        # Execute with custom save path
        self.node.prompt = "A beautiful sunset"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        self.node.save_path = "my-custom-path"  # Custom path without trailing slash
        
        asyncio.run(self.node.execute())
        
        # Check that the S3 key contains custom path
        upload_call = mock_s3_instance.upload_image.call_args
        uploaded_key = upload_call[1]['key']  # key is a keyword argument
        
        self.assertIn('my-custom-path/', uploaded_key)
        self.assertIn('generated_dalle2_1024x1024', uploaded_key)
        
        # Check that file_path output shows the actual save location
        self.assertEqual(self.node.file_path, uploaded_key)
        self.assertIn('my-custom-path/', self.node.file_path)
    
    def test_save_path_normalization(self):
        """Test that save paths are properly normalized"""
        self.node.prompt = "test prompt"
        self.node.model = "dall-e-2"
        self.node.size = "1024x1024"
        
        # Test double slashes get normalized
        self.node.save_path = "path//with//double//slashes"
        self.node.validate_parameters()
        self.assertEqual(self.node.save_path, "path/with/double/slashes/")
        
        # Test trailing slash is added
        self.node.save_path = "path/without/trailing/slash"
        self.node.validate_parameters()
        self.assertEqual(self.node.save_path, "path/without/trailing/slash/")
        
        # Test existing trailing slash is preserved
        self.node.save_path = "path/with/trailing/slash/"
        self.node.validate_parameters()
        self.assertEqual(self.node.save_path, "path/with/trailing/slash/")


if __name__ == "__main__":
    unittest.main()