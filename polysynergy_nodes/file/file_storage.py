import os
import re
import base64
import asyncio
import hashlib
import mimetypes
from datetime import datetime
from typing import Optional, Union
from pathlib import Path

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings, dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.qr.services.s3_image_service import S3ImageService


@node(
    name="File Storage",
    category="file",
    icon="file_storage.svg"
)
class FileStorage(Node):
    # Content inputs
    content_data: Union[str, bytes] = NodeVariableSettings(
        label="Content Data",
        info="File content as string, bytes, or base64",
        dock=dock_property(
            text_area=True,
            placeholder="File content, base64 data, or binary data..."
        ),
        has_in=True,
        required=True
    )
    
    content_type: str = NodeVariableSettings(
        label="Content Type",
        info="Type of content being stored",
        dock=dock_property(
            select_values={
                "auto": "Auto-detect from data",
                "text": "Plain Text (.txt)",
                "html": "HTML Document (.html)",
                "css": "CSS Stylesheet (.css)",
                "javascript": "JavaScript (.js)",
                "json": "JSON Data (.json)",
                "xml": "XML Document (.xml)",
                "csv": "CSV Data (.csv)",
                "pdf": "PDF Document (.pdf)",
                "image": "Image File",
                "binary": "Binary Data"
            }
        ),
        has_in=True,
        default="auto"
    )
    
    data_format: str = NodeVariableSettings(
        label="Data Format",
        info="Format of the input data",
        dock=dock_property(
            select_values={
                "auto": "Auto-detect",
                "string": "String/Text",
                "base64": "Base64 Encoded",
                "bytes": "Raw Bytes"
            }
        ),
        has_in=True,
        default="auto"
    )
    
    # File naming
    filename: Optional[str] = NodeVariableSettings(
        label="Filename",
        info="Custom filename (without extension). If empty, auto-generates based on content type",
        dock=dock_property(
            placeholder="my_document"
        ),
        has_in=True
    )
    
    file_extension: Optional[str] = NodeVariableSettings(
        label="File Extension",
        info="Custom file extension (with or without dot). Overrides content type extension",
        dock=dock_property(
            placeholder=".txt, .pdf, .json"
        ),
        has_in=True
    )
    
    # Storage settings
    save_path: str = NodeVariableSettings(
        label="Save Path",
        info="Directory path where to save the file (relative to tenant bucket root). If empty, defaults to 'generated/files/'",
        dock=dock_property(
            placeholder="generated/files/"
        ),
        has_in=True,
        default="generated/files/"
    )
    
    overwrite: bool = NodeVariableSettings(
        label="Allow Overwrite",
        info="When disabled, creates unique filenames to avoid overwriting existing files",
        dock=dock_property(
            switch=True
        ),
        has_in=True,
        default=False
    )
    
    # Outputs
    file_url: str = NodeVariableSettings(
        label="File URL",
        info="Direct URL to the stored file",
        has_out=True
    )
    
    file_path: str = NodeVariableSettings(
        label="File Path",
        info="S3 key/path of the stored file",
        has_out=True
    )
    
    file_size: int = NodeVariableSettings(
        label="File Size",
        info="Size of the stored file in bytes",
        has_out=True
    )
    
    mime_type: str = NodeVariableSettings(
        label="MIME Type",
        info="Detected MIME type of the file",
        has_out=True
    )
    
    file_metadata: dict = NodeVariableSettings(
        label="File Metadata",
        info="File information and storage details",
        has_out=True
    )

    true_path: dict = PathSettings(
        label="Success",
        info="File stored successfully"
    )
    
    false_path: dict = PathSettings(
        label="Error",
        info="Error during file storage"
    )

    def _validate_save_path(self):
        """Validate and clean save path - same logic as generate image node"""
        if not self.save_path or not self.save_path.strip():
            self.save_path = "generated/files/"
            return
        
        path = self.save_path.strip()
        
        if ".." in path:
            raise ValueError("Save path cannot contain '..' (directory traversal not allowed)")
        
        if path.startswith("/"):
            raise ValueError("Save path must be relative to tenant bucket root (cannot start with '/')")
        
        if re.search(r'[<>:"|?*\x00-\x1f]', path):
            raise ValueError("Save path contains invalid characters (<>:\"|?* or control characters)")
        
        path_parts = [part.strip() for part in path.split('/') if part.strip()]
        
        if not path_parts:
            self.save_path = "generated/files/"
            return
            
        cleaned_parts = []
        for part in path_parts:
            cleaned_part = re.sub(r'[^\w\-.]', '_', part)
            cleaned_part = re.sub(r'_+', '_', cleaned_part)
            cleaned_part = cleaned_part.strip('_')
            
            if cleaned_part:
                cleaned_parts.append(cleaned_part)
        
        if not cleaned_parts:
            raise ValueError("Save path contains no valid directory names")
        
        path = '/'.join(cleaned_parts) + '/'
        
        if len(path) > 800:
            raise ValueError("Save path is too long (maximum 800 characters)")
        
        self.save_path = path

    def _process_content_data(self) -> bytes:
        """Process and convert content data to bytes"""
        if not self.content_data:
            raise ValueError("Content data cannot be empty")
        
        # Auto-detect data format if needed
        if self.data_format == "auto":
            self.data_format = self._detect_data_format()
        
        # Convert to bytes based on format
        if self.data_format == "bytes":
            if isinstance(self.content_data, bytes):
                return self.content_data
            elif isinstance(self.content_data, str):
                # Assume it's a string representation that needs encoding
                return self.content_data.encode('utf-8')
            else:
                raise ValueError("Invalid bytes data format")
        
        elif self.data_format == "base64":
            data_str = str(self.content_data)
            
            # Handle data URLs like "data:image/png;base64,..."
            if data_str.startswith("data:"):
                header, data = data_str.split(",", 1)
                return base64.b64decode(data)
            else:
                return base64.b64decode(data_str)
        
        elif self.data_format == "string":
            return str(self.content_data).encode('utf-8')
        
        else:
            raise ValueError(f"Unsupported data format: {self.data_format}")

    def _detect_data_format(self) -> str:
        """Auto-detect the format of input data"""
        if isinstance(self.content_data, bytes):
            return "bytes"
        
        data_str = str(self.content_data)
        
        # Check if it's base64 (heuristic)
        if data_str.startswith("data:"):
            return "base64"
        
        # Check if it looks like base64
        try:
            if len(data_str) % 4 == 0 and re.match(r'^[A-Za-z0-9+/]*={0,2}$', data_str):
                # Try to decode to verify
                base64.b64decode(data_str)
                return "base64"
        except:
            pass
        
        # Default to string
        return "string"

    def _detect_content_type(self, content_bytes: bytes) -> tuple[str, str]:
        """Auto-detect content type and appropriate file extension"""
        if self.content_type != "auto":
            return self.content_type, self._get_extension_for_type(self.content_type)
        
        # Check for common file signatures
        if content_bytes.startswith(b'%PDF'):
            return "pdf", ".pdf"
        
        if content_bytes.startswith((b'\xFF\xD8\xFF', b'\x89PNG\r\n\x1a\n', b'GIF8')):
            return "image", self._detect_image_extension(content_bytes)
        
        # Try to decode as text to see if it's text-based content
        try:
            text_content = content_bytes.decode('utf-8')
            
            # Check for HTML
            if re.search(r'<html|<!DOCTYPE html|<head|<body', text_content, re.IGNORECASE):
                return "html", ".html"
            
            # Check for XML
            if text_content.strip().startswith('<?xml') or re.search(r'<\w+.*?>', text_content):
                return "xml", ".xml"
            
            # Check for JSON
            try:
                import json
                json.loads(text_content)
                return "json", ".json"
            except:
                pass
            
            # Check for CSV (simple heuristic)
            lines = text_content.split('\n')[:5]  # Check first 5 lines
            if len(lines) > 1 and all(',' in line for line in lines if line.strip()):
                return "csv", ".csv"
            
            # Check for JavaScript
            if re.search(r'function\s+\w+|var\s+\w+|const\s+\w+|let\s+\w+|\w+\s*=\s*function', text_content):
                return "javascript", ".js"
            
            # Check for CSS
            if re.search(r'\w+\s*\{[^}]*\}|\.\w+\s*\{|#\w+\s*\{', text_content):
                return "css", ".css"
            
            # Default to plain text
            return "text", ".txt"
            
        except UnicodeDecodeError:
            # Binary content that's not a known format
            return "binary", ".bin"

    def _detect_image_extension(self, content_bytes: bytes) -> str:
        """Detect image file extension from binary content"""
        if content_bytes.startswith(b'\xFF\xD8\xFF'):
            return ".jpg"
        elif content_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            return ".png"
        elif content_bytes.startswith(b'GIF8'):
            return ".gif"
        elif content_bytes.startswith(b'RIFF') and b'WEBP' in content_bytes[:12]:
            return ".webp"
        else:
            return ".png"  # Default fallback

    def _get_extension_for_type(self, content_type: str) -> str:
        """Get appropriate file extension for content type"""
        mapping = {
            "text": ".txt",
            "html": ".html",
            "css": ".css",
            "javascript": ".js",
            "json": ".json",
            "xml": ".xml",
            "csv": ".csv",
            "pdf": ".pdf",
            "image": ".png",
            "binary": ".bin"
        }
        return mapping.get(content_type, ".txt")

    def _get_mime_type(self, content_type: str, extension: str) -> str:
        """Get MIME type for the file"""
        # Try to get from file extension first
        mime_type, _ = mimetypes.guess_type(f"file{extension}")
        if mime_type:
            return mime_type
        
        # Fallback to content type mapping
        mapping = {
            "text": "text/plain",
            "html": "text/html",
            "css": "text/css",
            "javascript": "application/javascript",
            "json": "application/json",
            "xml": "application/xml",
            "csv": "text/csv",
            "pdf": "application/pdf",
            "image": "image/png",
            "binary": "application/octet-stream"
        }
        return mapping.get(content_type, "application/octet-stream")

    def _generate_filename(self, content_type: str, extension: str) -> str:
        """Generate filename if not provided"""
        if self.filename:
            # Clean the provided filename
            clean_filename = re.sub(r'[^\w\-.]', '_', self.filename.strip())
            clean_filename = re.sub(r'_+', '_', clean_filename).strip('_')
            
            if not clean_filename:
                clean_filename = "file"
            
            return clean_filename
        
        # Auto-generate based on content type and timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        
        type_prefixes = {
            "text": "text",
            "html": "document",
            "css": "stylesheet",
            "javascript": "script",
            "json": "data",
            "xml": "document",
            "csv": "data",
            "pdf": "document",
            "image": "image",
            "binary": "file"
        }
        
        prefix = type_prefixes.get(content_type, "file")
        return f"{prefix}_{timestamp}"

    def _generate_s3_key(self, filename: str, extension: str) -> str:
        """Generate S3 key for the file"""
        full_filename = f"{filename}{extension}"
        
        # If overwrite is disabled, add hash to make it unique
        if not self.overwrite:
            content_hash = hashlib.md5(str(self.content_data).encode()).hexdigest()[:8]
            name_part, ext_part = os.path.splitext(full_filename)
            full_filename = f"{name_part}_{content_hash}{ext_part}"
        
        return f"{self.save_path}{full_filename}"

    async def execute(self):
        try:
            # Validate save path
            self._validate_save_path()
            
            # Process content data
            content_bytes = self._process_content_data()
            
            # Detect content type and extension
            detected_type, detected_ext = self._detect_content_type(content_bytes)
            
            # Use custom extension if provided
            final_extension = self.file_extension.strip() if self.file_extension else detected_ext
            if final_extension and not final_extension.startswith('.'):
                final_extension = f".{final_extension}"
            
            # Generate filename
            filename = self._generate_filename(detected_type, final_extension)
            
            # Get MIME type
            mime_type = self._get_mime_type(detected_type, final_extension)
            
            # Generate S3 key
            s3_key = self._generate_s3_key(filename, final_extension)
            
            # Upload to S3 using the same service as images
            def _sync_upload():
                s3_service = S3ImageService()
                
                return s3_service.upload_image(
                    image_data=content_bytes,
                    key=s3_key,
                    content_type=mime_type,
                    metadata={
                        'original_filename': self.filename or filename,
                        'content_type': detected_type,
                        'data_format': self.data_format,
                        'file_size': str(len(content_bytes)),
                        'created_at': datetime.now().isoformat()
                    }
                )
            
            upload_result = await asyncio.to_thread(_sync_upload)
            
            if not upload_result['success']:
                raise Exception(f"Failed to store file: {upload_result.get('error')}")
            
            # Set outputs
            self.file_url = upload_result['url']
            self.file_path = s3_key
            self.file_size = len(content_bytes)
            self.mime_type = mime_type
            
            self.file_metadata = {
                "url": upload_result['url'],
                "path": s3_key,
                "filename": f"{filename}{final_extension}",
                "size": len(content_bytes),
                "mime_type": mime_type,
                "content_type": detected_type,
                "extension": final_extension,
                "storage": {
                    "bucket": upload_result.get('bucket'),
                    "key": s3_key,
                    "etag": upload_result.get('etag'),
                    "created_at": datetime.now().isoformat()
                },
                "processing": {
                    "data_format": self.data_format,
                    "auto_detected_type": detected_type,
                    "custom_filename": bool(self.filename),
                    "custom_extension": bool(self.file_extension)
                }
            }
            
            self.true_path = self.file_metadata
            
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.file_url = None
            self.file_path = None
            self.file_size = 0
            self.mime_type = None
            self.file_metadata = None