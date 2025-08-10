import base64
import re
from typing import List, Optional

from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from .providers.base import EmailAddress, EmailMessage, EmailAttachment as EmailAttachmentData
from .providers.factory import EmailProviderFactory


@node(
    'Send Email Enhanced',
    'email',
    icon='email.svg',
)
class SendEmailEnhanced(Node):
    # Provider selection
    provider_type: str = NodeVariableSettings(
        label="Provider",
        dock=dock_property(
            select_values={
                "smtp": "SMTP Server",
                "aws_ses": "AWS Simple Email Service"
            }
        ),
        has_in=True,
        default="smtp"
    )
    
    # SMTP Configuration
    smtp_host: str = NodeVariableSettings(label="SMTP Host", dock=True, has_in=True, default="")
    smtp_port: int = NodeVariableSettings(label="SMTP Port", dock=True, has_in=True, default=587)
    smtp_user: str = NodeVariableSettings(label="SMTP User", dock=True, has_in=True, default="")
    smtp_password: str = NodeVariableSettings(
        label="SMTP Password",
        dock=dock_property(
            enabled=False,
            info="Connect a secret (node) to set this value."
        ),
        has_in=True,
        default=""
    )
    smtp_use_tls: bool = NodeVariableSettings(label="Use TLS", dock=dock_property(switch=True), default=True)
    smtp_timeout: int = NodeVariableSettings(label="Timeout (seconds)", dock=True, has_in=True, default=30)
    
    # AWS SES Configuration  
    aws_region: str = NodeVariableSettings(label="AWS Region", dock=True, has_in=True, default="us-east-1")
    aws_access_key_id: str = NodeVariableSettings(
        label="AWS Access Key ID",
        dock=dock_property(
            enabled=False,
            info="Optional - uses IAM role if not provided"
        ),
        has_in=True,
        default=""
    )
    aws_secret_access_key: str = NodeVariableSettings(
        label="AWS Secret Access Key", 
        dock=dock_property(
            enabled=False,
            info="Optional - uses IAM role if not provided"
        ),
        has_in=True,
        default=""
    )

    # Email content
    sender: str = NodeVariableSettings(
        label="From",
        dock=dock_property(info='Sender email address, e.g.: Example <no-reply@example.com>'),
        has_in=True,
        default="Example <no-reply@example.com>"
    )
    recipient: str = NodeVariableSettings(label="To", dock=True, has_in=True)
    cc: str = NodeVariableSettings(label="CC", dock=True, has_in=True, default="")
    bcc: str = NodeVariableSettings(label="BCC", dock=True, has_in=True, default="")
    subject: str = NodeVariableSettings(label="Subject", dock=True, has_in=True)
    body: str = NodeVariableSettings(
        label="Body", 
        dock=dock_text_area(info='Email body content. For HTML, set "Is HTML" to true.'), 
        has_in=True
    )
    is_html: bool = NodeVariableSettings(label="Is HTML?", dock=dock_property(switch=True), default=True)

    attachments: list[dict] | dict | None = NodeVariableSettings(
        label="Attachments",
        has_in=True,
        default=None,
        info="Dict or list of dicts with 'filename', 'content' (base64), and optional 'mimetype'"
    )

    # Output
    message_id: str = NodeVariableSettings(
        label="Message ID",
        info="Email message ID from provider",
        has_out=True
    )
    
    provider_used: str = NodeVariableSettings(
        label="Provider Used",
        info="Which email provider was used",
        has_out=True
    )

    true_path: bool = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    def validate_email(self, email: str) -> bool:
        """Validate email address format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))

    def parse_email_address(self, email_str: str) -> EmailAddress:
        """Parse email string into EmailAddress object"""
        email_str = email_str.strip()
        
        # Check for "Name <email@domain.com>" format
        if '<' in email_str and '>' in email_str:
            parts = email_str.split('<')
            name = parts[0].strip().strip('"\'')
            email = parts[1].strip().rstrip('>')
            return EmailAddress(email=email, name=name if name else None)
        else:
            return EmailAddress(email=email_str)

    def parse_email_list(self, email_string: str) -> List[EmailAddress]:
        """Parse comma-separated email addresses"""
        if not email_string or not email_string.strip():
            return []
        
        addresses = []
        for email_str in email_string.split(','):
            email_str = email_str.strip()
            if email_str:
                addr = self.parse_email_address(email_str)
                if not self.validate_email(addr.email):
                    raise ValueError(f"Invalid email address: {addr.email}")
                addresses.append(addr)
        
        return addresses

    def process_attachments(self, attachments_input) -> List[EmailAttachmentData]:
        """Process and validate attachments"""
        if not attachments_input:
            return []
        
        # Convert to list if single dict
        if isinstance(attachments_input, dict):
            attachments_input = [attachments_input]
        elif not isinstance(attachments_input, list):
            raise ValueError("Attachments must be a list of dicts or a single dict.")
        
        processed_attachments = []
        total_size = 0
        
        for att in attachments_input:
            filename = att.get("filename", "attachment")
            content_b64 = att.get("content")
            mimetype = att.get("mimetype", "application/octet-stream")
            
            if not content_b64:
                raise ValueError(f"Attachment '{filename}' has no content.")
            
            try:
                content_bytes = base64.b64decode(content_b64)
                size = len(content_bytes)
                
                # Size validation will be done by provider
                processed_attachments.append(EmailAttachmentData(
                    filename=filename,
                    content=content_bytes,
                    mimetype=mimetype,
                    size=size
                ))
                
                total_size += size
                
            except Exception as e:
                raise ValueError(f"Invalid attachment content for '{filename}': {str(e)}")
        
        return processed_attachments

    async def execute(self):
        try:
            # Parse email addresses
            sender_addr = self.parse_email_address(self.sender)
            recipient_addr = self.parse_email_address(self.recipient)
            cc_addrs = self.parse_email_list(self.cc)
            bcc_addrs = self.parse_email_list(self.bcc)
            
            # Validate required fields
            if not self.validate_email(recipient_addr.email):
                raise ValueError(f"Invalid recipient email: {recipient_addr.email}")
            
            if not self.validate_email(sender_addr.email):
                raise ValueError(f"Invalid sender email: {sender_addr.email}")
            
            # Validate content lengths
            if len(self.subject) > 998:
                raise ValueError("Subject line too long (max 998 characters)")
            
            if len(self.body) > 1000000:
                raise ValueError("Email body too long (max 1MB)")
            
            # Process attachments
            attachments = self.process_attachments(self.attachments)
            
            # Create email message
            email_message = EmailMessage(
                sender=sender_addr,
                recipient=recipient_addr,
                cc=cc_addrs,
                bcc=bcc_addrs,
                subject=self.subject,
                body=self.body,
                is_html=self.is_html,
                attachments=attachments
            )
            
            # Create provider
            if self.provider_type == "smtp":
                if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
                    raise ValueError("SMTP configuration missing (host, user, password required)")
                
                provider = EmailProviderFactory.create_smtp_provider(
                    host=self.smtp_host,
                    port=self.smtp_port,
                    user=self.smtp_user,
                    password=self.smtp_password,
                    use_tls=self.smtp_use_tls,
                    timeout=self.smtp_timeout
                )
            elif self.provider_type == "aws_ses":
                provider = EmailProviderFactory.create_aws_ses_provider(
                    region=self.aws_region,
                    aws_access_key_id=self.aws_access_key_id if self.aws_access_key_id else None,
                    aws_secret_access_key=self.aws_secret_access_key if self.aws_secret_access_key else None
                )
            else:
                raise ValueError(f"Unsupported provider type: {self.provider_type}")
            
            # Validate attachment sizes against provider limits
            if attachments:
                total_size = sum(att.size for att in attachments)
                max_attachment_size = provider.max_attachment_size
                max_total_size = provider.max_total_size
                
                for att in attachments:
                    if att.size > max_attachment_size:
                        raise ValueError(
                            f"Attachment '{att.filename}' ({att.size} bytes) exceeds "
                            f"provider limit of {max_attachment_size} bytes"
                        )
                
                if total_size > max_total_size:
                    raise ValueError(
                        f"Total attachment size ({total_size} bytes) exceeds "
                        f"provider limit of {max_total_size} bytes"
                    )
            
            # Send email
            response = await provider.send_email(email_message)
            
            if response.success:
                self.message_id = response.message_id or ""
                self.provider_used = provider.name
                self.true_path = True
            else:
                raise Exception(response.error or "Unknown email sending error")
                
        except Exception as e:
            self.false_path = NodeError.format(e, True)
            self.message_id = ""
            self.provider_used = ""