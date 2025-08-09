import os
import io
import asyncio
import requests
from PIL import Image as PILImage
from datetime import datetime
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.qr.services.s3_image_service import S3ImageService
from polysynergy_nodes.image.types import Image


@node(
    name="Resize Image",
    category="image",
    icon="resize.svg"
)
class ResizeImage(Node):
    # Input image (from QR generator or other image nodes)
    input_image: Image = NodeVariableSettings(
        label="Input Image",
        info="Image to resize (URL or image object)",
        dock=True,
        has_in=True,
        required=True
    )
    
    # Resize options
    width: int = NodeVariableSettings(
        label="Width",
        info="Target width in pixels (0 = maintain aspect ratio)",
        dock=True,
        has_in=True,
        default=0
    )
    
    height: int = NodeVariableSettings(
        label="Height", 
        info="Target height in pixels (0 = maintain aspect ratio)",
        dock=True,
        has_in=True,
        default=0
    )
    
    max_width: int = NodeVariableSettings(
        label="Max Width",
        info="Maximum width (0 = no limit)",
        dock=True,
        has_in=True,
        default=0
    )
    
    max_height: int = NodeVariableSettings(
        label="Max Height",
        info="Maximum height (0 = no limit)",
        dock=True,
        has_in=True,
        default=0
    )
    
    resize_method: str = NodeVariableSettings(
        label="Resize Method",
        info="How to resize the image",
        dock=dock_property(
            select_values={
                "fit": "Fit within dimensions (maintain aspect ratio)",
                "fill": "Fill dimensions exactly (may stretch)",
                "crop": "Crop to fill dimensions",
                "pad": "Pad to fill dimensions"
            }
        ),
        has_in=True,
        default="fit"
    )
    
    quality: int = NodeVariableSettings(
        label="Quality",
        info="JPEG quality (1-100, only for JPEG output)",
        dock=True,
        has_in=True,
        default=85
    )

    # Outputs
    resized_image: Image = NodeVariableSettings(
        label="Resized Image",
        info="The resized image with URL and metadata",
        has_out=True
    )
    
    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the resized image",
        has_out=True
    )

    true_path: dict = PathSettings(
        label="Success",
        info="Image resized successfully"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during image resizing"
    )

    def get_image_from_input(self):
        """Extract image URL and metadata from various input formats"""
        if isinstance(self.input_image, dict):
            if 'url' in self.input_image:
                return self.input_image['url'], self.input_image
            elif 'image_url' in self.input_image:
                return self.input_image['image_url'], self.input_image
        elif isinstance(self.input_image, str):
            # Direct URL
            return self.input_image, {"url": self.input_image}
        
        raise ValueError("Input must be an image object with 'url' field or a direct URL string")

    async def download_image(self, url: str) -> PILImage.Image:
        """Download image from URL and return PIL Image"""
        def _sync_download():
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                image_data = io.BytesIO(response.content)
                image = PILImage.open(image_data)
                
                # Convert to RGB if necessary (handles RGBA, P, etc.)
                if image.mode in ('RGBA', 'LA'):
                    # Create white background for transparent images
                    background = PILImage.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                return image
                
            except Exception as e:
                raise Exception(f"Failed to download image from {url}: {str(e)}")
        
        return await asyncio.to_thread(_sync_download)

    def calculate_dimensions(self, original_width: int, original_height: int):
        """Calculate target dimensions based on resize method and constraints"""
        target_width = self.width if self.width > 0 else None
        target_height = self.height if self.height > 0 else None
        
        # Apply max constraints
        if self.max_width > 0:
            if target_width is None or target_width > self.max_width:
                target_width = self.max_width
                
        if self.max_height > 0:
            if target_height is None or target_height > self.max_height:
                target_height = self.max_height
        
        # If no dimensions specified, return original
        if target_width is None and target_height is None:
            return original_width, original_height
        
        # Calculate dimensions based on method
        if self.resize_method == "fill":
            # Fill exactly - may stretch
            return (target_width or original_width, 
                   target_height or original_height)
        
        elif self.resize_method in ["fit", "crop", "pad"]:
            # Calculate aspect-preserving dimensions
            aspect_ratio = original_width / original_height
            
            if target_width and target_height:
                # Both dimensions specified
                target_aspect = target_width / target_height
                
                if self.resize_method == "fit":
                    # Fit within - use smaller scaling factor
                    if aspect_ratio > target_aspect:
                        return target_width, int(target_width / aspect_ratio)
                    else:
                        return int(target_height * aspect_ratio), target_height
                else:
                    # Crop/pad - will handle in resize_image method
                    return target_width, target_height
                    
            elif target_width:
                # Only width specified
                return target_width, int(target_width / aspect_ratio)
            else:
                # Only height specified
                return int(target_height * aspect_ratio), target_height
        
        return original_width, original_height

    def resize_image(self, image: PILImage.Image, target_width: int, target_height: int) -> PILImage.Image:
        """Resize image according to the specified method"""
        if self.resize_method == "fill":
            # Simple resize, may stretch
            return image.resize((target_width, target_height), PILImage.Resampling.LANCZOS)
        
        elif self.resize_method == "fit":
            # Already calculated in calculate_dimensions
            return image.resize((target_width, target_height), PILImage.Resampling.LANCZOS)
        
        elif self.resize_method == "crop":
            # Resize and crop to fill exactly
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            target_aspect = target_width / target_height
            
            if aspect_ratio > target_aspect:
                # Image is wider - crop width
                temp_height = target_height
                temp_width = int(temp_height * aspect_ratio)
                temp_image = image.resize((temp_width, temp_height), PILImage.Resampling.LANCZOS)
                
                # Crop horizontally (center crop)
                left = (temp_width - target_width) // 2
                return temp_image.crop((left, 0, left + target_width, target_height))
            else:
                # Image is taller - crop height
                temp_width = target_width
                temp_height = int(temp_width / aspect_ratio)
                temp_image = image.resize((temp_width, temp_height), PILImage.Resampling.LANCZOS)
                
                # Crop vertically (center crop)
                top = (temp_height - target_height) // 2
                return temp_image.crop((0, top, target_width, top + target_height))
        
        elif self.resize_method == "pad":
            # Resize and pad to fill exactly
            # First fit the image
            fit_image = self.resize_image_fit(image, target_width, target_height)
            
            # Create new image with target size and white background
            padded = PILImage.new('RGB', (target_width, target_height), (255, 255, 255))
            
            # Paste the fitted image in the center
            x_offset = (target_width - fit_image.width) // 2
            y_offset = (target_height - fit_image.height) // 2
            padded.paste(fit_image, (x_offset, y_offset))
            
            return padded
        
        return image

    def resize_image_fit(self, image: PILImage.Image, max_width: int, max_height: int) -> PILImage.Image:
        """Resize image to fit within dimensions while preserving aspect ratio"""
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        target_aspect = max_width / max_height
        
        if aspect_ratio > target_aspect:
            # Image is wider - constrain by width
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            # Image is taller - constrain by height
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        return image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

    def generate_s3_key(self, original_metadata: dict):
        """Generate S3 key for resized image"""
        tenant_id = os.getenv('TENANT_ID', 'unknown')
        project_id = os.getenv('PROJECT_ID', 'unknown')
        node_id = os.getenv('NODE_ID', self.__class__.__name__.lower())
        execution_id = os.getenv('EXECUTION_ID', 'direct')
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        
        # Include resize parameters in filename
        params = f"w{self.width}h{self.height}_{self.resize_method}"
        key = f"{tenant_id}/{project_id}/{node_id}/{execution_id}/resized_{params}_{timestamp}.jpg"
        
        return key

    async def execute(self):
        try:
            # Validate inputs
            if self.quality < 1 or self.quality > 100:
                raise ValueError("Quality must be between 1 and 100")
                
            if self.width < 0 or self.height < 0:
                raise ValueError("Width and height must be non-negative")
            
            if self.width == 0 and self.height == 0 and self.max_width == 0 and self.max_height == 0:
                raise ValueError("At least one dimension constraint must be specified")
            
            # Get image URL
            image_url, original_metadata = self.get_image_from_input()
            
            # Download and open image
            image = await self.download_image(image_url)
            original_width, original_height = image.size
            
            # Calculate target dimensions
            target_width, target_height = self.calculate_dimensions(original_width, original_height)
            
            # Skip resize if dimensions are the same
            if target_width == original_width and target_height == original_height:
                self.resized_image = original_metadata
                self.image_url = image_url
                self.true_path = {"message": "No resize needed - dimensions already match"}
                return
            
            # Resize image and upload to S3 (CPU intensive operations)
            def _sync_resize_and_upload():
                # Resize image
                resized_image = self.resize_image(image, target_width, target_height)
                
                # Convert to bytes
                img_bytes = io.BytesIO()
                resized_image.save(img_bytes, format='JPEG', quality=self.quality, optimize=True)
                img_bytes.seek(0)
                image_data = img_bytes.getvalue()
                
                # Upload to S3
                s3_service = S3ImageService()
                s3_key = self.generate_s3_key(original_metadata)
                
                upload_result = s3_service.upload_image(
                    image_data=image_data,
                    key=s3_key,
                    content_type='image/jpeg',
                    metadata={
                        'original_width': str(original_width),
                        'original_height': str(original_height),
                        'target_width': str(target_width),
                        'target_height': str(target_height),
                        'resize_method': self.resize_method,
                        'quality': str(self.quality),
                        'original_url': image_url
                    }
                )
                
                return upload_result, image_data, s3_key
            
            upload_result, image_data, s3_key = await asyncio.to_thread(_sync_resize_and_upload)
            
            if not upload_result['success']:
                raise Exception(f"Failed to upload resized image: {upload_result.get('error')}")
            
            # Prepare output
            self.image_url = upload_result['url']
            
            self.resized_image = {
                "url": upload_result['url'],
                "mime_type": "image/jpeg",
                "width": target_width,
                "height": target_height,
                "size": len(image_data),
                "metadata": {
                    "original": {
                        "width": original_width,
                        "height": original_height,
                        "url": image_url
                    },
                    "resize_method": self.resize_method,
                    "quality": self.quality,
                    "s3_key": s3_key,
                    "bucket": upload_result.get('bucket')
                }
            }
            
            self.true_path = self.resized_image
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.resized_image = None
            self.image_url = None