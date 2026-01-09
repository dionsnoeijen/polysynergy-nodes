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


@node(name="OAuth Refresh Token", category="auth", icon="lock.svg")
class OAuthRefreshToken(Node):
    """OAuth 2.0 Refresh Token Grant flow node - for renewing access tokens"""

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
        info="OAuth token endpoint URL"
    )

    refresh_token: str = NodeVariableSettings(
        label="Refresh Token",
        dock=True,
        has_in=True,
        required=True,
        info="Refresh token to use for obtaining new access token"
    )

    scope: Optional[str] = NodeVariableSettings(
        label="Scope",
        dock=True,
        has_in=True,
        info="OAuth scope (optional, some providers require it)"
    )

    # Output parameters
    access_token: str = NodeVariableSettings(
        label="Access Token",
        dock=True,
        has_out=True,
        info="New OAuth access token"
    )

    new_refresh_token: Optional[str] = NodeVariableSettings(
        label="New Refresh Token",
        dock=True,
        has_out=True,
        info="New refresh token (if provider issues one)"
    )

    token_type: str = NodeVariableSettings(
        label="Token Type",
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
        info="Triggered when token is successfully refreshed"
    )

    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered when token refresh fails"
    )

    # Private attributes
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

    async def _save_token_to_storage(self):
        """Save token to DynamoDB if available"""
        table = self._get_dynamodb_table()
        if table is None:
            return

        try:
            # Use the new refresh token if provided, otherwise keep the old one
            refresh_token_to_store = self.new_refresh_token or self.refresh_token

            # Use update instead of put to merge with existing record
            update_expression = "SET access_token = :at, refresh_token = :rt, token_type = :tt, grant_type = :gt"
            expression_values = {
                ":at": self.access_token,
                ":rt": refresh_token_to_store,
                ":tt": self.token_type,
                ":gt": "refresh_token"
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

    async def _refresh_access_token(self):
        """Use refresh token to get new access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        # Add scope if provided
        if self.scope:
            data["scope"] = self.scope

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

                    # Some providers issue a new refresh token
                    if "refresh_token" in token_data:
                        self.new_refresh_token = token_data["refresh_token"]

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

                    raise Exception(f"Token refresh failed ({response.status_code}): {error_text}")

        except httpx.RequestError as e:
            raise Exception(f"Network error during token refresh: {str(e)}")

    async def execute(self):
        try:
            # Trim whitespace from string inputs
            if self.token_url:
                self.token_url = self.token_url.strip()
            if self.client_id:
                self.client_id = self.client_id.strip()
            if self.client_secret:
                self.client_secret = self.client_secret.strip()
            if self.refresh_token:
                self.refresh_token = self.refresh_token.strip()

            # Refresh the access token
            await self._refresh_access_token()
            self.true_path = f"Bearer {self.access_token}" if self.access_token else None

        except Exception as e:
            self.false_path = NodeError.format(e)