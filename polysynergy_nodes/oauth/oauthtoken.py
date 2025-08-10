import httpx
import time
import os
import boto3
from typing import Optional

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="OAuth 2.0 Token", category="auth", icon="oauth.svg")
class OAuthToken(Node):
    # Input parameters
    service_name: str = NodeVariableSettings(
        label="Service Name", 
        dock=True, 
        has_in=True, 
        required=True,
        info="Unique identifier for this OAuth service (used for token storage)"
    )
    client_id: str = NodeVariableSettings(
        label="Client ID", 
        dock=True, 
        has_in=True, 
        required=True,
        info="OAuth client identifier"
    )
    client_secret: str = NodeVariableSettings(
        label="Client Secret", 
        dock=True, 
        has_in=True, 
        required=True,
        info="OAuth client secret"
    )
    token_url: str = NodeVariableSettings(
        label="Token URL", 
        dock=True, 
        has_in=True, 
        required=True,
        info="OAuth token endpoint URL"
    )
    grant_type: str = NodeVariableSettings(
        label="Grant Type",
        dock=True,
        has_in=True,
        default="client_credentials",
        info="OAuth grant type (client_credentials or refresh_token)"
    )
    scope: Optional[str] = NodeVariableSettings(
        label="Scope",
        dock=True,
        has_in=True,
        info="OAuth scope (optional)"
    )

    # Output parameters
    access_token: str = NodeVariableSettings(
        label="Access Token", 
        dock=True, 
        has_out=True,
        info="Valid OAuth access token"
    )
    token_type: str = NodeVariableSettings(
        label="Token Type",
        dock=True,
        has_out=True,
        info="Token type (usually 'Bearer')"
    )
    expires_in: Optional[int] = NodeVariableSettings(
        label="Expires In",
        dock=True,
        has_out=True,
        info="Token expiry time in seconds"
    )

    # Path settings
    true_path: bool | str = PathSettings(
        label="Success",
        info="Triggered when token is successfully obtained. Contains access token."
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered when token request fails. Contains error details."
    )

    # Private attributes for token management
    _refresh_token: Optional[str] = None
    _expires_at: Optional[float] = None
    _dynamodb_table = None

    def _get_dynamodb_table(self):
        """Lazy initialization of DynamoDB table"""
        if self._dynamodb_table is None:
            try:
                dynamodb = boto3.resource(
                    "dynamodb",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=os.getenv("AWS_REGION", "eu-central-1"),
                )
                self._dynamodb_table = dynamodb.Table("OAuthTokens")
            except Exception:
                # If DynamoDB is not available, we'll just skip token caching
                self._dynamodb_table = None
        return self._dynamodb_table

    async def _get_token_from_storage(self):
        """Get stored token from DynamoDB if available"""
        table = self._get_dynamodb_table()
        if table is None:
            return {}
        
        try:
            response = table.get_item(Key={"service_name": self.service_name})
            return response.get("Item", {})
        except Exception:
            return {}

    async def _save_token_to_storage(self):
        """Save token to DynamoDB if available"""
        table = self._get_dynamodb_table()
        if table is None:
            return
        
        try:
            table.put_item(Item={
                "service_name": self.service_name,
                "access_token": self.access_token,
                "refresh_token": self._refresh_token,
                "expires_at": self._expires_at,
                "token_type": self.token_type,
                "expires_in": self.expires_in
            })
        except Exception:
            # Silently fail if DynamoDB is not available
            pass

    def _is_token_valid(self):
        """Check if current token is still valid"""
        if not self.access_token:
            return False
        if self._expires_at is None:
            return True  # Assume valid if no expiry info
        return self._expires_at > time.time() + 60  # 60 second buffer

    async def _request_new_token(self):
        """Request a new token using the specified grant type"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
        }

        # Add scope if provided
        if self.scope:
            data["scope"] = self.scope

        # Add grant-type specific parameters
        if self.grant_type == "refresh_token" and self._refresh_token:
            data["refresh_token"] = self._refresh_token
        elif self.grant_type == "client_credentials":
            # Client credentials flow - no additional parameters needed
            pass
        else:
            raise ValueError(f"Unsupported grant type: {self.grant_type}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0
                )

                if response.status_code == 200:
                    token_data = response.json()
                    
                    # Update token information
                    self.access_token = token_data.get("access_token")
                    self.token_type = token_data.get("token_type", "Bearer")
                    self.expires_in = token_data.get("expires_in")
                    
                    # Update refresh token if provided
                    if "refresh_token" in token_data:
                        self._refresh_token = token_data["refresh_token"]
                    
                    # Calculate expiry time
                    if self.expires_in:
                        self._expires_at = time.time() + self.expires_in
                    
                    # Save to storage
                    await self._save_token_to_storage()
                    
                    return True
                else:
                    error_text = response.text
                    try:
                        error_data = response.json()
                        error_text = error_data.get("error_description", error_data.get("error", error_text))
                    except:
                        pass
                    
                    raise Exception(f"Token request failed ({response.status_code}): {error_text}")
                    
        except httpx.RequestError as e:
            raise Exception(f"Network error during token request: {str(e)}")

    async def execute(self):
        try:
            # First, try to load existing token from storage
            token_data = await self._get_token_from_storage()
            
            if token_data:
                self.access_token = token_data.get("access_token")
                self._refresh_token = token_data.get("refresh_token")
                self._expires_at = token_data.get("expires_at")
                self.token_type = token_data.get("token_type", "Bearer")
                self.expires_in = token_data.get("expires_in")

            # Check if current token is valid
            if self._is_token_valid():
                self.true_path = self.access_token
                return

            # Token is expired or missing, request a new one
            await self._request_new_token()
            self.true_path = self.access_token

        except Exception as e:
            self.false_path = NodeError.format(e)