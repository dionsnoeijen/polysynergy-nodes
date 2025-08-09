import os
import io
import qrcode
import asyncio
import re
from datetime import datetime
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.qr.services.s3_image_service import S3ImageService
from polysynergy_nodes.image.types import Image


@node(
    name="Generate QR Code",
    category="media",
    icon="qr.svg"
)
class GenerateQRCode(Node):
    data: str = NodeVariableSettings(
        label="Data",
        info="Text or URL to encode in the QR code",
        dock=True,
        has_in=True,
        required=True
    )
    
    size: int = NodeVariableSettings(
        label="Size",
        info="Size of the QR code image (pixels)",
        dock=True,
        has_in=True,
        default=400
    )
    
    border: int = NodeVariableSettings(
        label="Border",
        info="Border size in modules (default: 4)",
        dock=True,
        has_in=True,
        default=4
    )
    
    error_correction: str = NodeVariableSettings(
        label="Error Correction",
        info="Error correction level",
        dock=dock_property(
            select_values={
                "L": "Low (~7% correction)",
                "M": "Medium (~15% correction)",
                "Q": "Quartile (~25% correction)",
                "H": "High (~30% correction)"
            }
        ),
        has_in=True,
        default="M"
    )
    
    fill_color: str = NodeVariableSettings(
        label="Fill Color",
        info="QR code color (hex format, e.g., #000000)",
        dock=True,
        has_in=True,
        default="#000000"
    )
    
    back_color: str = NodeVariableSettings(
        label="Background Color",
        info="Background color (hex format, e.g., #FFFFFF)",
        dock=True,
        has_in=True,
        default="#FFFFFF"
    )
    
    # Rerender control
    rerender: bool = NodeVariableSettings(
        label="Rerender",
        info="Whether to generate a new QR code on each run. When disabled, reuses existing QR code if available.",
        dock=dock_property(
            switch=True
        ),
        has_in=True,
        default=True
    )
    
    # Save path
    save_path: str = NodeVariableSettings(
        label="Save Path",
        info="Custom path where to save the generated QR code (relative to tenant bucket root). If empty, defaults to 'generated/qr_codes/'",
        dock=dock_property(
            placeholder="generated/qr_codes/"
        ),
        has_in=True,
        default="generated/qr_codes/"
    )

    # Image output with metadata
    qr_image: Image = NodeVariableSettings(
        label="QR Code Image",
        info="Generated QR code image with URL and metadata",
        has_out=True
    )
    
    image_url: str = NodeVariableSettings(
        label="Image URL",
        info="Direct URL to the QR code image",
        has_out=True
    )
    
    file_path: str = NodeVariableSettings(
        label="File Path",
        info="S3 key/path of the generated QR code file",
        has_out=True
    )

    true_path: dict = PathSettings(
        label="Success",
        info="QR code generated successfully"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during QR code generation"
    )

    def get_error_correction_level(self):
        """Map error correction string to qrcode constants"""
        levels = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        return levels.get(self.error_correction, qrcode.constants.ERROR_CORRECT_M)

    def _validate_save_path(self):
        """Validate and clean save path - fix minor issues, reject dangerous ones"""
        if not self.save_path or not self.save_path.strip():
            # Use default if empty or whitespace only
            self.save_path = "generated/qr_codes/"
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
            self.save_path = "generated/qr_codes/"
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

    def generate_s3_key(self, with_timestamp=True):
        """Generate S3 key for generated QR code using custom save path"""
        node_id = os.getenv('NODE_ID', self.__class__.__name__.lower())
        execution_id = os.getenv('EXECUTION_ID', 'direct')
        
        # Use custom save_path
        # Keep the trailing slash that validation added - it's important for path consistency
        
        if with_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            filename = f"qr_{timestamp}.png"
        else:
            # For persistent QR codes (when rerender=False), use a stable key based on content
            import hashlib
            content_hash = hashlib.md5(
                f"{self.data}_{self.error_correction}_{self.fill_color}_{self.back_color}_{self.border}".encode()
            ).hexdigest()[:8]
            filename = f"cached_qr_{content_hash}.png"
        
        # Construct full S3 key - always save directly to the specified path
        key = f"{self.save_path}{filename}"
        
        return key

    async def check_existing_image(self, s3_key: str) -> dict:
        """Check if a QR code already exists at the given S3 key"""
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
            # Validate input
            if not self.data:
                raise ValueError("Data cannot be empty")
            
            if self.size < 100 or self.size > 2000:
                raise ValueError("Size must be between 100 and 2000 pixels")
            
            if self.border < 0 or self.border > 20:
                raise ValueError("Border must be between 0 and 20")
            
            # Validate save path
            self._validate_save_path()
            
            # Check if we should reuse existing QR code
            if not self.rerender:
                # Generate stable key for caching
                cached_s3_key = self.generate_s3_key(with_timestamp=False)
                existing_image = await self.check_existing_image(cached_s3_key)
                
                if existing_image['exists']:
                    # Reuse existing QR code
                    self.image_url = existing_image['url']
                    self.file_path = cached_s3_key
                    
                    self.qr_image = {
                        "url": existing_image['url'],
                        "mime_type": "image/png",
                        "width": self.size,  # Approximation since we don't have actual width stored
                        "height": self.size,  # Approximation since we don't have actual height stored
                        "size": existing_image.get('size', 0),
                        "metadata": {
                            "generation": {
                                "data": self.data[:100] + "..." if len(self.data) > 100 else self.data,
                                "data_length": len(self.data),
                                "error_correction": self.error_correction,
                                "border": self.border,
                                "fill_color": self.fill_color,
                                "back_color": self.back_color,
                                "cached": True  # Indicate this was reused
                            },
                            "s3_key": cached_s3_key,
                            "bucket": existing_image.get('metadata', {}).get('bucket')
                        }
                    }
                    
                    self.true_path = self.qr_image
                    return
            
            # Generate QR code in a separate thread to avoid blocking
            def _generate_qr():
                # Create QR code instance
                qr = qrcode.QRCode(
                    version=None,  # Auto-determine version
                    error_correction=self.get_error_correction_level(),
                    box_size=10,  # Will be adjusted based on size
                    border=self.border,
                )
                
                # Add data and optimize
                qr.add_data(self.data)
                qr.make(fit=True)
                
                # Calculate box size to achieve desired image size
                modules = len(qr.modules) + (2 * self.border)
                box_size = max(1, self.size // modules)
                
                # Recreate with calculated box size
                qr = qrcode.QRCode(
                    version=qr.version,
                    error_correction=self.get_error_correction_level(),
                    box_size=box_size,
                    border=self.border,
                )
                qr.add_data(self.data)
                qr.make(fit=True)
                
                # Create image
                img = qr.make_image(
                    fill_color=self.fill_color,
                    back_color=self.back_color
                )
                
                # Convert to bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG', optimize=True)
                img_bytes.seek(0)
                
                # Get actual image size and data
                actual_width, actual_height = img.size
                image_data = img_bytes.getvalue()
                
                return qr, img, actual_width, actual_height, image_data
            
            # Run QR generation in thread pool
            qr, img, actual_width, actual_height, image_data = await asyncio.to_thread(_generate_qr)
            
            # Choose appropriate S3 key based on rerender setting
            s3_key = self.generate_s3_key(with_timestamp=self.rerender)
            
            # Upload to S3 asynchronously
            def _upload_to_s3():
                s3_service = S3ImageService()
                
                return s3_service.upload_image(
                    image_data=image_data,
                    key=s3_key,
                    content_type='image/png',
                    metadata={
                        'data_length': str(len(self.data)),
                        'error_correction': self.error_correction,
                        'border': str(self.border),
                        'qr_version': str(qr.version),
                        'modules': str(len(qr.modules)),
                        'fill_color': self.fill_color,
                        'back_color': self.back_color
                    }
                ), s3_key
            
            upload_result, final_s3_key = await asyncio.to_thread(_upload_to_s3)
            
            if not upload_result['success']:
                raise Exception(f"Failed to upload to S3: {upload_result.get('error')}")
            
            # Prepare output
            self.image_url = upload_result['url']
            self.file_path = final_s3_key
            
            self.qr_image = {
                "url": upload_result['url'],
                "mime_type": "image/png",
                "width": actual_width,
                "height": actual_height,
                "size": len(image_data),
                "metadata": {
                    "generation": {
                        "data": self.data[:100] + "..." if len(self.data) > 100 else self.data,
                        "data_length": len(self.data),
                        "error_correction": self.error_correction,
                        "border": self.border,
                        "fill_color": self.fill_color,
                        "back_color": self.back_color,
                        "qr_version": qr.version,
                        "modules": len(qr.modules),
                        "cached": False  # Indicate this was newly generated
                    },
                    "s3_key": final_s3_key,
                    "bucket": upload_result.get('bucket')
                }
            }
            
            self.true_path = self.qr_image
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.qr_image = None
            self.image_url = None
            self.file_path = None