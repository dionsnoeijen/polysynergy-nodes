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


@node(name="OAuth Device Code", category="auth", icon="oauth.svg")
class OAuthDeviceCode(Node):
    """OAuth 2.0 Device Code Grant flow node - for devices with limited input capability"""

    # Note: node_id is automatically available from the Node base class

    # OAuth endpoints
    device_auth_url: str = NodeVariableSettings(
        label="Device Authorization URL",
        dock=True,
        has_in=True,
        required=True,
        info="Device authorization endpoint URL"
    )

    token_url: str = NodeVariableSettings(
        label="Token URL",
        dock=True,
        has_in=True,
        required=True,
        info="OAuth token endpoint URL"
    )

    # Client credentials
    client_id: str = NodeVariableSettings(
        label="Client ID",
        dock=True,
        has_in=True,
        required=True,
        info="OAuth client identifier"
    )

    client_secret: Optional[str] = NodeVariableSettings(
        label="Client Secret",
        dock=True,
        has_in=True,
        info="OAuth client secret (optional for device flow)"
    )

    scope: Optional[str] = NodeVariableSettings(
        label="Scope",
        dock=True,
        has_in=True,
        info="OAuth scope (optional)"
    )

    # Device flow specific inputs
    device_code: Optional[str] = NodeVariableSettings(
        label="Device Code",
        dock=True,
        has_in=True,
        info="Device code from previous authorization (for polling)"
    )

    # Output parameters for device authorization
    user_code: Optional[str] = NodeVariableSettings(
        label="User Code",
        dock=True,
        has_out=True,
        info="Code for user to enter"
    )

    verification_url: Optional[str] = NodeVariableSettings(
        label="Verification URL",
        dock=True,
        has_out=True,
        info="URL where user should authenticate"
    )

    verification_url_complete: Optional[str] = NodeVariableSettings(
        label="Complete Verification URL",
        dock=True,
        has_out=True,
        info="Pre-filled verification URL (if supported)"
    )

    device_code_output: Optional[str] = NodeVariableSettings(
        label="Device Code",
        dock=True,
        has_out=True,
        info="Device code for polling"
    )

    expires_in_device: Optional[int] = NodeVariableSettings(
        label="Device Code Expires In",
        dock=True,
        has_out=True,
        info="Device code expiry time in seconds"
    )

    interval: Optional[int] = NodeVariableSettings(
        label="Polling Interval",
        dock=True,
        has_out=True,
        info="Minimum seconds between polling requests"
    )

    # Token outputs
    access_token: Optional[str] = NodeVariableSettings(
        label="Access Token",
        dock=True,
        has_out=True,
        info="OAuth access token (after successful polling)"
    )

    refresh_token: Optional[str] = NodeVariableSettings(
        label="Refresh Token",
        dock=True,
        has_out=True,
        info="OAuth refresh token (if provided)"
    )

    token_type: Optional[str] = NodeVariableSettings(
        label="Token Type",
        has_out=True,
        info="Token type (usually 'Bearer')"
    )

    expires_in: Optional[int] = NodeVariableSettings(
        label="Token Expires In",
        dock=True,
        has_out=True,
        info="Access token expiry time in seconds"
    )

    # Path settings
    true_path: bool | dict = PathSettings(
        label="Success",
        info="Triggered on success with device info or tokens"
    )

    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered when request fails"
    )

    pending_path: bool | dict = PathSettings(
        label="Pending",
        info="User authorization is pending (for polling)"
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
                self._dynamodb_table = None
        return self._dynamodb_table

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
                ":gt": "device_code"
            }

            if self.refresh_token:
                update_expression += ", refresh_token = :rt"
                expression_values[":rt"] = self.refresh_token

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
            pass

    async def _request_device_code(self):
        """Request device code and user code"""
        data = {
            "client_id": self.client_id,
        }

        if self.scope:
            data["scope"] = self.scope

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.device_auth_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0
                )

                if response.status_code == 200:
                    device_data = response.json()

                    # Extract device authorization info
                    self.device_code_output = device_data.get("device_code")
                    self.user_code = device_data.get("user_code")
                    self.verification_url = device_data.get("verification_uri") or device_data.get("verification_url")
                    self.verification_url_complete = device_data.get("verification_uri_complete") or device_data.get("verification_url_complete")
                    self.expires_in_device = device_data.get("expires_in")
                    self.interval = device_data.get("interval", 5)

                    return True
                else:
                    error_text = response.text
                    try:
                        error_data = response.json()
                        error_text = error_data.get("error_description", error_data.get("error", error_text))
                    except:
                        pass

                    raise Exception(f"Device authorization failed ({response.status_code}): {error_text}")

        except httpx.RequestError as e:
            raise Exception(f"Network error during device authorization: {str(e)}")

    async def _poll_for_token(self):
        """Poll for access token using device code"""
        data = {
            "client_id": self.client_id,
            "device_code": self.device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        if self.client_secret:
            data["client_secret"] = self.client_secret

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
                    self.refresh_token = token_data.get("refresh_token")
                    self.token_type = token_data.get("token_type", "Bearer")
                    self.expires_in = token_data.get("expires_in")

                    # Calculate expiry time
                    if self.expires_in:
                        self._expires_at = time.time() + self.expires_in

                    # Save to storage
                    await self._save_token_to_storage()

                    return "success"
                else:
                    try:
                        error_data = response.json()
                        error = error_data.get("error")

                        if error == "authorization_pending":
                            return "pending"
                        elif error == "slow_down":
                            return "slow_down"
                        else:
                            error_text = error_data.get("error_description", error)
                            raise Exception(f"Token polling failed: {error_text}")
                    except ValueError:
                        raise Exception(f"Token polling failed ({response.status_code}): {response.text}")

        except httpx.RequestError as e:
            raise Exception(f"Network error during token polling: {str(e)}")

    async def execute(self):
        try:
            # Trim whitespace from string inputs
            if self.device_authorization_url:
                self.device_authorization_url = self.device_authorization_url.strip()
            if self.token_url:
                self.token_url = self.token_url.strip()
            if self.client_id:
                self.client_id = self.client_id.strip()
            if self.device_code:
                self.device_code = self.device_code.strip()

            if not self.device_code:
                # Step 1: Request device code
                await self._request_device_code()
                self.true_path = {
                    "action": "device_authorization",
                    "user_code": self.user_code,
                    "verification_url": self.verification_url,
                    "verification_url_complete": self.verification_url_complete,
                    "device_code": self.device_code_output,
                    "expires_in": self.expires_in_device,
                    "interval": self.interval,
                    "message": f"Please visit {self.verification_url} and enter code: {self.user_code}"
                }
            else:
                # Step 2: Poll for token
                result = await self._poll_for_token()

                if result == "success":
                    self.true_path = f"Bearer {self.access_token}" if self.access_token else None
                elif result == "pending":
                    self.pending_path = {
                        "action": "authorization_pending",
                        "message": "User has not yet authorized the device"
                    }
                elif result == "slow_down":
                    self.pending_path = {
                        "action": "slow_down",
                        "message": "Polling too frequently, increase interval"
                    }

        except Exception as e:
            self.false_path = NodeError.format(e)