import logging
import unittest
from polysynergy_nodes.base64.decode_base64 import DecodeBase64

class TestDecodeBase64Node(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        self.node = DecodeBase64()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_base64_string(self):
        self.node.value = "SGVsbG8gd29ybGQ="  # "Hello world"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Hello world")
        self.assertFalse(self.node.false_path)

    def test_valid_base64_bytes(self):
        self.node.value = b"UHl0aG9u"  # "Python"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Python")
        self.assertFalse(self.node.false_path)

    def test_invalid_base64(self):
        self.node.value = "Not base64!"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_empty_string(self):
        self.node.value = ""
        self.node.execute()
        self.assertEqual(self.node.true_path, "")
        self.assertFalse(self.node.false_path)

if __name__ == '__main__':
    unittest.main()