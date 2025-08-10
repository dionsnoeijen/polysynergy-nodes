import logging
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from polysynergy_nodes.http.http_request import HttpRequest

class TestHttpRequestNode(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        self.node = HttpRequest()
        self.node.true_path = False
        self.node.false_path = False
        self.node.state = {}  # dummy state, want replace_placeholders wordt aangeroepen

    @patch("polysynergy_nodes.http.http_request.httpx.AsyncClient")
    def test_successful_get_request(self, mock_client_class):
        self.node.url = "https://example.com"
        self.node.url_variables = {}
        self.node.method = "GET"
        self.node.headers = {}
        self.node.body = ""
        self.node.query = {}
        self.node.cookies = {}
        self.node.timeout = 10
        self.node.allow_redirects = True
        self.node.verify_ssl = True
        self.node.proxies = None

        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.cookies = {}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_client.request.return_value = mock_response

        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, "OK")
        self.assertEqual(self.node.response_http_status, 200)
        self.assertEqual(self.node.response_body, "OK")
        self.assertEqual(self.node.response_headers, {"Content-Type": "text/plain"})
        self.assertEqual(self.node.response_cookies, {})
        self.assertEqual(self.node.response_elapsed, 0.1)
        self.assertFalse(self.node.false_path)

    @patch("polysynergy_nodes.http.http_request.httpx.AsyncClient")
    def test_http_error(self, mock_client_class):
        self.node.url = "https://example.com/not-found"
        self.node.url_variables = {}
        self.node.method = "GET"
        self.node.headers = {}
        self.node.body = ""
        self.node.query = {}
        self.node.cookies = {}
        self.node.timeout = 10
        self.node.allow_redirects = True
        self.node.verify_ssl = True
        self.node.proxies = None

        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.headers = {}
        mock_response.cookies = {}
        mock_response.elapsed.total_seconds.return_value = 0.2
        mock_client.request.return_value = mock_response

        asyncio.run(self.node.execute())

        self.assertEqual(self.node.response_http_status, 404)
        self.assertIn("error", self.node.false_path)
        self.assertEqual(self.node.false_path["error"], "404: Not Found")

    @patch("polysynergy_nodes.http.http_request.httpx.AsyncClient")
    def test_json_body_parsing_error_fallback(self, mock_client_class):
        self.node.url = "https://example.com"
        self.node.url_variables = {}
        self.node.method = "POST"
        self.node.headers = {"Content-Type": "application/json"}
        self.node.body = "{invalid: true}"  # geen geldige JSON
        self.node.query = {}
        self.node.cookies = {}
        self.node.timeout = 10
        self.node.allow_redirects = True
        self.node.verify_ssl = True
        self.node.proxies = None

        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Fallback OK"
        mock_response.headers = {}
        mock_response.cookies = {}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_client.request.return_value = mock_response

        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, "Fallback OK")

if __name__ == "__main__":
    unittest.main()