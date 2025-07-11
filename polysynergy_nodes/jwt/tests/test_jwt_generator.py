import unittest
from unittest.mock import patch, MagicMock
from polysynergy_nodes.jwt.jwt_generator import JWTGenerator

class TestJWTGeneratorNode(unittest.TestCase):

    def setUp(self):
        self.node = JWTGenerator()
        self.node.true_path = False
        self.node.false_path = False

    @patch("polysynergy_nodes.jwt.jwt_generator.jwt.encode")
    @patch("polysynergy_nodes.jwt.jwt_generator.requests.post")
    def test_successful_token_exchange(self, mock_post, mock_jwt_encode):
        self.node.jwt_claims = {
            "iss": "test-issuer",
            "aud": "https://example.com/token",
            "scope": "test-scope",
            "exp_time": 3600
        }
        self.node.exchange_config = {
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIB...fake...\n-----END PRIVATE KEY-----",
            "token_uri": "https://example.com/token"
        }

        mock_jwt_encode.return_value = "signed-jwt-token"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "fake-access-token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        self.node.execute()

        self.assertEqual(self.node.access_token, "fake-access-token")
        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)


    @patch("polysynergy_nodes.jwt.jwt_generator.requests.post")
    def test_failure_response(self, mock_post):
        self.node.jwt_claims = {
            "iss": "test-issuer",
            "aud": "https://example.com/token"
        }
        self.node.exchange_config = {
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIB...fake...\n-----END PRIVATE KEY-----",
            "token_uri": "https://example.com/token"
        }

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid request"
        mock_post.return_value = mock_response

        self.node.execute()

        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()