import unittest
import os
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

    @patch.dict(os.environ, {"AWS_LAMBDA_FUNCTION_NAME": "true"})
    @patch("polysynergy_nodes.email.send_email.smtplib.SMTP")
    def test_lambda_smtp_send(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)
        mock_server.sendmail.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    @patch("polysynergy_nodes.email.send_email.EmailMessage")
    @patch("polysynergy_nodes.email.send_email.get_connection")
    def test_local_send_email(self, mock_get_connection, mock_email_message):
        mock_conn = MagicMock()
        mock_get_connection.return_value = mock_conn

        mock_email = MagicMock()
        mock_email_message.return_value = mock_email

        self.node.execute()

        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)
        mock_email.send.assert_called_once()

    @patch.dict(os.environ, {"AWS_LAMBDA_FUNCTION_NAME": "true"})
    def test_missing_smtp_config_in_lambda(self):
        self.node.smtp_host = None
        self.node.smtp_user = None
        self.node.smtp_password = None

        self.node.execute()

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()