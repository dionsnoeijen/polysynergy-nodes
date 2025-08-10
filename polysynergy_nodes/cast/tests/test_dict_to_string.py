import unittest
from polysynergy_nodes.cast.dict_to_string import DictToString


class TestDictToString(unittest.TestCase):

    def setUp(self):
        self.node = DictToString()
        self.node.true_path = False
        self.node.false_path = False

    def test_simple_dict_to_json(self):
        self.node.input_value = {"name": "John", "age": 30}
        self.node.execute()
        # Parse back to verify it's valid JSON
        import json
        result = json.loads(self.node.true_path)
        self.assertEqual(result, {"name": "John", "age": 30})
        self.assertFalse(self.node.false_path)

    def test_empty_dict_to_json(self):
        self.node.input_value = {}
        self.node.execute()
        self.assertEqual(self.node.true_path, "{}")
        self.assertFalse(self.node.false_path)

    def test_nested_dict_to_json(self):
        self.node.input_value = {"user": {"name": "John", "details": {"age": 30}}}
        self.node.execute()
        import json
        result = json.loads(self.node.true_path)
        expected = {"user": {"name": "John", "details": {"age": 30}}}
        self.assertEqual(result, expected)
        self.assertFalse(self.node.false_path)

    def test_list_values_to_json(self):
        self.node.input_value = {"items": ["apple", "banana"], "count": 2}
        self.node.execute()
        import json
        result = json.loads(self.node.true_path)
        expected = {"items": ["apple", "banana"], "count": 2}
        self.assertEqual(result, expected)
        self.assertFalse(self.node.false_path)

    def test_unicode_values_to_json(self):
        self.node.input_value = {"greeting": "Hello 世界", "emoji": "🌍"}
        self.node.execute()
        import json
        result = json.loads(self.node.true_path)
        expected = {"greeting": "Hello 世界", "emoji": "🌍"}
        self.assertEqual(result, expected)
        self.assertFalse(self.node.false_path)

    def test_non_serializable_object_error(self):
        # Create an object that can't be JSON serialized
        class NonSerializable:
            pass
        
        self.node.input_value = {"obj": NonSerializable()}
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)


if __name__ == "__main__":
    unittest.main()