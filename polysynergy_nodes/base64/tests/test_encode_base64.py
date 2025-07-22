import unittest
from polysynergy_node_runner64.encode_base64 import EncodeBase64

class TestEncodeBase64Node(unittest.TestCase):

    def setUp(self):
        self.node = EncodeBase64()
        self.node.true_path = False
        self.node.false_path = False

    def test_encode_string(self):
        self.node.value = "Hello world"
        self.node.execute()
        self.assertEqual(self.node.true_path, "SGVsbG8gd29ybGQ=")
        self.assertFalse(self.node.false_path)

    def test_encode_bytes(self):
        self.node.value = b"Python"
        self.node.execute()
        self.assertEqual(self.node.true_path, "UHl0aG9u")
        self.assertFalse(self.node.false_path)

    def test_empty_string(self):
        self.node.value = ""
        self.node.execute()
        self.assertEqual(self.node.true_path, "")
        self.assertFalse(self.node.false_path)

    def test_invalid_type(self):
        self.node.value = 12345  # Not encodable
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()