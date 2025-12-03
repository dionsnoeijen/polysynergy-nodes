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
from polysynergy_node_runner.services.s3_service import S3Service
from polysynergy_nodes.image.types import Image


@node(
    name="Crop Image",
    category="image",
    icon="crop.svg"
)
class CropImage(Node):
    # Input image
    input_image: Image = NodeVariableSettings(
        label="Input Image",
        info="Image to crop (URL or image object)",
        dock=True,
        has_in=True,
        required=True
    )
    
    # Crop coordinates
    x: int = NodeVariableSettings(
        label="X Position",
        info="Left position of crop area in pixels (0 = left edge)",
        dock=True,
        has_in=True,
        default=0
    )
    
    y: int = NodeVariableSettings(
        label="Y Position",
        info="Top position of crop area in pixels (0 = top edge)",
        dock=True,
        has_in=True,
        default=0
    )
    
    width: int = NodeVariableSettings(
        label="Width",
        info="Width of crop area in pixels (0 = use remaining width)",
        dock=True,
        has_in=True,
        default=0
    )
    
    height: int = NodeVariableSettings(
        label="Height",
        info="Height of crop area in pixels (0 = use remaining height)",
        dock=True,
        has_in=True,
        default=0
    )
    
    # Percentage-based cropping option
    crop_mode: str = NodeVariableSettings(
        label="Crop Mode",
        info="Use pixel coordinates or percentage values",
        dock=dock_property(
            select_values={
                "pixels": "Use exact pixel coordinates",
                "percentage": "Use percentage of image dimensions",
                "center_square": "Center square crop (largest possible)",
                "center_circle": "Center circle crop area"
            }
        ),
        has_in=True,
        default="pixels"
    )
    
    # Percentage values (when crop_mode is percentage)
    x_percent: float = NodeVariableSettings(
        label="X Percent",
        info="Left position as percentage (0-100)",
        dock=True,
        has_in=True,
        default=0.0
    )
    
    y_percent: float = NodeVariableSettings(
        label="Y Percent",
        info="Top position as percentage (0-100)",
        dock=True,
        has_in=True,
        default=0.0
    )
    
    width_percent: float = NodeVariableSettings(
        label="Width Percent",
        info="Width as percentage of image (0-100)",
        dock=True,
        has_in=True,
        default=100.0
    )
    
    height_percent: float = NodeVariableSettings(
        label="Height Percent",
        info="Height as percentage of image (0-100)",
        dock=True,
        has_in=True,
        default=100.0
    )
    
    # Output quality
    quality: int = NodeVariableSettings(
        label="Quality",
        info="JPEG quality (1-100)",
        dock=True,
        has_in=True,
        default=85
    )

    # Outputs
    cropped_image: Image = NodeVariableSettings(
        label="Cropped Image",
        info="The cropped image with URL and metadata",
        has_out=True
    )
    
    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the cropped image",
        has_out=True
    )

    true_path: dict = PathSettings(
        label="Success",
        info="Image cropped successfully"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during image cropping"
    )

    def get_image_from_input(self):
        """Extract image URL and metadata from various input formats"""
        if isinstance(self.input_image, dict):
            if 'url' in self.input_image:
                return self.input_image['url'], self.input_image
            elif 'image_url' in self.input_image:
                return self.input_image['image_url'], self.input_image
        elif isinstance(self.input_image, str):
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
                
                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'LA'):
                    background = PILImage.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                return image
                
            except Exception as e:
                raise Exception(f"Failed to download image from {url}: {str(e)}")
        
        return await asyncio.to_thread(_sync_download)

    def calculate_crop_box(self, image_width: int, image_height: int):
        """Calculate crop box coordinates based on mode and parameters"""
        if self.crop_mode == "pixels":
            # Use direct pixel coordinates
            x = max(0, min(self.x, image_width - 1))
            y = max(0, min(self.y, image_height - 1))
            
            # Calculate width and height
            if self.width <= 0:
                width = image_width - x
            else:
                width = min(self.width, image_width - x)
            
            if self.height <= 0:
                height = image_height - y
            else:
                height = min(self.height, image_height - y)
            
            return x, y, x + width, y + height
        
        elif self.crop_mode == "percentage":
            # Convert percentages to pixels
            x = int((self.x_percent / 100.0) * image_width)
            y = int((self.y_percent / 100.0) * image_height)
            width = int((self.width_percent / 100.0) * image_width)
            height = int((self.height_percent / 100.0) * image_height)
            
            # Ensure bounds
            x = max(0, min(x, image_width - 1))
            y = max(0, min(y, image_height - 1))
            width = min(width, image_width - x)
            height = min(height, image_height - y)
            
            return x, y, x + width, y + height
        
        elif self.crop_mode == "center_square":
            # Create largest possible centered square
            size = min(image_width, image_height)
            x = (image_width - size) // 2
            y = (image_height - size) // 2
            
            return x, y, x + size, y + size
        
        elif self.crop_mode == "center_circle":
            # Create square crop area for circular content
            size = min(image_width, image_height)
            x = (image_width - size) // 2
            y = (image_height - size) // 2
            
            return x, y, x + size, y + size
        
        return 0, 0, image_width, image_height

    def validate_crop_parameters(self):
        """Validate crop parameters based on mode"""
        if self.crop_mode == "pixels":
            if self.x < 0:
                raise ValueError("X position cannot be negative")
            if self.y < 0:
                raise ValueError("Y position cannot be negative")
            if self.width < 0:
                raise ValueError("Width cannot be negative")
            if self.height < 0:
                raise ValueError("Height cannot be negative")
        
        elif self.crop_mode == "percentage":
            if not (0 <= self.x_percent <= 100):
                raise ValueError("X percent must be between 0 and 100")
            if not (0 <= self.y_percent <= 100):
                raise ValueError("Y percent must be between 0 and 100")
            if not (0 < self.width_percent <= 100):
                raise ValueError("Width percent must be between 0 and 100")
            if not (0 < self.height_percent <= 100):
                raise ValueError("Height percent must be between 0 and 100")
            
            # Check if crop area is within bounds
            if self.x_percent + self.width_percent > 100:
                raise ValueError("X percent + Width percent cannot exceed 100")
            if self.y_percent + self.height_percent > 100:
                raise ValueError("Y percent + Height percent cannot exceed 100")

    def generate_s3_key(self, original_metadata: dict):
        """Generate S3 key for cropped image"""
        tenant_id = os.getenv('TENANT_ID', 'unknown')
        project_id = os.getenv('PROJECT_ID', 'unknown')
        node_id = os.getenv('NODE_ID', self.__class__.__name__.lower())
        execution_id = os.getenv('EXECUTION_ID', 'direct')
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        
        # Include crop parameters in filename
        if self.crop_mode == "pixels":
            params = f"x{self.x}y{self.y}w{self.width}h{self.height}"
        elif self.crop_mode == "percentage":
            params = f"px{self.x_percent}py{self.y_percent}pw{self.width_percent}ph{self.height_percent}"
        else:
            params = self.crop_mode
        
        key = f"{tenant_id}/{project_id}/{node_id}/{execution_id}/crop_{params}_{timestamp}.jpg"
        
        return key

    async def execute(self):
        try:
            # Validate inputs
            if self.quality < 1 or self.quality > 100:
                raise ValueError("Quality must be between 1 and 100")
            
            self.validate_crop_parameters()
            
            # Get image URL
            image_url, original_metadata = self.get_image_from_input()
            
            # Download and open image
            image = await self.download_image(image_url)
            original_width, original_height = image.size
            
            # Calculate crop box
            left, top, right, bottom = self.calculate_crop_box(original_width, original_height)
            
            # Validate crop box
            if left >= right or top >= bottom:
                raise ValueError("Invalid crop area - width and height must be positive")
            
            if right > original_width or bottom > original_height:
                raise ValueError("Crop area extends beyond image boundaries")
            
            # Check if no cropping is needed
            if left == 0 and top == 0 and right == original_width and bottom == original_height:
                self.cropped_image = original_metadata
                self.image_url = image_url
                self.true_path = {"message": "No cropping needed - crop area matches full image"}
                return
            
            # Crop image and upload to S3 (CPU intensive operations)
            def _sync_crop_and_upload():
                # Crop the image
                cropped_image = image.crop((left, top, right, bottom))
                crop_width = right - left
                crop_height = bottom - top
                
                # Convert to bytes
                img_bytes = io.BytesIO()
                cropped_image.save(img_bytes, format='JPEG', quality=self.quality, optimize=True)
                img_bytes.seek(0)
                image_data = img_bytes.getvalue()
                
                # Upload to S3
                s3_service = S3Service()
                s3_key = self.generate_s3_key(original_metadata)
                
                upload_result = s3_service.upload_image(
                    image_data=image_data,
                    key=s3_key,
                    content_type='image/jpeg',
                    metadata={
                        'original_width': str(original_width),
                        'original_height': str(original_height),
                        'crop_x': str(left),
                        'crop_y': str(top),
                        'crop_width': str(crop_width),
                        'crop_height': str(crop_height),
                        'crop_mode': self.crop_mode,
                        'quality': str(self.quality),
                        'original_url': image_url
                    }
                )
                
                return upload_result, image_data, s3_key, crop_width, crop_height
            
            upload_result, image_data, s3_key, crop_width, crop_height = await asyncio.to_thread(_sync_crop_and_upload)
            
            if not upload_result['success']:
                raise Exception(f"Failed to upload cropped image: {upload_result.get('error')}")
            
            # Prepare output
            self.image_url = upload_result['url']
            
            self.cropped_image = {
                "url": upload_result['url'],
                "mime_type": "image/jpeg",
                "width": crop_width,
                "height": crop_height,
                "size": len(image_data),
                "metadata": {
                    "original": {
                        "width": original_width,
                        "height": original_height,
                        "url": image_url
                    },
                    "crop": {
                        "x": left,
                        "y": top,
                        "width": crop_width,
                        "height": crop_height,
                        "mode": self.crop_mode
                    },
                    "quality": self.quality,
                    "s3_key": s3_key,
                    "bucket": upload_result.get('bucket')
                }
            }
            
            self.true_path = self.cropped_image
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.cropped_image = None
            self.image_url = None