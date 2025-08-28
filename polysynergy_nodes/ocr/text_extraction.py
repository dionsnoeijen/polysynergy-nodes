import asyncio
import base64
import io
import os
import tempfile
from typing import Optional, Literal
from pathlib import Path

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.dock_property import dock_property


@node(
    name="Text Extraction",
    category="ocr",
    icon="text_extraction.svg",
    version=2.0,
)
class TextExtraction(Node):
    # Input settings
    input_source: str = NodeVariableSettings(
        label="Input Source",
        dock=dock_property(select_values={
            "file_path": "File Path",
            "base64": "Base64 Data",
            "url": "URL"
        }),
        default="file_path",
        has_in=True,
        required=True,
        info="How to provide the file for text extraction"
    )
    
    # Source-specific inputs
    file_path: Optional[str] = NodeVariableSettings(
        label="File Path",
        dock=True,
        has_in=True,
        info="Local file path (when source is file_path)"
    )
    
    file_data: Optional[str] = NodeVariableSettings(
        label="Base64 File Data",
        dock=True,
        has_in=True,
        info="Base64 encoded file data (when source is base64)"
    )
    
    file_url: Optional[str] = NodeVariableSettings(
        label="File URL",
        dock=True,
        has_in=True,
        info="URL to download file from (when source is url)"
    )
    
    
    # Extraction settings
    engine: str = NodeVariableSettings(
        label="OCR Engine",
        dock=dock_property(select_values={
            "auto": "Auto (Best for File Type)",
            "easyocr": "EasyOCR (Images)",
            "pymupdf": "PyMuPDF (PDF Text)",
            "textract": "AWS Textract (Cloud OCR)"
        }),
        default="auto",
        has_in=True,
        info="OCR engine to use for text extraction"
    )
    
    language: str = NodeVariableSettings(
        label="Language",
        dock=True,
        default="en",
        has_in=True,
        info="Language code for OCR (e.g., 'en', 'es', 'fr')"
    )
    
    
    # Output settings
    extracted_text: str = NodeVariableSettings(
        label="Extracted Text",
        dock=True,
        has_out=True,
        info="The extracted text content"
    )
    
    confidence_score: Optional[float] = NodeVariableSettings(
        label="Confidence Score",
        dock=True,
        has_out=True,
        info="OCR confidence score (0-1, when available)"
    )
    
    word_count: int = NodeVariableSettings(
        label="Word Count",
        dock=True,
        has_out=True,
        info="Number of words extracted"
    )
    
    detected_language: Optional[str] = NodeVariableSettings(
        label="Detected Language",
        dock=True,
        has_out=True,
        info="Automatically detected language code"
    )
    
    extraction_metadata: dict = NodeVariableSettings(
        label="Extraction Metadata",
        dock=True,
        has_out=True,
        info="Additional information about the extraction process"
    )
    
    # Path settings
    true_path: bool | str = PathSettings(
        label="Success",
        info="Triggered when text extraction succeeds. Contains extracted text."
    )
    
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered when text extraction fails. Contains error details."
    )

    async def execute(self):
        try:
            # Get file data based on input source
            file_content, file_extension = await self._get_file_content()
            
            # Choose the best engine for the file type
            chosen_engine = self._choose_engine(file_extension)
            
            # Extract text using the chosen engine
            result = await self._extract_text(file_content, file_extension, chosen_engine)
            
            # Set output variables
            self.extracted_text = result["text"]
            self.confidence_score = result.get("confidence")
            self.word_count = len(result["text"].split()) if result["text"] else 0
            self.detected_language = result.get("language", self.language)
            self.extraction_metadata = {
                "engine_used": chosen_engine,
                "file_extension": file_extension,
                "processing_time": result.get("processing_time"),
                "page_count": result.get("page_count", 1)
            }
            
            self.true_path = self.extracted_text
            
        except Exception as e:
            self.false_path = NodeError.format(e)

    async def _get_file_content(self) -> tuple[bytes, str]:
        """Get file content based on the input source"""
        try:
            if self.input_source == "file_path":
                if not self.file_path:
                    raise ValueError("file_path is required when input_source is 'file_path'")
                
                file_path = Path(self.file_path)
                if not file_path.exists():
                    raise FileNotFoundError(f"File not found: {self.file_path}")
                
                return file_path.read_bytes(), file_path.suffix.lower()
                
            elif self.input_source == "base64":
                if not self.file_data:
                    raise ValueError("file_data is required when input_source is 'base64'")
                
                # Handle data URLs like "data:image/png;base64,..."
                if self.file_data.startswith("data:"):
                    header, data = self.file_data.split(",", 1)
                    # Extract file type from header
                    content_type = header.split(";")[0].split(":")[1]
                    extension = self._content_type_to_extension(content_type)
                else:
                    data = self.file_data
                    extension = ".png"  # Default assumption
                
                return base64.b64decode(data), extension
                
            elif self.input_source == "url":
                if not self.file_url:
                    raise ValueError("file_url is required when input_source is 'url'")
                
                return await self._download_file(self.file_url)
                
                
            else:
                raise ValueError(f"Unsupported input_source: {self.input_source}")
                
        except Exception as e:
            raise Exception(f"Failed to get file content: {str(e)}")

    async def _download_file(self, url: str) -> tuple[bytes, str]:
        """Download file from URL"""
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            response.raise_for_status()
            
            # Try to get extension from URL or Content-Type
            extension = Path(url).suffix.lower()
            if not extension:
                content_type = response.headers.get("content-type", "")
                extension = self._content_type_to_extension(content_type)
            
            return response.content, extension


    def _content_type_to_extension(self, content_type: str) -> str:
        """Convert MIME type to file extension"""
        mapping = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg", 
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/tiff": ".tiff",
            "application/pdf": ".pdf",
            "text/plain": ".txt"
        }
        return mapping.get(content_type.lower(), ".png")

    def _choose_engine(self, file_extension: str) -> str:
        """Choose the best OCR engine based on file type and environment"""
        if self.engine != "auto":
            return self.engine
        
        # Check if running in Lambda environment
        is_lambda = os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None
        
        # PDF files: Always use PyMuPDF for text-based PDFs (lightweight)
        if file_extension == ".pdf":
            return "pymupdf"
        
        # For images: Use cloud OCR in Lambda, local OCR in development
        if is_lambda:
            return "textract"  # Use AWS Textract in Lambda (no heavy dependencies)
        else:
            return "easyocr"   # Use EasyOCR locally (full ML capability)


    async def _extract_text(self, file_content: bytes, file_extension: str, engine: str) -> dict:
        """Extract text using the specified engine"""
        import time
        start_time = time.time()
        
        try:
            if engine == "easyocr":
                result = await self._extract_with_easyocr(file_content, file_extension)
            elif engine == "pymupdf":
                result = await self._extract_with_pymupdf(file_content, file_extension)
            elif engine == "textract":
                result = await self._extract_with_textract(file_content, file_extension)
            else:
                raise ValueError(f"Unsupported engine: {engine}")
            
            result["processing_time"] = time.time() - start_time
            return result
            
        except Exception as e:
            raise Exception(f"Text extraction failed with {engine}: {str(e)}")

    async def _extract_with_easyocr(self, file_content: bytes, file_extension: str) -> dict:
        """Extract text using EasyOCR"""
        try:
            import easyocr
            import numpy as np
            from PIL import Image
        except ImportError as e:
            raise ImportError(
                f"EasyOCR dependencies not available: {e}. "
                "In Lambda environment, 'textract' engine is automatically used instead."
            )
        
        # Initialize reader (this might be slow on first run)
        reader = easyocr.Reader([self.language], gpu=False)
        
        # Convert to image if needed
        if file_extension == ".pdf":
            # For PDFs, convert first page to image
            import fitz
            doc = fitz.open(stream=file_content, filetype="pdf")
            page = doc[0]
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            doc.close()
        else:
            img_data = file_content
        
        # Load image
        image = Image.open(io.BytesIO(img_data))
        img_array = np.array(image)
        
        # Extract text
        results = reader.readtext(img_array)
        
        # Combine text and calculate confidence
        text_parts = []
        confidences = []
        
        for (bbox, text, confidence) in results:
            text_parts.append(text)
            confidences.append(confidence)
        
        extracted_text = " ".join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return {
            "text": extracted_text,
            "confidence": avg_confidence,
            "language": self.language
        }


    async def _extract_with_pymupdf(self, file_content: bytes, file_extension: str) -> dict:
        """Extract text using PyMuPDF (good for text-based PDFs)"""
        import fitz
        
        if file_extension != ".pdf":
            raise ValueError("PyMuPDF engine only supports PDF files")
        
        doc = fitz.open(stream=file_content, filetype="pdf")
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(text)
        
        doc.close()
        
        return {
            "text": "\n\n".join(text_parts),
            "confidence": 1.0,  # Text-based PDFs are highly reliable
            "page_count": len(doc)
        }

    async def _extract_with_textract(self, file_content: bytes, file_extension: str) -> dict:
        """Extract text using AWS Textract (cloud OCR service)"""
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        try:
            # Initialize Textract client
            textract = boto3.client('textract')
            
            # Check file size (Textract has limits)
            if len(file_content) > 10 * 1024 * 1024:  # 10MB limit for synchronous calls
                raise ValueError("File too large for Textract synchronous processing (max 10MB)")
            
            # Call Textract
            if file_extension == ".pdf":
                response = textract.detect_document_text(
                    Document={'Bytes': file_content}
                )
            else:
                # For images
                response = textract.detect_document_text(
                    Document={'Bytes': file_content}
                )
            
            # Extract text from response
            text_parts = []
            confidences = []
            
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    text_parts.append(block['Text'])
                    confidences.append(block.get('Confidence', 95.0) / 100.0)
            
            extracted_text = '\n'.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.95
            
            return {
                "text": extracted_text,
                "confidence": avg_confidence,
                "language": self.language,
                "page_count": 1  # Textract processes one page at a time for sync calls
            }
            
        except NoCredentialsError:
            raise Exception(
                "AWS credentials not configured. Please ensure AWS credentials are available "
                "for Textract OCR in Lambda environment."
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidParameterException':
                raise Exception(f"Invalid file format for Textract: {file_extension}")
            elif error_code == 'DocumentTooLargeException':
                raise Exception("Document too large for Textract")
            elif error_code == 'UnsupportedDocumentException':
                raise Exception(f"Unsupported document type for Textract: {file_extension}")
            else:
                raise Exception(f"Textract error: {e}")
        except Exception as e:
            raise Exception(f"AWS Textract extraction failed: {str(e)}")

