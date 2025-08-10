from typing import Optional
from .base import EmailProvider
from .smtp import SMTPProvider
from .aws_ses import AWSSESProvider


class EmailProviderFactory:
    """Factory for creating email providers"""
    
    @staticmethod
    def create_smtp_provider(
        host: str,
        port: int,
        user: str,
        password: str,
        use_tls: bool = True,
        timeout: int = 30
    ) -> SMTPProvider:
        """Create SMTP provider"""
        return SMTPProvider(
            host=host,
            port=port,
            user=user,
            password=password,
            use_tls=use_tls,
            timeout=timeout
        )
    
    @staticmethod
    def create_aws_ses_provider(
        region: str = "us-east-1",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None
    ) -> AWSSESProvider:
        """Create AWS SES provider"""
        return AWSSESProvider(
            region=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    
    @staticmethod
    def create_provider(provider_type: str, **kwargs) -> EmailProvider:
        """Create provider by type"""
        if provider_type.lower() == "smtp":
            return EmailProviderFactory.create_smtp_provider(**kwargs)
        elif provider_type.lower() == "aws_ses":
            return EmailProviderFactory.create_aws_ses_provider(**kwargs)
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")