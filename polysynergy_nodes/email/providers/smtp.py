import smtplib
import asyncio
from email.message import EmailMessage as RawEmail
from typing import Optional

from .base import EmailProvider, EmailMessage, EmailResponse, EmailAddress


class SMTPProvider(EmailProvider):
    """SMTP email provider implementation"""
    
    def __init__(
        self, 
        host: str, 
        port: int, 
        user: str, 
        password: str, 
        use_tls: bool = True,
        timeout: int = 30
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_tls = use_tls
        self.timeout = timeout
    
    @property
    def name(self) -> str:
        return f"SMTP ({self.host}:{self.port})"
    
    @property
    def max_attachment_size(self) -> int:
        return 25 * 1024 * 1024  # 25MB
    
    @property
    def max_total_size(self) -> int:
        return 50 * 1024 * 1024  # 50MB
    
    async def validate_connection(self) -> bool:
        """Test SMTP connection without sending an email"""
        def _test_connection():
            try:
                server = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
                if self.use_tls:
                    server.starttls()
                server.login(self.user, self.password)
                server.quit()
                return True
            except Exception:
                return False
        
        return await asyncio.to_thread(_test_connection)
    
    async def send_email(self, email: EmailMessage) -> EmailResponse:
        """Send email via SMTP"""
        def _send():
            try:
                # Build email message
                msg = RawEmail()
                msg['Subject'] = email.subject
                msg['From'] = str(email.sender)
                msg['To'] = str(email.recipient)
                
                if email.cc:
                    msg['Cc'] = ', '.join(str(addr) for addr in email.cc)
                if email.bcc:
                    msg['Bcc'] = ', '.join(str(addr) for addr in email.bcc)
                
                # Set content
                msg.set_content(email.body, subtype="html" if email.is_html else "plain")
                
                # Add attachments
                for attachment in email.attachments:
                    maintype, subtype = attachment.mimetype.split("/", 1)
                    msg.add_attachment(
                        attachment.content,
                        maintype=maintype,
                        subtype=subtype,
                        filename=attachment.filename
                    )
                
                # Send email
                all_recipients = [email.recipient.email]
                all_recipients.extend(addr.email for addr in email.cc)
                all_recipients.extend(addr.email for addr in email.bcc)
                
                server = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
                try:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.user, self.password)
                    response = server.send_message(msg, to_addrs=all_recipients)
                    
                    return EmailResponse(
                        success=True,
                        message_id=msg.get('Message-ID'),
                        provider_response=response
                    )
                finally:
                    server.quit()
                    
            except Exception as e:
                return EmailResponse(
                    success=False,
                    error=str(e)
                )
        
        return await asyncio.to_thread(_send)