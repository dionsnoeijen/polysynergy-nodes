import os
import base64
import asyncio
import re
from datetime import datetime
from openai import OpenAI
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.qr.services.s3_image_service import S3ImageService
from polysynergy_nodes.image.types import Image


@node(
    name="Generate Image",
    category="image",
    icon="generate.svg"
)
class GenerateImage(Node):
    # Input prompt
    prompt: str = NodeVariableSettings(
        label="Prompt",
        info="Text description of the image to generate",
        dock=dock_property(
            text_area=True,
            placeholder="A serene landscape with mountains and a lake at sunset..."
        ),
        has_in=True,
        required=True
    )
    
    # Model selection
    model: str = NodeVariableSettings(
        label="Model",
        info="AI model to use for image generation",
        dock=dock_property(
            select_values={
                "dall-e-2": "DALL-E 2 (faster, lower cost)",
                "dall-e-3": "DALL-E 3 (higher quality, more expensive)"
            }
        ),
        has_in=True,
        default="dall-e-2"
    )
    
    # Image size
    size: str = NodeVariableSettings(
        label="Size",
        info="Generated image dimensions",
        dock=dock_property(
            select_values={
                "256x256": "256x256 (small, DALL-E 2 only)",
                "512x512": "512x512 (medium, DALL-E 2 only)", 
                "1024x1024": "1024x1024 (large)",
                "1792x1024": "1792x1024 (landscape, DALL-E 3 only)",
                "1024x1792": "1024x1792 (portrait, DALL-E 3 only)"
            }
        ),
        has_in=True,
        default="1024x1024"
    )
    
    # Quality (DALL-E 3 only)
    quality: str = NodeVariableSettings(
        label="Quality",
        info="Image quality (DALL-E 3 only)",
        dock=dock_property(
            select_values={
                "standard": "Standard quality",
                "hd": "High definition"
            }
        ),
        has_in=True,
        default="standard"
    )
    
    # Style (DALL-E 3 only)
    style: str = NodeVariableSettings(
        label="Style",
        info="Image style (DALL-E 3 only)",
        dock=dock_property(
            select_values={
                "vivid": "Vivid colors and dramatic imagery",
                "natural": "Natural, realistic style"
            }
        ),
        has_in=True,
        default="vivid"
    )
    
    # Rerender control
    rerender: bool = NodeVariableSettings(
        label="Rerender",
        info="Whether to generate a new image on each run. When disabled, reuses existing image if available.",
        dock=dock_property(
            switch=True
        ),
        has_in=True,
        default=True
    )
    
    # Save path
    save_path: str = NodeVariableSettings(
        label="Save Path",
        info="Custom path where to save the generated image (relative to tenant bucket root). If empty, defaults to 'generated/images/'",
        dock=dock_property(
            placeholder="generated/images/"
        ),
        has_in=True,
        default="generated/images/"
    )

    # Outputs
    generated_image: Image = NodeVariableSettings(
        label="Generated Image",
        info="The generated image with URL and metadata",
        has_out=True
    )
    
    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the generated image",
        has_out=True
    )
    
    file_path: str = NodeVariableSettings(
        label="File Path",
        info="S3 key/path of the generated image file",
        has_out=True
    )

    true_path: dict = PathSettings(
        label="Success",
        info="Image generated successfully"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during image generation"
    )

    def get_openai_client(self) -> OpenAI:
        """Create OpenAI client with API key from environment"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return OpenAI(api_key=api_key)

    def validate_parameters(self):
        """Validate model and size combinations"""
        if not self.prompt or self.prompt.strip() == "":
            raise ValueError("Prompt cannot be empty")
        
        # DALL-E 2 size restrictions
        if self.model == "dall-e-2":
            valid_sizes = ["256x256", "512x512", "1024x1024"]
            if self.size not in valid_sizes:
                raise ValueError(f"DALL-E 2 only supports sizes: {', '.join(valid_sizes)}")
        
        # DALL-E 3 size restrictions  
        if self.model == "dall-e-3":
            valid_sizes = ["1024x1024", "1792x1024", "1024x1792"]
            if self.size not in valid_sizes:
                raise ValueError(f"DALL-E 3 only supports sizes: {', '.join(valid_sizes)}")
        
        # Validate save path
        self._validate_save_path()
    
    def _validate_save_path(self):
        """Validate and clean save path - fix minor issues, reject dangerous ones"""
        if not self.save_path or not self.save_path.strip():
            # Use default if empty or whitespace only
            self.save_path = "generated/images/"
            return
        
        # Strip whitespace
        path = self.save_path.strip()
        
        # REJECT: Directory traversal attempts
        if ".." in path:
            raise ValueError("Save path cannot contain '..' (directory traversal not allowed)")
        
        # REJECT: Absolute paths
        if path.startswith("/"):
            raise ValueError("Save path must be relative to tenant bucket root (cannot start with '/')")
        
        # REJECT: Dangerous characters that could break S3 or filesystem
        if re.search(r'[<>:"|?*\x00-\x1f]', path):
            raise ValueError("Save path contains invalid characters (<>:\"|?* or control characters)")
        
        # FIX: Remove leading/trailing whitespace from each path segment
        path_parts = [part.strip() for part in path.split('/') if part.strip()]
        
        # REJECT: Empty path parts (like "folder//subfolder" or "/folder/")
        if not path_parts:
            self.save_path = "generated/images/"
            return
            
        # FIX: Replace spaces and special chars with underscores in path segments
        cleaned_parts = []
        for part in path_parts:
            # Replace problematic characters with underscores
            cleaned_part = re.sub(r'[^\w\-.]', '_', part)
            # Remove multiple consecutive underscores
            cleaned_part = re.sub(r'_+', '_', cleaned_part)
            # Remove leading/trailing underscores
            cleaned_part = cleaned_part.strip('_')
            
            if cleaned_part:  # Only add non-empty parts
                cleaned_parts.append(cleaned_part)
        
        # REJECT: All parts were invalid
        if not cleaned_parts:
            raise ValueError("Save path contains no valid directory names")
        
        # FIX: Reconstruct path with proper formatting
        path = '/'.join(cleaned_parts) + '/'
        
        # REJECT: Path too long (S3 limit is 1024 chars, leave room for filename)
        if len(path) > 800:
            raise ValueError("Save path is too long (maximum 800 characters)")
        
        self.save_path = path

    async def generate_image_with_openai(self) -> bytes:
        """Generate image using OpenAI API"""
        def _sync_generate():
            client = self.get_openai_client()
            
            # Build parameters based on model
            params = {
                "model": self.model,
                "prompt": self.prompt.strip(),
                "size": self.size,
                "response_format": "b64_json",
                "n": 1
            }
            
            # Add DALL-E 3 specific parameters
            if self.model == "dall-e-3":
                params["quality"] = self.quality
                params["style"] = self.style
            
            try:
                response = client.images.generate(**params)
                b64_json = response.data[0].b64_json
                return base64.b64decode(b64_json)
                
            except Exception as e:
                raise Exception(f"OpenAI image generation failed: {str(e)}")
        
        return await asyncio.to_thread(_sync_generate)

    def parse_dimensions(self):
        """Parse width and height from size string"""
        width, height = self.size.split('x')
        return int(width), int(height)

    def generate_s3_key(self, with_timestamp=True):
        """Generate S3 key for generated image using custom save path or default structure"""
        node_id = os.getenv('NODE_ID', self.__class__.__name__.lower())
        execution_id = os.getenv('EXECUTION_ID', 'direct')
        
        # Use custom save_path or default structure
        # Keep the trailing slash that validation added - it's important for path consistency
        
        # Create filename with model and size info
        model_short = self.model.replace('-', '')  # dalle2, dalle3
        size_short = self.size.replace('x', 'x')   # Keep size format
        
        if with_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            filename = f"generated_{model_short}_{size_short}_{timestamp}.png"
        else:
            # For persistent images (when rerender=False), use a stable key based on content
            import hashlib
            content_hash = hashlib.md5(
                f"{self.prompt.strip()}_{self.model}_{self.size}_{self.quality}_{self.style}".encode()
            ).hexdigest()[:8]
            filename = f"cached_{model_short}_{size_short}_{content_hash}.png"
        
        # Construct full S3 key - always save directly to the specified path
        key = f"{self.save_path}{filename}"
        
        return key

    async def check_existing_image(self, s3_key: str) -> dict:
        """Check if an image already exists at the given S3 key"""
        def _sync_check():
            s3_service = S3ImageService()
            try:
                # Try to get existing image metadata
                result = s3_service.get_image_metadata(s3_key)
                if result and result.get('success'):
                    # Image exists, get its URL
                    url = s3_service.get_image_url(s3_key)
                    return {
                        'exists': True,
                        'url': url,
                        'metadata': result.get('metadata', {}),
                        'size': result.get('size', 0)
                    }
                return {'exists': False}
            except Exception:
                # If any error occurs, assume image doesn't exist
                return {'exists': False}
        
        return await asyncio.to_thread(_sync_check)

    async def execute(self):
        try:
            # Validate parameters
            self.validate_parameters()
            
            width, height = self.parse_dimensions()
            
            # Check if we should reuse existing image
            if not self.rerender:
                # Generate stable key for caching
                cached_s3_key = self.generate_s3_key(with_timestamp=False)
                existing_image = await self.check_existing_image(cached_s3_key)
                
                if existing_image['exists']:
                    # Reuse existing image
                    self.image_url = existing_image['url']
                    self.file_path = cached_s3_key
                    
                    self.generated_image = {
                        "url": existing_image['url'],
                        "mime_type": "image/png",
                        "width": width,
                        "height": height,
                        "size": existing_image.get('size', 0),
                        "metadata": {
                            "generation": {
                                "model": self.model,
                                "size": self.size,
                                "quality": self.quality if self.model == "dall-e-3" else "standard",
                                "style": self.style if self.model == "dall-e-3" else "natural",
                                "prompt": self.prompt[:200] + "..." if len(self.prompt) > 200 else self.prompt,
                                "prompt_length": len(self.prompt),
                                "cached": True  # Indicate this was reused
                            },
                            "s3_key": cached_s3_key,
                            "bucket": existing_image.get('metadata', {}).get('bucket')
                        }
                    }
                    
                    self.true_path = self.generated_image
                    return
            
            # Generate new image (either rerender=True or no existing image found)
            image_data = await self.generate_image_with_openai()
            
            # Choose appropriate S3 key based on rerender setting
            s3_key = self.generate_s3_key(with_timestamp=self.rerender)
            
            # Upload to S3
            def _sync_upload():
                s3_service = S3ImageService()
                
                return s3_service.upload_image(
                    image_data=image_data,
                    key=s3_key,
                    content_type='image/png',
                    metadata={
                        'model': self.model,
                        'size': self.size,
                        'quality': self.quality if self.model == "dall-e-3" else "standard",
                        'style': self.style if self.model == "dall-e-3" else "natural",
                        'prompt': self.prompt[:200],  # Truncate long prompts
                        'prompt_length': str(len(self.prompt))
                    }
                ), s3_key
            
            upload_result, final_s3_key = await asyncio.to_thread(_sync_upload)
            
            if not upload_result['success']:
                raise Exception(f"Failed to upload generated image: {upload_result.get('error')}")
            
            # Prepare output
            self.image_url = upload_result['url']
            self.file_path = final_s3_key
            
            self.generated_image = {
                "url": upload_result['url'],
                "mime_type": "image/png",
                "width": width,
                "height": height,
                "size": len(image_data),
                "metadata": {
                    "generation": {
                        "model": self.model,
                        "size": self.size,
                        "quality": self.quality if self.model == "dall-e-3" else "standard",
                        "style": self.style if self.model == "dall-e-3" else "natural",
                        "prompt": self.prompt[:200] + "..." if len(self.prompt) > 200 else self.prompt,
                        "prompt_length": len(self.prompt),
                        "cached": False  # Indicate this was newly generated
                    },
                    "s3_key": final_s3_key,
                    "bucket": upload_result.get('bucket')
                }
            }
            
            self.true_path = self.generated_image
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.generated_image = None
            self.image_url = None
            self.file_path = None