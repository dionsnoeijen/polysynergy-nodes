import unittest
from polysynergy_nodes.cast.string_to_int import StringToInt


class TestStringToInt(unittest.TestCase):

    def setUp(self):
        self.node = StringToInt()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_positive_integer(self):
        self.node.input_value = "123"
        self.node.execute()
        self.assertEqual(self.node.true_path, 123)
        self.assertFalse(self.node.false_path)

    def test_valid_negative_integer(self):
        self.node.input_value = "-456"
        self.node.execute()
        self.assertEqual(self.node.true_path, -456)
        self.assertFalse(self.node.false_path)

    def test_zero(self):
        self.node.input_value = "0"
        self.node.execute()
        self.assertEqual(self.node.true_path, 0)
        self.assertFalse(self.node.false_path)

    def test_string_with_whitespace(self):
        self.node.input_value = "  789  "
        self.node.execute()
        self.assertEqual(self.node.true_path, 789)
        self.assertFalse(self.node.false_path)

    def test_float_to_int(self):
        self.node.input_value = 12.7
        self.node.execute()
        self.assertEqual(self.node.true_path, 12)
        self.assertFalse(self.node.false_path)

    def test_int_passthrough(self):
        self.node.input_value = 42
        self.node.execute()
        self.assertEqual(self.node.true_path, 42)
        self.assertFalse(self.node.false_path)

    def test_invalid_string_format(self):
        self.node.input_value = "not_a_number"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_float_string_invalid(self):
        self.node.input_value = "12.34"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_empty_string(self):
        self.node.input_value = ""
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_mixed_alphanumeric(self):
        self.node.input_value = "123abc"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)


if __name__ == "__main__":
    unittest.main()