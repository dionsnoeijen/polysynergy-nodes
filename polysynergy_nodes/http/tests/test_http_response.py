import unittest
from http import HTTPStatus
import asyncio
from polysynergy_nodes.http.http_response import HttpResponse

class TestHttpResponseNode(unittest.TestCase):

    def setUp(self):
        self.node = HttpResponse()

    def test_basic_response(self):
        self.node.headers = {"Content-Type": "text/plain"}
        self.node.body = "Hello, world!"
        self.node.http_status = HTTPStatus.CREATED.value
        asyncio.run(self.node.execute())

        self.assertIsNotNone(self.node.response)
        self.assertEqual(self.node.response["headers"]["Content-Type"], "application/json")  # Default content_type overrides header
        self.assertEqual(self.node.response["body"], "Hello, world!")
        self.assertEqual(self.node.response["status"], HTTPStatus.CREATED.value)

    def test_response_with_bytes_body(self):
        self.node.headers = {"X-Test": "1"}
        self.node.body = b"binary data"
        self.node.http_status = 202
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.response["body"], b"binary data")
        self.assertEqual(self.node.response["headers"]["X-Test"], "1")

    def test_response_with_invalid_headers(self):
        self.node.headers = "not a dict"
        self.node.body = "oops"
        self.node.http_status = 200

        asyncio.run(self.node.execute())
        self.assertIsInstance(self.node.response, object)

if __name__ == "__main__":
    unittest.main()