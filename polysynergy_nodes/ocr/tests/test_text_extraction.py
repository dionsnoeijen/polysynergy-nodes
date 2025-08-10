import unittest
import asyncio
import base64
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from polysynergy_nodes.ocr.text_extraction import TextExtraction


class TestTextExtractionNode(unittest.TestCase):

    def setUp(self):
        self.node = TextExtraction()
        self.node.input_source = "file_path"
        self.node.engine = "auto"
        self.node.language = "en"
        self.node.detect_tables = False
        
        # Reset path settings
        self.node.true_path = False
        self.node.false_path = False

    def test_content_type_to_extension(self):
        """Test MIME type to extension conversion"""
        self.assertEqual(self.node._content_type_to_extension("image/jpeg"), ".jpg")
        self.assertEqual(self.node._content_type_to_extension("image/png"), ".png")
        self.assertEqual(self.node._content_type_to_extension("application/pdf"), ".pdf")
        self.assertEqual(self.node._content_type_to_extension("unknown/type"), ".png")

    def test_choose_engine_with_pdf(self):
        """Test engine selection for PDF files"""
        with patch.object(self.node, '_is_engine_available') as mock_available:
            mock_available.side_effect = lambda engine: engine == "pymupdf"
            
            chosen = self.node._choose_engine(".pdf")
            self.assertEqual(chosen, "pymupdf")

    def test_choose_engine_with_image(self):
        """Test engine selection for image files"""
        with patch.object(self.node, '_is_engine_available') as mock_available:
            mock_available.side_effect = lambda engine: engine == "easyocr"
            
            chosen = self.node._choose_engine(".jpg")
            self.assertEqual(chosen, "easyocr")

    def test_choose_engine_fallback(self):
        """Test engine fallback when preferred engines aren't available"""
        with patch.object(self.node, '_is_engine_available') as mock_available:
            mock_available.side_effect = lambda engine: engine == "tesseract"
            
            chosen = self.node._choose_engine(".jpg")
            self.assertEqual(chosen, "tesseract")

    def test_choose_engine_none_available(self):
        """Test error when no engines are available"""
        with patch.object(self.node, '_is_engine_available', return_value=False):
            with self.assertRaises(Exception) as context:
                self.node._choose_engine(".jpg")
            self.assertIn("No OCR engines available", str(context.exception))

    def test_engine_availability_checks(self):
        """Test engine availability detection"""
        # Test easyocr availability
        with patch('polysynergy_nodes.ocr.text_extraction.importlib.import_module') as mock_import:
            mock_import.return_value = None
            self.assertTrue(self.node._is_engine_available("easyocr"))
            
        # Test import error
        with patch('polysynergy_nodes.ocr.text_extraction.importlib.import_module', side_effect=ImportError):
            self.assertFalse(self.node._is_engine_available("easyocr"))

    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.read_bytes', return_value=b'fake_file_content')
    @patch('pathlib.Path.suffix', new_callable=lambda: ".jpg")
    async def test_get_file_content_file_path(self, mock_suffix, mock_read, mock_exists):
        """Test getting file content from file path"""
        self.node.input_source = "file_path"
        self.node.file_path = "/test/image.jpg"
        
        content, extension = await self.node._get_file_content()
        
        self.assertEqual(content, b'fake_file_content')
        self.assertEqual(extension, ".jpg")

    async def test_get_file_content_file_not_found(self):
        """Test file not found error"""
        self.node.input_source = "file_path"
        self.node.file_path = "/nonexistent/file.jpg"
        
        with patch('pathlib.Path.exists', return_value=False):
            with self.assertRaises(Exception) as context:
                await self.node._get_file_content()
            self.assertIn("File not found", str(context.exception))

    async def test_get_file_content_base64(self):
        """Test getting file content from base64 data"""
        self.node.input_source = "base64"
        test_data = base64.b64encode(b"test image data").decode()
        self.node.file_data = test_data
        
        content, extension = await self.node._get_file_content()
        
        self.assertEqual(content, b"test image data")
        self.assertEqual(extension, ".png")  # Default

    async def test_get_file_content_base64_data_url(self):
        """Test getting file content from data URL"""
        self.node.input_source = "base64"
        test_data = base64.b64encode(b"test image data").decode()
        self.node.file_data = f"data:image/jpeg;base64,{test_data}"
        
        content, extension = await self.node._get_file_content()
        
        self.assertEqual(content, b"test image data")
        self.assertEqual(extension, ".jpg")

    @patch('polysynergy_nodes.ocr.text_extraction.httpx.AsyncClient')
    async def test_get_file_content_url(self, mock_client):
        """Test getting file content from URL"""
        self.node.input_source = "url"
        self.node.file_url = "https://example.com/image.png"
        
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.content = b"downloaded content"
        mock_response.headers = {"content-type": "image/png"}
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = MagicMock()
        mock_client_instance.get = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        content, extension = await self.node._get_file_content()
        
        self.assertEqual(content, b"downloaded content")
        self.assertEqual(extension, ".png")

    @patch('polysynergy_nodes.ocr.text_extraction.boto3.client')
    async def test_get_file_content_s3(self, mock_boto_client):
        """Test getting file content from S3"""
        self.node.input_source = "s3"
        self.node.s3_bucket = "test-bucket"
        self.node.s3_key = "test/file.jpg"
        
        # Mock S3 response
        mock_response = {
            "Body": MagicMock()
        }
        mock_response["Body"].read.return_value = b"s3 content"
        
        mock_s3_client = MagicMock()
        mock_s3_client.get_object.return_value = mock_response
        mock_boto_client.return_value = mock_s3_client
        
        content, extension = await self.node._get_file_content()
        
        self.assertEqual(content, b"s3 content")
        self.assertEqual(extension, ".jpg")

    async def test_get_file_content_missing_required_field(self):
        """Test error when required field is missing"""
        self.node.input_source = "file_path"
        self.node.file_path = None  # Missing required field
        
        with self.assertRaises(Exception) as context:
            await self.node._get_file_content()
        self.assertIn("file_path is required", str(context.exception))

    @patch.object(TextExtraction, '_is_engine_available')
    @patch.object(TextExtraction, '_extract_with_tesseract')
    async def test_extract_text_success(self, mock_extract, mock_available):
        """Test successful text extraction"""
        mock_available.return_value = True
        mock_extract.return_value = {
            "text": "Extracted text",
            "confidence": 0.95,
            "language": "en"
        }
        
        result = await self.node._extract_text(b"fake content", ".jpg", "tesseract")
        
        self.assertEqual(result["text"], "Extracted text")
        self.assertEqual(result["confidence"], 0.95)
        self.assertIn("processing_time", result)

    @patch.object(TextExtraction, '_extract_with_tesseract')
    async def test_extract_text_engine_error(self, mock_extract):
        """Test extraction engine error handling"""
        mock_extract.side_effect = Exception("OCR failed")
        
        with self.assertRaises(Exception) as context:
            await self.node._extract_text(b"fake content", ".jpg", "tesseract")
        self.assertIn("Text extraction failed with tesseract", str(context.exception))

    @patch('polysynergy_nodes.ocr.text_extraction.easyocr.Reader')
    @patch('polysynergy_nodes.ocr.text_extraction.Image.open')
    @patch('polysynergy_nodes.ocr.text_extraction.np.array')
    async def test_extract_with_easyocr(self, mock_array, mock_image_open, mock_reader_class):
        """Test EasyOCR text extraction"""
        # Mock EasyOCR reader
        mock_reader = MagicMock()
        mock_reader.readtext.return_value = [
            ([(0, 0), (10, 0), (10, 10), (0, 10)], "Hello", 0.9),
            ([(20, 0), (30, 0), (30, 10), (20, 10)], "World", 0.8)
        ]
        mock_reader_class.return_value = mock_reader
        
        # Mock image processing
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        mock_array.return_value = "fake_array"
        
        result = await self.node._extract_with_easyocr(b"fake image", ".jpg")
        
        self.assertEqual(result["text"], "Hello World")
        self.assertAlmostEqual(result["confidence"], 0.85, places=2)
        self.assertEqual(result["language"], "en")

    @patch('polysynergy_nodes.ocr.text_extraction.pytesseract.image_to_string')
    @patch('polysynergy_nodes.ocr.text_extraction.pytesseract.image_to_data')
    @patch('polysynergy_nodes.ocr.text_extraction.Image.open')
    async def test_extract_with_tesseract(self, mock_image_open, mock_image_to_data, mock_image_to_string):
        """Test Tesseract text extraction"""
        mock_image_to_string.return_value = "  Tesseract extracted text  "
        mock_image_to_data.return_value = {
            'conf': ['95', '87', '92', '-1', '89']
        }
        
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        
        result = await self.node._extract_with_tesseract(b"fake image", ".jpg")
        
        self.assertEqual(result["text"], "Tesseract extracted text")
        self.assertAlmostEqual(result["confidence"], 0.908, places=2)  # (95+87+92+89)/4/100
        self.assertEqual(result["language"], "en")

    @patch('polysynergy_nodes.ocr.text_extraction.fitz.open')
    async def test_extract_with_pymupdf(self, mock_fitz_open):
        """Test PyMuPDF text extraction"""
        # Mock PDF document
        mock_page = MagicMock()
        mock_page.get_text.return_value = "PDF text content"
        
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        result = await self.node._extract_with_pymupdf(b"fake pdf", ".pdf")
        
        self.assertEqual(result["text"], "PDF text content")
        self.assertEqual(result["confidence"], 1.0)
        self.assertEqual(result["page_count"], 1)

    async def test_extract_with_pymupdf_non_pdf_error(self):
        """Test PyMuPDF error for non-PDF files"""
        with self.assertRaises(ValueError) as context:
            await self.node._extract_with_pymupdf(b"fake image", ".jpg")
        self.assertIn("only supports PDF files", str(context.exception))

    @patch('polysynergy_nodes.ocr.text_extraction.boto3.client')
    async def test_extract_with_textract(self, mock_boto_client):
        """Test AWS Textract extraction"""
        # Mock Textract response
        mock_response = {
            "Blocks": [
                {
                    "BlockType": "LINE",
                    "Text": "Line 1"
                },
                {
                    "BlockType": "LINE", 
                    "Text": "Line 2"
                },
                {
                    "BlockType": "WORD",
                    "Text": "Word"
                }
            ]
        }
        
        mock_textract_client = MagicMock()
        mock_textract_client.detect_document_text.return_value = mock_response
        mock_boto_client.return_value = mock_textract_client
        
        result = await self.node._extract_with_textract(b"fake content", ".jpg")
        
        self.assertEqual(result["text"], "Line 1\nLine 2")
        self.assertIsNone(result["confidence"])

    @patch.object(TextExtraction, '_get_file_content')
    @patch.object(TextExtraction, '_choose_engine')
    @patch.object(TextExtraction, '_extract_text')
    async def test_execute_success(self, mock_extract, mock_choose, mock_get_content):
        """Test successful execution"""
        # Mock the pipeline
        mock_get_content.return_value = (b"fake content", ".jpg")
        mock_choose.return_value = "tesseract"
        mock_extract.return_value = {
            "text": "Hello World",
            "confidence": 0.9,
            "language": "en",
            "processing_time": 1.5
        }
        
        await self.node.execute()
        
        # Check outputs
        self.assertEqual(self.node.extracted_text, "Hello World")
        self.assertEqual(self.node.confidence_score, 0.9)
        self.assertEqual(self.node.word_count, 2)
        self.assertEqual(self.node.detected_language, "en")
        self.assertEqual(self.node.true_path, "Hello World")
        self.assertFalse(self.node.false_path)
        
        # Check metadata
        self.assertEqual(self.node.extraction_metadata["engine_used"], "tesseract")
        self.assertEqual(self.node.extraction_metadata["file_extension"], ".jpg")

    @patch.object(TextExtraction, '_get_file_content')
    async def test_execute_error(self, mock_get_content):
        """Test execution error handling"""
        mock_get_content.side_effect = Exception("File error")
        
        await self.node.execute()
        
        # Check error handling
        self.assertFalse(self.node.true_path)
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

    def test_word_count_calculation(self):
        """Test word count calculation"""
        # This will be tested as part of execute, but let's verify the logic
        test_text = "Hello world, this is a test."
        word_count = len(test_text.split())
        self.assertEqual(word_count, 6)
        
        # Empty text
        empty_count = len("".split()) if "" else 0
        self.assertEqual(empty_count, 0)


if __name__ == "__main__":
    unittest.main()