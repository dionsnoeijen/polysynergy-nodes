import unittest
from polysynergy_nodes.cast.bytes_to_string import BytesToString


class TestBytesToString(unittest.TestCase):

    def setUp(self):
        self.node = BytesToString()
        self.node.true_path = False
        self.node.false_path = False

    def test_bytes_to_string(self):
        self.node.input_value = b"Hello World"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Hello World")
        self.assertFalse(self.node.false_path)

    def test_utf8_bytes_to_string(self):
        self.node.input_value = "Hello 世界".encode("utf-8")
        self.node.execute()
        self.assertEqual(self.node.true_path, "Hello 世界")
        self.assertFalse(self.node.false_path)

    def test_empty_bytes_to_string(self):
        self.node.input_value = b""
        self.node.execute()
        self.assertEqual(self.node.true_path, "")
        self.assertFalse(self.node.false_path)

    def test_string_passthrough(self):
        self.node.input_value = "Already a string"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Already a string")
        self.assertFalse(self.node.false_path)

    def test_int_to_string(self):
        self.node.input_value = 123
        self.node.execute()
        self.assertEqual(self.node.true_path, "123")
        self.assertFalse(self.node.false_path)

    def test_none_to_string(self):
        self.node.input_value = None
        self.node.execute()
        self.assertEqual(self.node.true_path, "None")
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()