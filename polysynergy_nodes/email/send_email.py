import smtplib
import base64
import asyncio
import re
from email.message import EmailMessage as RawEmail

from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    'Send Email',
    'email',
    icon='email.svg',
)
class SendEmail(Node):
    smtp_host: str = NodeVariableSettings(label="Host", dock=True, has_in=True)
    smtp_port: int = NodeVariableSettings(label="Port", dock=True, has_in=True, default=587)
    smtp_user: str = NodeVariableSettings(label="User", dock=True, has_in=True)
    smtp_password: str = NodeVariableSettings(
        label="SMTP Password",
        dock=dock_property(
            enabled=False,
            info="Connect a secret (node) to set this value."
        ),
        has_in=True,
    )
    smtp_use_tls: bool = NodeVariableSettings(label="Use TLS", dock=dock_property(switch=True), default=True)
    smtp_timeout: int = NodeVariableSettings(label="Timeout (seconds)", dock=True, has_in=True, default=30)

    sender: str = NodeVariableSettings(
        label="From",
        dock=dock_property(info='Sender email address, something like: Example <no-reply@example.com>'),
        has_in=True,
        default="Example <no-reply@example.com>"
    )
    recipient: str = NodeVariableSettings(label="To", dock=True, has_in=True)
    cc: str = NodeVariableSettings(label="CC", dock=True, has_in=True, default="")
    bcc: str = NodeVariableSettings(label="BCC", dock=True, has_in=True, default="")
    subject: str = NodeVariableSettings(label="Subject", dock=True, has_in=True)
    body: str = NodeVariableSettings(label="Body", dock=dock_text_area(info='For a html body, connect a template node.'), has_in=True)
    is_html: bool = NodeVariableSettings(label="Is HTML?", dock=dock_property(switch=True), default=True)

    attachments: list[dict] | dict | None = NodeVariableSettings(
        label="Attachments",
        has_in=True,
        default=None,
        info="Dict or list of dicts with 'filename', 'content' (base64), and optional 'mimetype'"
    )

    true_path: bool = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    def validate_email(self, email: str) -> bool:
        """Validate email address format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))

    def parse_email_list(self, email_string: str) -> list[str]:
        """Parse comma-separated email addresses and validate them"""
        if not email_string or not email_string.strip():
            return []
        
        emails = [email.strip() for email in email_string.split(',')]
        invalid_emails = [email for email in emails if not self.validate_email(email)]
        
        if invalid_emails:
            raise ValueError(f"Invalid email addresses: {', '.join(invalid_emails)}")
        
        return emails

    def validate_attachment_size(self, attachments: list[dict]) -> None:
        """Validate attachment sizes (limit to 25MB per attachment, 50MB total)"""
        max_attachment_size = 25 * 1024 * 1024  # 25MB
        max_total_size = 50 * 1024 * 1024  # 50MB
        total_size = 0
        
        for att in attachments:
            content_b64 = att.get("content", "")
            # Base64 encoded size is ~4/3 of original, so decode to get actual size
            try:
                decoded_size = len(base64.b64decode(content_b64))
                if decoded_size > max_attachment_size:
                    filename = att.get("filename", "unknown")
                    raise ValueError(f"Attachment '{filename}' exceeds 25MB limit")
                total_size += decoded_size
            except Exception as e:
                raise ValueError(f"Invalid attachment content: {str(e)}")
        
        if total_size > max_total_size:
            raise ValueError("Total attachment size exceeds 50MB limit")

    async def execute(self):
        try:
            # Validate SMTP configuration
            if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
                raise ValueError("SMTP config missing.")
            
            # Validate email addresses
            if not self.validate_email(self.recipient):
                raise ValueError(f"Invalid recipient email: {self.recipient}")
            
            # Validate optional email lists
            cc_list = self.parse_email_list(self.cc)
            bcc_list = self.parse_email_list(self.bcc)
            
            # Validate content lengths
            if len(self.subject) > 998:  # RFC 5322 limit
                raise ValueError("Subject line too long (max 998 characters)")
            
            if len(self.body) > 1000000:  # 1MB limit for email body
                raise ValueError("Email body too long (max 1MB)")

            # Process attachments
            attachments = self.attachments or []
            if isinstance(attachments, dict):
                attachments = [attachments]
            elif not isinstance(attachments, list):
                raise ValueError("Attachments must be a list of dicts or a single dict.")

            # Validate attachments
            if attachments:
                self.validate_attachment_size(attachments)

            # Build email message in thread to avoid blocking
            def _build_message():
                msg = RawEmail()
                msg['Subject'] = self.subject
                msg['From'] = self.sender
                msg['To'] = self.recipient
                
                if cc_list:
                    msg['Cc'] = ', '.join(cc_list)
                if bcc_list:
                    msg['Bcc'] = ', '.join(bcc_list)

                # Set email content
                msg.set_content(self.body, subtype="html" if self.is_html else "plain")

                # Add attachments
                for att in attachments:
                    filename = att.get("filename", "attachment")
                    content_b64 = att.get("content")
                    mimetype = att.get("mimetype", "application/octet-stream")
                    
                    if not content_b64:
                        raise ValueError(f"Attachment '{filename}' has no content.")
                    
                    data = base64.b64decode(content_b64)
                    maintype, subtype = mimetype.split("/", 1)
                    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

                return msg

            # Build message asynchronously
            msg = await asyncio.to_thread(_build_message)

            # Send email asynchronously
            def _send_email():
                all_recipients = [self.recipient] + cc_list + bcc_list
                
                server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=self.smtp_timeout)
                try:
                    if self.smtp_use_tls:
                        server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    response = server.send_message(msg, to_addrs=all_recipients)
                    return response
                finally:
                    server.quit()

            # Send email in thread pool
            response = await asyncio.to_thread(_send_email)
            print("SMTP RESPONSE:", response)

            self.true_path = True

        except Exception as e:
            self.false_path = NodeError.format(e, True)