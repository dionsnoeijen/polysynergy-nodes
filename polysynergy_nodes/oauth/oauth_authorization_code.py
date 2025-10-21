import httpx
import time
import os
import boto3
import json

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(name="OAuth Authorization Code", category="auth", icon="oauth.svg")
class OAuthAuthorizationCode(Node):

    init_authorization: str = NodeVariableSettings(
        label="Authorize",
        dock=dock_property(),
        metadata={"button": "oauth_authorize"}
    )

    # Service identification (for user clarity)
    service_name: str = NodeVariableSettings(
        label="Service Name",
        dock=True,
        has_in=True,
        required=True,
        info="Human-readable name for this OAuth service (e.g. 'Google Drive', 'Slack API')"
    )

    # OAuth endpoints
    auth_url: str = NodeVariableSettings(
        label="Authorization URL",
        dock=True,
        has_in=True,
        required=True,
        info="OAuth authorization endpoint URL"
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

    client_secret: str = NodeVariableSettings(
        label="Client Secret",
        dock=True,
        has_in=True,
        required=True,
        info="OAuth client secret"
    )

    scopes: list[str] = NodeVariableSettings(
        label="OAuth Scopes",
        dock=True,
        has_in=True,
        required=True,
        info="List of OAuth permission scopes to request from the provider"
    )

    state: str | None = NodeVariableSettings(
        label="State",
        dock=True,
        has_in=True,
        info="State parameter for CSRF protection"
    )

    response_type: str | None = NodeVariableSettings(
        label="Response Type",
        dock=True,
        has_in=True,
        info="OAuth response type (default: 'code'). Azure AD may require 'code' or 'code id_token'. Most providers use 'code'.",
        default="code"
    )

    resource: str | None = NodeVariableSettings(
        label="Resource",
        dock=True,
        has_in=True,
        info="Resource parameter for Azure AD/SharePoint (e.g. 'https://outzsoftware.sharepoint.com'). Leave empty for other providers."
    )

    service_name_output: str | None = NodeVariableSettings(
        label="Service Name",
        dock=True,
        has_out=True,
        info="Name of the service being authenticated"
    )

    scopes_output: list[str] | None = NodeVariableSettings(
        label="Granted Scopes",
        dock=True,
        has_out=True,
        info="List of OAuth scopes that were requested"
    )

    access_token: str | None = NodeVariableSettings(
        label="Access Token",
        dock=False,
        has_out=True,
        info="OAuth access token (when code is provided)"
    )

    refresh_token: str | None = NodeVariableSettings(
        label="Refresh Token",
        dock=False,
        has_out=True,
        info="OAuth refresh token for token renewal"
    )

    token_type: str | None = NodeVariableSettings(
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

    # Path settings
    true_path: bool | str | dict = PathSettings(
        label="Success",
        info="Triggered on success with either auth URL or tokens"
    )

    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered when request fails"
    )

    # Private attributes
    _dynamodb_table = None
    _expires_at: float | None = None

    def _get_dynamodb_table(self):
        """Lazy initialization of DynamoDB table"""
        if self._dynamodb_table is None:
            print(f"[OAuth Debug] Initializing DynamoDB table...")
            try:
                aws_key = os.getenv("AWS_ACCESS_KEY_ID")
                aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
                aws_region = os.getenv("AWS_REGION", "eu-central-1")
                print(f"[OAuth Debug] AWS Key present: {bool(aws_key)}")
                print(f"[OAuth Debug] AWS Secret present: {bool(aws_secret)}")
                print(f"[OAuth Debug] AWS Region: {aws_region}")

                dynamodb = boto3.resource(
                    "dynamodb",
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret,
                    region_name=aws_region,
                )
                self._dynamodb_table = dynamodb.Table("OAuthTokens")
                print(f"[OAuth Debug] DynamoDB table initialized successfully")
            except Exception as e:
                print(f"[OAuth Debug] Failed to initialize DynamoDB: {str(e)}")
                # If DynamoDB is not available, skip token caching
                self._dynamodb_table = None
        return self._dynamodb_table

    async def _save_token_to_storage(self):
        """Save token to DynamoDB if available"""
        table = self._get_dynamodb_table()
        if table is None:
            return

        try:
            # Use node_id as primary key and merge with existing record
            update_expression = "SET access_token = :at, token_type = :tt"
            expression_values = {
                ":at": self.access_token,
                ":tt": self.token_type,
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
            # Silently fail if DynamoDB is not available
            pass

    def _get_redirect_uri(self):
        """Get the correct redirect URI based on environment"""
        # If user provided a custom redirect URI, use that
        if self.redirect_uri:
            return self.redirect_uri

        # Otherwise, auto-detect based on environment
        api_base_url = os.getenv("API_BASE_URL")

        if api_base_url:
            return f"{api_base_url}/api/v1/oauth/callback"
        else:
            # Fallback based on common environment indicators
            environment = os.getenv("ENVIRONMENT", "local").lower()

            if environment == "production":
                return "https://api.polysynergy.com/api/v1/oauth/callback"
            else:
                # Local development - check common ports
                local_port = os.getenv("PORT", "8090")  # Default to 8090
                return f"http://localhost:{local_port}/api/v1/oauth/callback"

    def _build_authorization_url(self):
        """Build the authorization URL for user redirect"""
        from urllib.parse import urlencode

        redirect_uri = self._get_redirect_uri()

        # Use configured response_type or default to 'code'
        response_type_value = self.response_type if self.response_type else "code"

        # Debug logging
        print(f"[OAuth Debug] response_type input: {self.response_type}")
        print(f"[OAuth Debug] response_type_value to use: {response_type_value}")

        params = {
            "response_type": response_type_value,
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
        }

        print(f"[OAuth Debug] Initial params: {params}")

        # Convert list of scopes to space-separated string
        if not self.scopes or len(self.scopes) == 0:
            raise ValueError("At least one OAuth scope is required")

        scope_string = " ".join(self.scopes)
        params["scope"] = scope_string

        # Always include state with node_id for callback tracking
        state_data = {
            "node_id": self.id,
            "flow_id": self.context.node_setup_version_id if self.context else None,
            "tenant_id": getattr(self.context, 'tenant_id', None) if self.context else None,
            "trigger_node_id": getattr(self.context, 'trigger_node_id', None) if self.context else None,
        }

        # Include user-provided state if any
        if self.state:
            state_data["user_state"] = self.state

        # Use base64 encoded JSON for state to avoid URL encoding issues
        import base64
        state_json = json.dumps(state_data)
        params["state"] = base64.urlsafe_b64encode(state_json.encode()).decode().rstrip('=')

        # Only add provider-specific parameters if we detect the provider
        # Don't add Google-specific params to all requests!
        if "accounts.google.com" in self.auth_url.lower():
            params["access_type"] = "offline"  # For Google, ensures refresh token
            params["prompt"] = "consent"  # Forces consent screen
        elif "microsoftonline.com" in self.auth_url.lower() or "microsoft.com" in self.auth_url.lower():
            # Azure AD specific parameters
            params["prompt"] = "select_account"  # Let user choose account
            # Add resource parameter if provided (needed for SharePoint, etc.)
            if self.resource:
                params["resource"] = self.resource
            # Note: response_mode could be added here if needed
            # params["response_mode"] = "query"  # or "fragment"

        # Always ensure response_type=code is in the URL
        if "response_type" not in params or not params["response_type"]:
            params["response_type"] = "code"

        auth_url = f"{self.auth_url}?{urlencode(params)}"

        # Debug logging
        print(f"Generated OAuth URL: {auth_url}")
        print(f"Params: {params}")

        return auth_url

    async def _exchange_code_for_token(self):
        """Exchange authorization code for access token"""
        redirect_uri = self._get_redirect_uri()

        data = {
            "grant_type": "authorization_code",
            "code": self.code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
        }

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
                        self._expires_at = time.time() + int(self.expires_in)

                    # Save to storage
                    await self._save_token_to_storage()

                    return True
                else:
                    error_text = response.text
                    try:
                        error_data = response.json()
                        error_text = error_data.get(
                            "error_description",
                            error_data.get("error", error_text)
                        )
                    except:
                        pass

                    raise Exception(f"Token exchange failed ({response.status_code}): {error_text}")

        except httpx.RequestError as e:
            raise Exception(f"Network error during token exchange: {str(e)}")

    async def _get_token_from_storage(self):
        """Get stored token from DynamoDB if available"""
        print(f"[OAuth Debug] _get_token_from_storage called")
        table = self._get_dynamodb_table()
        print(f"[OAuth Debug] DynamoDB table: {table}")
        if table is None:
            print(f"[OAuth Debug] No DynamoDB table available")
            return {}

        try:
            print(f"[OAuth Debug] Getting item with node_id: {self.id}")
            response = table.get_item(Key={"node_id": self.id})
            item = response.get("Item", {})
            print(f"[OAuth Debug] Retrieved item: {bool(item)}")
            return item
        except Exception as e:
            print(f"[OAuth Debug] Error getting token from storage: {str(e)}")
            return {}

    def _is_token_valid(self):
        """Check if current token is still valid"""
        if not self.access_token:
            return False
        if self._expires_at is None:
            return True  # Assume valid if no expiry info
        return self._expires_at > time.time() + 60  # 60 second buffer

    async def _refresh_access_token(self):
        """Refresh the access token using the refresh token"""
        if not self.refresh_token:
            raise Exception("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

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

                    # Some providers return a new refresh token, others keep the old one
                    new_refresh_token = token_data.get("refresh_token")
                    if new_refresh_token:
                        self.refresh_token = new_refresh_token

                    # Calculate expiry time
                    if self.expires_in:
                        self._expires_at = time.time() + int(self.expires_in)

                    # Save to storage
                    await self._save_token_to_storage()

                else:
                    error_text = response.text
                    try:
                        error_data = response.json()
                        error_text = error_data.get(
                            "error_description",
                            error_data.get("error", error_text)
                        )
                    except:
                        pass

                    raise Exception(f"Token refresh failed ({response.status_code}): {error_text}")

        except httpx.RequestError as e:
            raise Exception(f"Network error during token refresh: {str(e)}")

    async def execute(self):
        # Trim whitespace from string inputs
        if self.auth_url:
            self.auth_url = self.auth_url.strip()
        if self.token_url:
            self.token_url = self.token_url.strip()
        if self.client_id:
            self.client_id = self.client_id.strip()
        if self.client_secret:
            self.client_secret = self.client_secret.strip()
        if self.service_name:
            self.service_name = self.service_name.strip()
        if self.resource:
            self.resource = self.resource.strip()

        print(f"[OAuth Debug] === Starting OAuth node execution ===")
        print(f"[OAuth Debug] Service: {self.service_name}")
        print(f"[OAuth Debug] Node ID: {self.id}")
        print(f"[OAuth Debug] Auth URL: {self.auth_url}")
        print(f"[OAuth Debug] Token URL: {self.token_url}")
        print(f"[OAuth Debug] Client ID: {self.client_id[:10]}..." if self.client_id else "None")
        print(f"[OAuth Debug] Scopes: {self.scopes}")

        try:
            # Always output service name and scopes for clarity
            self.service_name_output = self.service_name
            self.scopes_output = self.scopes

            # Load existing tokens from storage
            print(f"[OAuth Debug] Attempting to load tokens from storage...")
            token_data = await self._get_token_from_storage()
            print(f"[OAuth Debug] Token data loaded: {bool(token_data)}")

            if token_data:
                print(f"[OAuth Debug] Found existing token data")
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                self._expires_at = token_data.get("token_expires")
                self.token_type = token_data.get("token_type", "Bearer")
                # Convert expires_in to int if it's stored as string
                expires_in_raw = token_data.get("expires_in")
                if expires_in_raw:
                    self.expires_in = int(expires_in_raw) if isinstance(expires_in_raw, str) else expires_in_raw
                else:
                    self.expires_in = None

                print(f"[OAuth Debug] Has access token: {bool(self.access_token)}")
                print(f"[OAuth Debug] Has refresh token: {bool(self.refresh_token)}")
                print(f"[OAuth Debug] Expires at: {self._expires_at}")

                # Check if current token is valid
                token_valid = self._is_token_valid()
                print(f"[OAuth Debug] Token is valid: {token_valid}")

                if token_valid:
                    # We have a valid token, proceed with true_path
                    print(f"[OAuth Debug] Using valid token, setting true_path")
                    self.true_path = f"Bearer {self.access_token}"
                    return

                # Token expired but we have refresh token - try to refresh
                print(f"[OAuth Debug] Token expired, checking for refresh token...")
                if self.refresh_token:
                    try:
                        print(f"[OAuth Debug] Attempting to refresh token...")
                        await self._refresh_access_token()
                        print(f"[OAuth Debug] Token refresh successful, setting true_path")
                        self.true_path = f"Bearer {self.access_token}"
                        return
                    except Exception as e:
                        print(f"[OAuth Debug] Token refresh failed: {str(e)}")
                        # Refresh failed, clear tokens for next authorization
                        self.access_token = None
                        self.refresh_token = None
                        self.token_type = None
                        self.expires_in = None
                        # Set false_path because refresh failed
                        print(f"[OAuth Debug] Setting false_path due to refresh failure")
                        self.false_path = f"Token refresh failed: {str(e)}"
                        return

            # No valid tokens available - trigger false path
            print(f"[OAuth Debug] No valid tokens available")
            print(f"[OAuth Debug] Setting false_path - no tokens available")
            self.false_path = "No valid OAuth tokens available"
            print(f"[OAuth Debug] false_path set, execution completed")

        except Exception as e:
            print(f"[OAuth Debug] ERROR in execute: {str(e)}")
            print(f"[OAuth Debug] Setting false_path")
            self.false_path = NodeError.format(e)
            print(f"[OAuth Debug] false_path set to: {self.false_path}")