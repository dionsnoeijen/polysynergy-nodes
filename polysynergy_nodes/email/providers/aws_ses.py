import boto3
import asyncio
from typing import Dict, Optional
from botocore.exceptions import ClientError

from .base import EmailProvider, EmailMessage, EmailResponse


class AWSSESProvider(EmailProvider):
    """AWS SES email provider implementation"""
    
    def __init__(
        self, 
        region: str = "us-east-1",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None
    ):
        self.region = region
        
        # Initialize SES client
        if aws_access_key_id and aws_secret_access_key:
            self.ses_client = boto3.client(
                'ses',
                region_name=region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        else:
            # Use default credentials (IAM role, environment variables, etc.)
            self.ses_client = boto3.client('ses', region_name=region)
    
    @property
    def name(self) -> str:
        return f"AWS SES ({self.region})"
    
    @property
    def max_attachment_size(self) -> int:
        return 10 * 1024 * 1024  # 10MB per SES limits
    
    @property
    def max_total_size(self) -> int:
        return 10 * 1024 * 1024  # 10MB total per SES limits
    
    async def validate_connection(self) -> bool:
        """Test SES connection by getting send quota"""
        def _test_connection():
            try:
                self.ses_client.get_send_quota()
                return True
            except Exception:
                return False
        
        return await asyncio.to_thread(_test_connection)
    
    async def send_email(self, email: EmailMessage) -> EmailResponse:
        """Send email via AWS SES"""
        def _send():
            try:
                # Prepare destination
                destination = {'ToAddresses': [email.recipient.email]}
                
                if email.cc:
                    destination['CcAddresses'] = [addr.email for addr in email.cc]
                if email.bcc:
                    destination['BccAddresses'] = [addr.email for addr in email.bcc]
                
                # If we have attachments, use raw email
                if email.attachments:
                    return self._send_raw_email(email)
                
                # Simple email without attachments
                message = {
                    'Subject': {'Data': email.subject, 'Charset': 'UTF-8'},
                    'Body': {}
                }
                
                if email.is_html:
                    message['Body']['Html'] = {'Data': email.body, 'Charset': 'UTF-8'}
                else:
                    message['Body']['Text'] = {'Data': email.body, 'Charset': 'UTF-8'}
                
                response = self.ses_client.send_email(
                    Source=email.sender.email,
                    Destination=destination,
                    Message=message
                )
                
                return EmailResponse(
                    success=True,
                    message_id=response['MessageId'],
                    provider_response=response
                )
                
            except ClientError as e:
                return EmailResponse(
                    success=False,
                    error=str(e)
                )
        
        return await asyncio.to_thread(_send)
    
    def _send_raw_email(self, email: EmailMessage) -> EmailResponse:
        """Send raw email with attachments via SES"""
        try:
            from email.message import EmailMessage as RawEmail
            import base64
            
            # Build raw email message
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
            
            # Get all recipients
            destinations = [email.recipient.email]
            destinations.extend(addr.email for addr in email.cc)
            destinations.extend(addr.email for addr in email.bcc)
            
            response = self.ses_client.send_raw_email(
                Source=email.sender.email,
                Destinations=destinations,
                RawMessage={'Data': msg.as_string()}
            )
            
            return EmailResponse(
                success=True,
                message_id=response['MessageId'],
                provider_response=response
            )
            
        except Exception as e:
            return EmailResponse(
                success=False,
                error=str(e)
            )