import os
import io
import asyncio
import requests
from PIL import Image as PILImage, ImageEnhance, ImageFilter
from datetime import datetime
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.services.s3_service import S3Service
from polysynergy_nodes.image.types import Image


@node(
    name="Image Effects",
    category="image",
    icon="effects.svg"
)
class ImageEffects(Node):
    # Input image
    input_image: Image = NodeVariableSettings(
        label="Input Image",
        info="Image to apply effects to (URL or image object)",
        dock=True,
        has_in=True,
        required=True
    )
    
    # Color adjustments
    brightness: float = NodeVariableSettings(
        label="Brightness",
        info="Brightness adjustment (0.0 = black, 1.0 = original, 2.0 = double brightness)",
        dock=True,
        has_in=True,
        default=1.0
    )
    
    contrast: float = NodeVariableSettings(
        label="Contrast",
        info="Contrast adjustment (0.0 = gray, 1.0 = original, 2.0 = double contrast)",
        dock=True,
        has_in=True,
        default=1.0
    )
    
    saturation: float = NodeVariableSettings(
        label="Saturation",
        info="Color saturation (0.0 = grayscale, 1.0 = original, 2.0 = double saturation)",
        dock=True,
        has_in=True,
        default=1.0
    )
    
    sharpness: float = NodeVariableSettings(
        label="Sharpness",
        info="Sharpness adjustment (0.0 = blurred, 1.0 = original, 2.0 = sharp)",
        dock=True,
        has_in=True,
        default=1.0
    )
    
    # Filters
    blur_radius: float = NodeVariableSettings(
        label="Blur Radius",
        info="Gaussian blur radius (0.0 = no blur)",
        dock=True,
        has_in=True,
        default=0.0
    )
    
    filter_effect: str = NodeVariableSettings(
        label="Filter Effect",
        info="Additional filter to apply",
        dock=dock_property(
            select_values={
                "none": "No filter",
                "emboss": "Emboss effect",
                "edge_enhance": "Edge enhancement",
                "edge_enhance_more": "Strong edge enhancement",
                "find_edges": "Find edges",
                "smooth": "Smooth filter",
                "smooth_more": "Strong smooth filter",
                "sharpen": "Sharpen filter"
            }
        ),
        has_in=True,
        default="none"
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
    processed_image: Image = NodeVariableSettings(
        label="Processed Image",
        info="The image with effects applied",
        has_out=True
    )
    
    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the processed image",
        has_out=True
    )

    true_path: dict = PathSettings(
        label="Success",
        info="Effects applied successfully"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during image processing"
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

    def apply_color_adjustments(self, image: PILImage.Image) -> PILImage.Image:
        """Apply brightness, contrast, saturation, and sharpness adjustments"""
        # Apply brightness
        if self.brightness != 1.0:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(self.brightness)
        
        # Apply contrast
        if self.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(self.contrast)
        
        # Apply color saturation
        if self.saturation != 1.0:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(self.saturation)
        
        # Apply sharpness
        if self.sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(self.sharpness)
        
        return image

    def apply_filters(self, image: PILImage.Image) -> PILImage.Image:
        """Apply blur and other filters"""
        # Apply Gaussian blur
        if self.blur_radius > 0:
            image = image.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))
        
        # Apply selected filter effect
        if self.filter_effect != "none":
            filter_map = {
                "emboss": ImageFilter.EMBOSS,
                "edge_enhance": ImageFilter.EDGE_ENHANCE,
                "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
                "find_edges": ImageFilter.FIND_EDGES,
                "smooth": ImageFilter.SMOOTH,
                "smooth_more": ImageFilter.SMOOTH_MORE,
                "sharpen": ImageFilter.SHARPEN
            }
            
            if self.filter_effect in filter_map:
                image = image.filter(filter_map[self.filter_effect])
        
        return image

    def has_any_effects(self) -> bool:
        """Check if any effects are actually being applied"""
        return (
            self.brightness != 1.0 or
            self.contrast != 1.0 or
            self.saturation != 1.0 or
            self.sharpness != 1.0 or
            self.blur_radius > 0 or
            self.filter_effect != "none"
        )

    def generate_s3_key(self, original_metadata: dict):
        """Generate S3 key for processed image"""
        tenant_id = os.getenv('TENANT_ID', 'unknown')
        project_id = os.getenv('PROJECT_ID', 'unknown')
        node_id = os.getenv('NODE_ID', self.__class__.__name__.lower())
        execution_id = os.getenv('EXECUTION_ID', 'direct')
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        
        # Create effects signature for filename
        effects = []
        if self.brightness != 1.0:
            effects.append(f"br{self.brightness:.1f}")
        if self.contrast != 1.0:
            effects.append(f"co{self.contrast:.1f}")
        if self.saturation != 1.0:
            effects.append(f"sa{self.saturation:.1f}")
        if self.sharpness != 1.0:
            effects.append(f"sh{self.sharpness:.1f}")
        if self.blur_radius > 0:
            effects.append(f"bl{self.blur_radius:.1f}")
        if self.filter_effect != "none":
            effects.append(f"f{self.filter_effect}")
        
        effects_str = "_".join(effects) if effects else "noeffects"
        key = f"{tenant_id}/{project_id}/{node_id}/{execution_id}/effects_{effects_str}_{timestamp}.jpg"
        
        return key

    async def execute(self):
        try:
            # Validate inputs
            if self.quality < 1 or self.quality > 100:
                raise ValueError("Quality must be between 1 and 100")
            
            if self.brightness < 0 or self.brightness > 3:
                raise ValueError("Brightness must be between 0 and 3")
            
            if self.contrast < 0 or self.contrast > 3:
                raise ValueError("Contrast must be between 0 and 3")
            
            if self.saturation < 0 or self.saturation > 3:
                raise ValueError("Saturation must be between 0 and 3")
            
            if self.sharpness < 0 or self.sharpness > 3:
                raise ValueError("Sharpness must be between 0 and 3")
            
            if self.blur_radius < 0 or self.blur_radius > 20:
                raise ValueError("Blur radius must be between 0 and 20")
            
            # Get image URL
            image_url, original_metadata = self.get_image_from_input()
            
            # Check if any effects are actually applied
            if not self.has_any_effects():
                self.processed_image = original_metadata
                self.image_url = image_url
                self.true_path = {"message": "No effects applied - all settings at default values"}
                return
            
            # Download and open image
            image = await self.download_image(image_url)
            original_width, original_height = image.size
            
            # Apply effects and upload to S3 (CPU intensive operations)
            def _sync_process_and_upload():
                # Apply color adjustments
                processed_image = self.apply_color_adjustments(image)
                
                # Apply filters
                processed_image = self.apply_filters(processed_image)
                
                # Convert to bytes
                img_bytes = io.BytesIO()
                processed_image.save(img_bytes, format='JPEG', quality=self.quality, optimize=True)
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
                        'brightness': str(self.brightness),
                        'contrast': str(self.contrast),
                        'saturation': str(self.saturation),
                        'sharpness': str(self.sharpness),
                        'blur_radius': str(self.blur_radius),
                        'filter_effect': self.filter_effect,
                        'quality': str(self.quality),
                        'original_url': image_url
                    }
                )
                
                return upload_result, image_data, s3_key
            
            upload_result, image_data, s3_key = await asyncio.to_thread(_sync_process_and_upload)
            
            if not upload_result['success']:
                raise Exception(f"Failed to upload processed image: {upload_result.get('error')}")
            
            # Prepare output
            self.image_url = upload_result['url']
            
            self.processed_image = {
                "url": upload_result['url'],
                "mime_type": "image/jpeg",
                "width": original_width,
                "height": original_height,
                "size": len(image_data),
                "metadata": {
                    "original": {
                        "width": original_width,
                        "height": original_height,
                        "url": image_url
                    },
                    "effects": {
                        "brightness": self.brightness,
                        "contrast": self.contrast,
                        "saturation": self.saturation,
                        "sharpness": self.sharpness,
                        "blur_radius": self.blur_radius,
                        "filter_effect": self.filter_effect
                    },
                    "quality": self.quality,
                    "s3_key": s3_key,
                    "bucket": upload_result.get('bucket')
                }
            }
            
            self.true_path = self.processed_image
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.processed_image = None
            self.image_url = None