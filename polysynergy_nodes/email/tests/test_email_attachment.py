import unittest
import asyncio
import os
import tempfile
from unittest.mock import patch
from polysynergy_nodes.email.email_attachment import EmailAttachment


class TestEmailAttachment(unittest.TestCase):

    def setUp(self):
        self.node = EmailAttachment()
        self.node.true_path = None
        self.node.false_path = None
        self.node.filename = "test.txt"
        self.node.mimetype = "text/plain"

    def test_successful_attachment_creation(self):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Hello, world!")
            temp_path = f.name
        
        try:
            self.node.filepath = temp_path
            
            asyncio.run(self.node.execute())
            
            self.assertIsNotNone(self.node.true_path)
            self.assertIsNone(self.node.false_path)
            
            # Check the attachment structure
            attachment = self.node.true_path
            self.assertIn("filename", attachment)
            self.assertIn("content", attachment)
            self.assertIn("mimetype", attachment)
            self.assertIn("size", attachment)
            
            self.assertEqual(attachment["filename"], "test.txt")
            self.assertEqual(attachment["mimetype"], "text/plain")
            self.assertGreater(attachment["size"], 0)
            
            # Verify content is base64 encoded
            import base64
            decoded = base64.b64decode(attachment["content"]).decode("utf-8")
            self.assertEqual(decoded, "Hello, world!")
            
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        self.node.filepath = "/nonexistent/file.txt"
        
        asyncio.run(self.node.execute())
        
        self.assertIsNone(self.node.true_path)
        self.assertIsNotNone(self.node.false_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("File not found", self.node.false_path["error"])

    def test_empty_file(self):
        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            self.node.filepath = temp_path
            
            asyncio.run(self.node.execute())
            
            self.assertIsNone(self.node.true_path)
            self.assertIsNotNone(self.node.false_path)
            self.assertIn("File is empty", self.node.false_path["error"])
            
        finally:
            os.unlink(temp_path)

    def test_file_too_large(self):
        # Mock os.path.getsize to return a large size
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=26 * 1024 * 1024):  # 26MB
            
            self.node.filepath = "/mock/large_file.txt"
            
            asyncio.run(self.node.execute())
            
            self.assertIsNone(self.node.true_path)
            self.assertIsNotNone(self.node.false_path)
            self.assertIn("File too large", self.node.false_path["error"])

    def test_binary_file_attachment(self):
        # Create a temporary binary file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            binary_data = bytes([0, 1, 2, 3, 255, 254, 253])
            f.write(binary_data)
            temp_path = f.name
        
        try:
            self.node.filepath = temp_path
            self.node.filename = "binary.dat"
            self.node.mimetype = "application/octet-stream"
            
            asyncio.run(self.node.execute())
            
            self.assertIsNotNone(self.node.true_path)
            attachment = self.node.true_path
            
            # Verify binary content is correctly encoded
            import base64
            decoded = base64.b64decode(attachment["content"])
            self.assertEqual(decoded, binary_data)
            
        finally:
            os.unlink(temp_path)

    def test_different_mime_types(self):
        """Test that different MIME types are handled correctly"""
        mime_types = [
            "application/pdf",
            "image/jpeg", 
            "application/zip",
            "text/csv"
        ]
        
        for mime_type in mime_types:
            with self.subTest(mime_type=mime_type):
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    f.write("test content")
                    temp_path = f.name
                
                try:
                    self.node.filepath = temp_path
                    self.node.mimetype = mime_type
                    self.node.true_path = None  # Reset
                    
                    asyncio.run(self.node.execute())
                    
                    self.assertIsNotNone(self.node.true_path)
                    self.assertEqual(self.node.true_path["mimetype"], mime_type)
                    
                finally:
                    os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()