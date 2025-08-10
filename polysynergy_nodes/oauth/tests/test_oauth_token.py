import unittest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch
from polysynergy_nodes.oauth.oauthtoken import OAuthToken


class TestOAuthTokenNode(unittest.TestCase):

    def setUp(self):
        self.node = OAuthToken()
        self.node.service_name = "test_service"
        self.node.client_id = "test_client_id"
        self.node.client_secret = "test_client_secret"
        self.node.token_url = "https://example.com/oauth/token"
        self.node.grant_type = "client_credentials"
        self.node.scope = "read write"
        
        # Reset path settings
        self.node.true_path = False
        self.node.false_path = False

    @patch('polysynergy_nodes.oauth.oauthtoken.httpx.AsyncClient')
    @patch.object(OAuthToken, '_get_token_from_storage')
    @patch.object(OAuthToken, '_save_token_to_storage')
    def test_client_credentials_flow_success(self, mock_save, mock_get_storage, mock_client):
        """Test successful client credentials OAuth flow"""
        # Mock no existing token
        mock_get_storage.return_value = {}

        # Mock successful token response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        mock_client_instance = MagicMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        mock_save.return_value = None

        # Execute the node
        asyncio.run(self.node.execute())

        # Verify successful execution
        self.assertEqual(self.node.access_token, "test_access_token")
        self.assertEqual(self.node.token_type, "Bearer")
        self.assertEqual(self.node.expires_in, 3600)
        self.assertEqual(self.node.true_path, "test_access_token")
        self.assertFalse(self.node.false_path)

        # Verify HTTP request was made correctly
        mock_client_instance.post.assert_called_once()
        call_args = mock_client_instance.post.call_args
        # Check positional arguments (URL should be first)
        self.assertEqual(call_args[0][0], "https://example.com/oauth/token")
        # Check keyword arguments
        self.assertEqual(call_args[1]["data"]["grant_type"], "client_credentials")
        self.assertEqual(call_args[1]["data"]["client_id"], "test_client_id")
        self.assertEqual(call_args[1]["data"]["client_secret"], "test_client_secret")
        self.assertEqual(call_args[1]["data"]["scope"], "read write")

    @patch('polysynergy_nodes.oauth.oauthtoken.httpx.AsyncClient')
    @patch.object(OAuthToken, '_get_token_from_storage')
    def test_token_request_failure(self, mock_get_storage, mock_client):
        """Test OAuth token request failure"""
        # Mock no existing token
        mock_get_storage.return_value = {}

        # Mock failed token response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "invalid_client"
        mock_response.json.return_value = {
            "error": "invalid_client",
            "error_description": "Client authentication failed"
        }
        
        mock_client_instance = MagicMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Execute the node
        asyncio.run(self.node.execute())

        # Verify error handling
        self.assertFalse(self.node.true_path)
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

    @patch.object(OAuthToken, '_get_token_from_storage')
    def test_valid_cached_token(self, mock_get_storage):
        """Test using valid cached token without making new request"""
        # Mock existing valid token
        future_time = time.time() + 3600  # 1 hour in future
        mock_get_storage.return_value = {
            "access_token": "cached_token",
            "token_type": "Bearer",
            "expires_at": future_time,
            "expires_in": 3600
        }

        # Execute the node
        asyncio.run(self.node.execute())

        # Verify cached token is used
        self.assertEqual(self.node.access_token, "cached_token")
        self.assertEqual(self.node.token_type, "Bearer")
        self.assertEqual(self.node.true_path, "cached_token")
        self.assertFalse(self.node.false_path)

    @patch('polysynergy_nodes.oauth.oauthtoken.httpx.AsyncClient')
    @patch.object(OAuthToken, '_get_token_from_storage')
    @patch.object(OAuthToken, '_save_token_to_storage')
    def test_expired_token_refresh(self, mock_save, mock_get_storage, mock_client):
        """Test refreshing expired token"""
        # Mock existing expired token
        past_time = time.time() - 3600  # 1 hour ago
        mock_get_storage.return_value = {
            "access_token": "expired_token",
            "refresh_token": "refresh_token_123",
            "expires_at": past_time,
            "token_type": "Bearer"
        }

        # Set node to use refresh token grant
        self.node.grant_type = "refresh_token"

        # Mock successful refresh response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "new_refresh_token"
        }
        
        mock_client_instance = MagicMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        mock_save.return_value = None

        # Execute the node
        asyncio.run(self.node.execute())

        # Verify new token is obtained
        self.assertEqual(self.node.access_token, "new_access_token")
        self.assertEqual(self.node._refresh_token, "new_refresh_token")
        self.assertEqual(self.node.true_path, "new_access_token")
        self.assertFalse(self.node.false_path)

        # Verify refresh token was used in request
        call_args = mock_client_instance.post.call_args
        self.assertEqual(call_args[1]["data"]["grant_type"], "refresh_token")
        self.assertEqual(call_args[1]["data"]["refresh_token"], "refresh_token_123")

    @patch('polysynergy_nodes.oauth.oauthtoken.httpx.AsyncClient')
    @patch.object(OAuthToken, '_get_token_from_storage')
    def test_network_error_handling(self, mock_get_storage, mock_client):
        """Test handling of network errors"""
        # Mock no existing token
        mock_get_storage.return_value = {}

        # Mock network error
        import httpx
        mock_client_instance = MagicMock()
        mock_client_instance.post = AsyncMock(side_effect=httpx.RequestError("Connection failed"))
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # Execute the node
        asyncio.run(self.node.execute())

        # Verify error handling
        self.assertFalse(self.node.true_path)
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

    def test_token_validity_check(self):
        """Test token validity checking logic"""
        # Test with no token
        self.assertFalse(self.node._is_token_valid())

        # Test with valid token (no expiry)
        self.node.access_token = "valid_token"
        self.assertTrue(self.node._is_token_valid())

        # Test with token expiring soon
        self.node._expires_at = time.time() + 30  # 30 seconds
        self.assertFalse(self.node._is_token_valid())  # Should be invalid (60s buffer)

        # Test with token expiring later
        self.node._expires_at = time.time() + 120  # 2 minutes
        self.assertTrue(self.node._is_token_valid())

    @patch.object(OAuthToken, '_get_dynamodb_table')
    def test_dynamodb_unavailable(self, mock_get_table):
        """Test graceful handling when DynamoDB is unavailable"""
        # Mock DynamoDB unavailable
        mock_get_table.return_value = None

        # Test storage operations don't fail
        asyncio.run(self.node._get_token_from_storage())
        asyncio.run(self.node._save_token_to_storage())

        # Should not raise any exceptions

    def test_unsupported_grant_type(self):
        """Test error handling for unsupported grant type"""
        self.node.grant_type = "authorization_code"  # Unsupported

        async def test_unsupported():
            try:
                await self.node._request_new_token()
                self.fail("Should have raised ValueError")
            except ValueError as e:
                self.assertIn("Unsupported grant type", str(e))

        asyncio.run(test_unsupported())

    @patch('polysynergy_nodes.oauth.oauthtoken.httpx.AsyncClient')
    @patch.object(OAuthToken, '_get_token_from_storage')
    @patch.object(OAuthToken, '_save_token_to_storage')
    def test_scope_handling(self, mock_save, mock_get_storage, mock_client):
        """Test that scope parameter is properly included"""
        # Mock no existing token
        mock_get_storage.return_value = {}

        # Test with no scope
        self.node.scope = None

        # Mock successful token response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        mock_client_instance = MagicMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        mock_save.return_value = None

        # Execute the node
        asyncio.run(self.node.execute())

        # Verify scope is not included when None
        call_args = mock_client_instance.post.call_args
        self.assertNotIn("scope", call_args[1]["data"])


if __name__ == "__main__":
    unittest.main()