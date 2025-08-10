import unittest
from polysynergy_nodes.cast.string_to_bytes import StringToBytes


class TestStringToBytes(unittest.TestCase):

    def setUp(self):
        self.node = StringToBytes()
        self.node.true_path = False
        self.node.false_path = False

    def test_string_to_bytes(self):
        self.node.input_value = "Hello World"
        self.node.execute()
        self.assertEqual(self.node.true_path, b"Hello World")
        self.assertFalse(self.node.false_path)

    def test_utf8_string_to_bytes(self):
        self.node.input_value = "Hello 世界"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Hello 世界".encode("utf-8"))
        self.assertFalse(self.node.false_path)

    def test_empty_string_to_bytes(self):
        self.node.input_value = ""
        self.node.execute()
        self.assertEqual(self.node.true_path, b"")
        self.assertFalse(self.node.false_path)

    def test_bytes_passthrough(self):
        test_bytes = b"Already bytes"
        self.node.input_value = test_bytes
        self.node.execute()
        self.assertEqual(self.node.true_path, test_bytes)
        self.assertFalse(self.node.false_path)

    def test_int_to_bytes(self):
        self.node.input_value = 123
        self.node.execute()
        self.assertEqual(self.node.true_path, b"123")
        self.assertFalse(self.node.false_path)

    def test_none_to_bytes(self):
        self.node.input_value = None
        self.node.execute()
        self.assertEqual(self.node.true_path, b"None")
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()