import asyncio
import unittest
from polysynergy_nodes.variable.variable_string import VariableString
from unittest.mock import MagicMock

class TestVariableStringNode(unittest.TestCase):

    def setUp(self):
        self.node = VariableString()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_placeholder_replacement(self):
        self.node.value = "Hello, {{ name }}! You have {{ count }} new messages."
        self.node.values = {
            "name": "John",
            "count": "5"
        }
        asyncio.run(self.node.execute())
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, "Hello, John! You have 5 new messages.")

    def test_missing_placeholder(self):
        self.node.value = "Hello, {{ name }}! You have {{ count }} new messages."
        self.node.values = {
            "name": "John"
        }
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("count", str(self.node.false_path))

    def test_empty_value(self):
        self.node.value = ""
        self.node.values = {
            "name": "John"
        }
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "")

    def test_empty_values(self):
        self.node.value = "Hello, {{ name }}!"
        self.node.values = {}
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("name", str(self.node.false_path))

    def test_automatic_string_conversion_number(self):
        self.node.value = 42
        self.node.values = {}
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "42")

    def test_automatic_string_conversion_boolean(self):
        self.node.value = True
        self.node.values = {}
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "True")

    def test_automatic_string_conversion_float(self):
        self.node.value = 3.14159
        self.node.values = {}
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "3.14159")

    def test_automatic_string_conversion_none(self):
        self.node.value = None
        self.node.values = {}
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "")

    def test_automatic_string_conversion_with_placeholders(self):
        self.node.value = 100
        self.node.values = {"name": "John"}
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "100")

    def test_automatic_conversion_from_add_node_output(self):
        """Test that number outputs from math nodes (like add) work correctly"""
        self.node.value = 30  # Simulating output from add node: {"true_path": 30}
        self.node.values = {}
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "30")

if __name__ == "__main__":
    unittest.main()