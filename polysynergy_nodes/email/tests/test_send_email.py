import unittest
import asyncio
import os
import base64
from unittest.mock import patch, MagicMock
from polysynergy_nodes.email.send_email import SendEmail

class TestSendEmailNode(unittest.TestCase):

    def setUp(self):
        self.node = SendEmail()
        self.node.true_path = False
        self.node.false_path = False
        self.node.smtp_host = "smtp.example.com"
        self.node.smtp_port = 587
        self.node.smtp_user = "user@example.com"
        self.node.smtp_password = "securepassword"
        self.node.smtp_use_tls = True
        self.node.sender = "Sender <sender@example.com>"
        self.node.recipient = "recipient@example.com"
        self.node.subject = "Test Subject"
        self.node.body = "<p>This is a test email.</p>"
        self.node.cc = ""
        self.node.bcc = ""
        self.node.is_html = True

    @patch("polysynergy_nodes.email.send_email.smtplib.SMTP")
    def test_smtp_send_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_server.send_message.return_value = {}

        asyncio.run(self.node.execute())

        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)
        mock_server.send_message.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "securepassword")
        mock_server.quit.assert_called_once()

    def test_missing_smtp_config(self):
        self.node.smtp_host = None
        self.node.smtp_user = None
        self.node.smtp_password = None

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("SMTP config missing", str(self.node.false_path))

    def test_invalid_recipient_email(self):
        self.node.recipient = "invalid-email"

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("Invalid recipient email", str(self.node.false_path))

    def test_invalid_cc_email(self):
        self.node.cc = "valid@example.com,invalid-email"

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("Invalid email addresses", str(self.node.false_path))

    def test_subject_too_long(self):
        self.node.subject = "x" * 1000  # Too long

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("Subject line too long", str(self.node.false_path))

    def test_body_too_long(self):
        self.node.body = "x" * 1000001  # Too long

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("Email body too long", str(self.node.false_path))

    @patch("polysynergy_nodes.email.send_email.smtplib.SMTP")
    def test_smtp_with_cc_bcc(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_server.send_message.return_value = {}
        
        self.node.cc = "cc1@example.com, cc2@example.com"
        self.node.bcc = "bcc@example.com"

        asyncio.run(self.node.execute())

        self.assertTrue(self.node.true_path)
        mock_server.send_message.assert_called_once()

    def test_attachment_validation(self):
        # Create a large attachment (over 25MB encoded)
        large_content = base64.b64encode(b"x" * (26 * 1024 * 1024)).decode("utf-8")
        self.node.attachments = [{
            "filename": "large.txt",
            "content": large_content,
            "mimetype": "text/plain"
        }]

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("exceeds 25MB limit", str(self.node.false_path))

    @patch("polysynergy_nodes.email.send_email.smtplib.SMTP")
    def test_smtp_connection_error(self, mock_smtp):
        mock_smtp.side_effect = Exception("Connection failed")

        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)
        self.assertIn("Connection failed", str(self.node.false_path))

    def test_email_validation_method(self):
        # Test the validate_email method directly
        self.assertTrue(self.node.validate_email("test@example.com"))
        self.assertTrue(self.node.validate_email("user.name+tag@domain.co.uk"))
        self.assertFalse(self.node.validate_email("invalid-email"))
        self.assertFalse(self.node.validate_email("@example.com"))
        self.assertFalse(self.node.validate_email("test@"))

    def test_parse_email_list_method(self):
        # Test valid email list
        emails = self.node.parse_email_list("test1@example.com, test2@example.com")
        self.assertEqual(emails, ["test1@example.com", "test2@example.com"])
        
        # Test empty list
        emails = self.node.parse_email_list("")
        self.assertEqual(emails, [])
        
        # Test invalid emails in list
        with self.assertRaises(ValueError) as context:
            self.node.parse_email_list("valid@example.com, invalid-email")
        self.assertIn("Invalid email addresses", str(context.exception))

if __name__ == "__main__":
    unittest.main()