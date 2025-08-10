import unittest
import asyncio
from unittest.mock import patch, MagicMock

from polysynergy_nodes.email.providers.base import EmailAddress, EmailMessage, EmailAttachment
from polysynergy_nodes.email.providers.smtp import SMTPProvider
from polysynergy_nodes.email.providers.aws_ses import AWSSESProvider
from polysynergy_nodes.email.providers.factory import EmailProviderFactory


class TestEmailProviders(unittest.TestCase):

    def setUp(self):
        self.sender = EmailAddress("sender@example.com", "Test Sender")
        self.recipient = EmailAddress("recipient@example.com")
        self.email_message = EmailMessage(
            sender=self.sender,
            recipient=self.recipient,
            cc=[],
            bcc=[],
            subject="Test Subject",
            body="Test Body",
            is_html=False,
            attachments=[]
        )

    @patch("polysynergy_nodes.email.providers.smtp.smtplib.SMTP")
    def test_smtp_provider_send_success(self, mock_smtp):
        """Test successful SMTP send"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_server.send_message.return_value = {}

        provider = SMTPProvider(
            host="smtp.example.com",
            port=587,
            user="user@example.com",
            password="password"
        )

        response = asyncio.run(provider.send_email(self.email_message))
        
        self.assertTrue(response.success)
        self.assertIsNone(response.error)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "password")
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch("polysynergy_nodes.email.providers.smtp.smtplib.SMTP")
    def test_smtp_provider_send_error(self, mock_smtp):
        """Test SMTP send with error"""
        mock_smtp.side_effect = Exception("Connection failed")

        provider = SMTPProvider(
            host="smtp.example.com",
            port=587,
            user="user@example.com",
            password="password"
        )

        response = asyncio.run(provider.send_email(self.email_message))
        
        self.assertFalse(response.success)
        self.assertIn("Connection failed", response.error)

    @patch("polysynergy_nodes.email.providers.smtp.smtplib.SMTP")
    def test_smtp_provider_validate_connection(self, mock_smtp):
        """Test SMTP connection validation"""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        provider = SMTPProvider(
            host="smtp.example.com",
            port=587,
            user="user@example.com",
            password="password"
        )

        is_valid = asyncio.run(provider.validate_connection())
        
        self.assertTrue(is_valid)
        mock_server.login.assert_called_once()
        mock_server.quit.assert_called_once()

    def test_smtp_provider_properties(self):
        """Test SMTP provider properties"""
        provider = SMTPProvider(
            host="smtp.example.com",
            port=587,
            user="user@example.com",
            password="password"
        )
        
        self.assertEqual(provider.name, "SMTP (smtp.example.com:587)")
        self.assertEqual(provider.max_attachment_size, 25 * 1024 * 1024)
        self.assertEqual(provider.max_total_size, 50 * 1024 * 1024)

    @patch("polysynergy_nodes.email.providers.aws_ses.boto3")
    def test_aws_ses_provider_send_success(self, mock_boto3):
        """Test successful AWS SES send"""
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.send_email.return_value = {'MessageId': 'test-message-id'}

        provider = AWSSESProvider(region="us-east-1")

        response = asyncio.run(provider.send_email(self.email_message))
        
        self.assertTrue(response.success)
        self.assertEqual(response.message_id, 'test-message-id')
        mock_client.send_email.assert_called_once()

    @patch("polysynergy_nodes.email.providers.aws_ses.boto3")
    def test_aws_ses_provider_with_attachments(self, mock_boto3):
        """Test AWS SES with attachments uses raw email"""
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.send_raw_email.return_value = {'MessageId': 'test-message-id'}

        # Add attachment to email
        attachment = EmailAttachment(
            filename="test.txt",
            content=b"test content",
            mimetype="text/plain",
            size=12
        )
        self.email_message.attachments = [attachment]

        provider = AWSSESProvider(region="us-east-1")
        response = asyncio.run(provider.send_email(self.email_message))
        
        self.assertTrue(response.success)
        mock_client.send_raw_email.assert_called_once()

    def test_aws_ses_provider_properties(self):
        """Test AWS SES provider properties"""
        provider = AWSSESProvider(region="eu-west-1")
        
        self.assertEqual(provider.name, "AWS SES (eu-west-1)")
        self.assertEqual(provider.max_attachment_size, 10 * 1024 * 1024)
        self.assertEqual(provider.max_total_size, 10 * 1024 * 1024)

    def test_email_provider_factory(self):
        """Test email provider factory"""
        # Test SMTP provider creation
        smtp_provider = EmailProviderFactory.create_provider(
            "smtp",
            host="smtp.example.com",
            port=587,
            user="user@example.com",
            password="password"
        )
        self.assertIsInstance(smtp_provider, SMTPProvider)
        
        # Test AWS SES provider creation
        ses_provider = EmailProviderFactory.create_provider(
            "aws_ses",
            region="us-west-2"
        )
        self.assertIsInstance(ses_provider, AWSSESProvider)
        
        # Test invalid provider type
        with self.assertRaises(ValueError) as context:
            EmailProviderFactory.create_provider("invalid_provider")
        self.assertIn("Unknown provider type", str(context.exception))

    def test_email_address_str_representation(self):
        """Test EmailAddress string representation"""
        # Test with name
        addr_with_name = EmailAddress("test@example.com", "Test User")
        self.assertEqual(str(addr_with_name), "Test User <test@example.com>")
        
        # Test without name
        addr_without_name = EmailAddress("test@example.com")
        self.assertEqual(str(addr_without_name), "test@example.com")


if __name__ == "__main__":
    unittest.main()