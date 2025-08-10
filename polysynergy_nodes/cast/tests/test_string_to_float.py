import unittest
from polysynergy_nodes.cast.string_to_float import StringToFloat


class TestStringToFloat(unittest.TestCase):

    def setUp(self):
        self.node = StringToFloat()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_positive_float(self):
        self.node.input_value = "123.45"
        self.node.execute()
        self.assertEqual(self.node.true_path, 123.45)
        self.assertFalse(self.node.false_path)

    def test_valid_negative_float(self):
        self.node.input_value = "-456.78"
        self.node.execute()
        self.assertEqual(self.node.true_path, -456.78)
        self.assertFalse(self.node.false_path)

    def test_integer_string_to_float(self):
        self.node.input_value = "123"
        self.node.execute()
        self.assertEqual(self.node.true_path, 123.0)
        self.assertFalse(self.node.false_path)

    def test_zero(self):
        self.node.input_value = "0.0"
        self.node.execute()
        self.assertEqual(self.node.true_path, 0.0)
        self.assertFalse(self.node.false_path)

    def test_scientific_notation(self):
        self.node.input_value = "1.23e-4"
        self.node.execute()
        self.assertEqual(self.node.true_path, 1.23e-4)
        self.assertFalse(self.node.false_path)

    def test_string_with_whitespace(self):
        self.node.input_value = "  789.12  "
        self.node.execute()
        self.assertEqual(self.node.true_path, 789.12)
        self.assertFalse(self.node.false_path)

    def test_int_to_float(self):
        self.node.input_value = 42
        self.node.execute()
        self.assertEqual(self.node.true_path, 42.0)
        self.assertFalse(self.node.false_path)

    def test_float_passthrough(self):
        self.node.input_value = 12.34
        self.node.execute()
        self.assertEqual(self.node.true_path, 12.34)
        self.assertFalse(self.node.false_path)

    def test_invalid_string_format(self):
        self.node.input_value = "not_a_number"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_empty_string(self):
        self.node.input_value = ""
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_mixed_alphanumeric(self):
        self.node.input_value = "12.34abc"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_multiple_dots(self):
        self.node.input_value = "12.34.56"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)


if __name__ == "__main__":
    unittest.main()