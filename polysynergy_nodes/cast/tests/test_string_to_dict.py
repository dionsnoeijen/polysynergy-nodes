import unittest
from polysynergy_nodes.cast.string_to_dict import StringToDict


class TestStringToDict(unittest.TestCase):

    def setUp(self):
        self.node = StringToDict()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_json_object(self):
        self.node.input_value = '{"name": "John", "age": 30}'
        self.node.execute()
        expected = {"name": "John", "age": 30}
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_valid_json_array(self):
        self.node.input_value = '["apple", "banana", "cherry"]'
        self.node.execute()
        expected = ["apple", "banana", "cherry"]
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_valid_json_with_whitespace(self):
        self.node.input_value = '  {"test": true}  '
        self.node.execute()
        expected = {"test": True}
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_empty_json_object(self):
        self.node.input_value = '{}'
        self.node.execute()
        self.assertEqual(self.node.true_path, {})
        self.assertFalse(self.node.false_path)

    def test_invalid_json_syntax(self):
        self.node.input_value = '{"name": "John", "age":}'
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_invalid_json_format(self):
        self.node.input_value = "Not JSON at all"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_empty_string(self):
        self.node.input_value = ""
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_nested_json(self):
        self.node.input_value = '{"user": {"name": "John", "details": {"age": 30}}}'
        self.node.execute()
        expected = {"user": {"name": "John", "details": {"age": 30}}}
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()