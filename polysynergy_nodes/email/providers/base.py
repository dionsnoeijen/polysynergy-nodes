from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class EmailAddress:
    """Represents an email address with optional name"""
    email: str
    name: Optional[str] = None
    
    def __str__(self):
        if self.name:
            return f"{self.name} <{self.email}>"
        return self.email


@dataclass
class EmailAttachment:
    """Represents an email attachment"""
    filename: str
    content: bytes
    mimetype: str
    size: int


@dataclass
class EmailMessage:
    """Represents an email message"""
    sender: EmailAddress
    recipient: EmailAddress
    cc: List[EmailAddress]
    bcc: List[EmailAddress] 
    subject: str
    body: str
    is_html: bool
    attachments: List[EmailAttachment]


@dataclass
class EmailResponse:
    """Response from email provider"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    provider_response: Optional[Dict] = None


class EmailProvider(ABC):
    """Abstract base class for email providers"""
    
    @abstractmethod
    async def send_email(self, email: EmailMessage) -> EmailResponse:
        """Send an email message"""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate that the provider connection is working"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass
    
    @property
    @abstractmethod
    def max_attachment_size(self) -> int:
        """Maximum attachment size in bytes"""
        pass
    
    @property
    @abstractmethod
    def max_total_size(self) -> int:
        """Maximum total email size in bytes"""
        pass