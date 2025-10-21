import httpx
import time
import os
import boto3
from typing import Optional, List

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(name="OAuth Client Credentials", category="auth", icon="oauth.svg")
class OAuthClientCredentials(Node):
    """OAuth 2.0 Client Credentials Grant flow node - for service-to-service authentication"""

    # Note: node_id is automatically available from the Node base class

    # Client credentials
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
        info="OAuth token endpoint URL (for Microsoft: https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token)"
    )

    scopes: list[str] = NodeVariableSettings(
        label="OAuth Scopes",
        dock=True,
        has_in=True,
        info="List of OAuth permission scopes. NOTE: Microsoft Client Credentials requires ONLY ['https://graph.microsoft.com/.default'] or ['api://YOUR_APP_ID/.default'] - individual scopes are not allowed!"
    )

    resource: str | None = NodeVariableSettings(
        label="Resource",
        dock=True,
        has_in=True,
        info="Resource parameter (optional, for older Microsoft endpoints)"
    )

    force_refresh: bool = NodeVariableSettings(
        label="Force Refresh Token",
        dock=dock_property(switch=True),
        has_in=True,
        default=False,
        info="Force request new token (ignore cached token in DynamoDB)"
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
        has_out=True,
        info="Token type (usually 'Bearer')"
    )

    expires_in: int | None = NodeVariableSettings(
        label="Expires In",
        dock=True,
        has_out=True,
        info="Token expiry time in seconds"
    )

    scopes_output: list[str] = NodeVariableSettings(
        label="Granted Scopes",
        dock=True,
        has_out=True,
        info="List of OAuth scopes that were requested"
    )

    # Path settings
    true_path: bool | str = PathSettings(
        label="Success",
        info="Triggered when token is successfully obtained"
    )

    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered when token request fails"
    )

    # Private attributes for token management
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
                # If DynamoDB is not available, skip token caching
                self._dynamodb_table = None
        return self._dynamodb_table

    async def _get_token_from_storage(self):
        """Get stored token from DynamoDB if available"""
        table = self._get_dynamodb_table()
        if table is None:
            return {}

        try:
            response = table.get_item(Key={"node_id": self.id})
            return response.get("Item", {})
        except Exception:
            return {}

    async def _save_token_to_storage(self):
        """Save token to DynamoDB if available"""
        table = self._get_dynamodb_table()
        if table is None:
            return

        try:
            # Use update instead of put to merge with existing record
            update_expression = "SET access_token = :at, token_type = :tt, grant_type = :gt"
            expression_values = {
                ":at": self.access_token,
                ":tt": self.token_type,
                ":gt": "client_credentials"
            }

            if self._expires_at:
                update_expression += ", token_expires = :te"
                expression_values[":te"] = self._expires_at

            if self.expires_in:
                update_expression += ", expires_in = :ei"
                expression_values[":ei"] = self.expires_in

            table.update_item(
                Key={"node_id": self.id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
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
        """Request a new token using client credentials"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        # Add scopes if provided (convert list to space-separated string)
        if self.scopes and len(self.scopes) > 0:
            data["scope"] = " ".join(self.scopes)

        # Add resource if provided (for older Microsoft endpoints)
        if self.resource:
            data["resource"] = self.resource

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
                    expires_in_raw = token_data.get("expires_in")
                    self.expires_in = int(expires_in_raw) if expires_in_raw is not None else None

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
            # Trim whitespace from string inputs
            if self.token_url:
                self.token_url = self.token_url.strip()
            if self.client_id:
                self.client_id = self.client_id.strip()
            if self.client_secret:
                self.client_secret = self.client_secret.strip()
            if self.resource:
                self.resource = self.resource.strip()

            # If force_refresh is enabled, skip cache and request new token
            if self.force_refresh:
                await self._request_new_token()
                self.scopes_output = self.scopes
                self.true_path = f"Bearer {self.access_token}" if self.access_token else None
                return

            # First, try to load existing token from storage
            token_data = await self._get_token_from_storage()

            if token_data:
                self.access_token = token_data.get("access_token")
                self._expires_at = token_data.get("token_expires")  # Updated field name
                self.token_type = token_data.get("token_type", "Bearer")
                expires_in_raw = token_data.get("expires_in")
                self.expires_in = int(expires_in_raw) if expires_in_raw is not None else None

            # Check if current token is valid
            if self._is_token_valid():
                self.scopes_output = self.scopes
                self.true_path = f"Bearer {self.access_token}"
                return

            # Token is expired or missing, request a new one
            await self._request_new_token()
            self.scopes_output = self.scopes
            self.true_path = f"Bearer {self.access_token}" if self.access_token else None

        except Exception as e:
            self.false_path = NodeError.format(e)