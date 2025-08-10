import asyncio
import unittest
from polysynergy_nodes.variable.variable_dict import VariableDict


class TestVariableDictNode(unittest.TestCase):
    def setUp(self):
        self.node = VariableDict()
        self.node.true_path = False
        self.node.false_path = False

    def test_simple_dict_value(self):
        self.node.value = {"name": "John", "age": 30}
        asyncio.run(self.node.execute())
        
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, {"name": "John", "age": 30})
        self.assertEqual(self.node.value_as_json_string, '{"name": "John", "age": 30}')

    def test_empty_dict(self):
        self.node.value = {}
        asyncio.run(self.node.execute())
        
        # Empty dict should still trigger true_path
        self.assertEqual(self.node.true_path, {})
        self.assertEqual(self.node.value_as_json_string, '{}')

    def test_nested_dict(self):
        self.node.value = {"user": {"name": "John", "profile": {"age": 30}}}
        asyncio.run(self.node.execute())
        
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, {"user": {"name": "John", "profile": {"age": 30}}})

    def test_dict_with_various_types(self):
        self.node.value = {
            "string": "hello",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "list": [1, 2, 3]
        }
        asyncio.run(self.node.execute())
        
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, {
            "string": "hello",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "list": [1, 2, 3]
        })


if __name__ == "__main__":
    unittest.main()