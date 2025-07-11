import unittest

from polysynergy_nodes.variable.variable_json import VariableJson


class TestVariableJsonNode(unittest.TestCase):

    def setUp(self):
        self.node = VariableJson()
        self.node.state = {}
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_json_input_with_append(self):
        self.node.value = {"a": "1", "b": "2"}
        self.node.append = {"c": "3"}
        self.node.execute()
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.value_as_dict_or_list, {"a": "1", "b": "2", "c": "3"})

    def test_valid_json_string_with_placeholders(self):
        self.node.value = '{"a": "{x}", "b": "{y}"}'
        self.node.values = {"x": "hello", "y": "world"}
        self.node.state = {"x": "hello", "y": "world"}
        self.node.execute()
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.value_as_dict_or_list, {"a": "hello", "b": "world"})

    def test_invalid_json_string(self):
        self.node.value = '{"a": "1", "b": 2'  # invalid JSON
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

    def test_append_to_non_dict(self):
        self.node.value = [1, 2, 3]
        self.node.append = {"x": "should fail"}
        self.node.execute()
        self.assertTrue(self.node.true_path)  # append ignored
        self.assertEqual(self.node.value_as_dict_or_list, [1, 2, 3])

    def test_json_serialization_failure(self):
        self.node.value = {"x": set([1, 2, 3])}  # sets not serializable
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()