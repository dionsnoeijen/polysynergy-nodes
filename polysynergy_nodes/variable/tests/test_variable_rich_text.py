import asyncio
import unittest
from polysynergy_nodes.variable.variable_rich_text import VariableRichText


class TestVariableRichTextNode(unittest.TestCase):
    def setUp(self):
        self.node = VariableRichText()
        self.node.true_path = False
        self.node.false_path = False

    def test_simple_rich_text(self):
        self.node.value = "<p>Hello World!</p>"
        self.node.values = {}
        asyncio.run(self.node.execute())
        
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, "<p>Hello World!</p>")

    def test_rich_text_with_placeholders(self):
        self.node.value = "<p>Hello {{ name }}!</p>"
        self.node.values = {"name": "John"}
        asyncio.run(self.node.execute())
        
        self.assertTrue(self.node.true_path)
        self.assertEqual(self.node.true_path, "<p>Hello John!</p>")

    def test_complex_html_structure(self):
        html_content = """
        <div class="container">
            <h1>Welcome {{ username }}</h1>
            <p>You have {{ count }} new messages.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
        """
        self.node.value = html_content
        self.node.values = {"username": "Alice", "count": "5"}
        asyncio.run(self.node.execute())
        
        self.assertTrue(self.node.true_path)
        self.assertIn("Alice", self.node.true_path)
        self.assertIn("5 new messages", self.node.true_path)

    def test_empty_rich_text(self):
        self.node.value = ""
        self.node.values = {}
        asyncio.run(self.node.execute())
        
        self.assertEqual(self.node.true_path, "")

    def test_missing_placeholder_error(self):
        self.node.value = "<p>Hello {{ name }}!</p>"
        self.node.values = {}  # No name provided
        asyncio.run(self.node.execute())
        
        self.assertFalse(self.node.true_path)
        self.assertIn("name", str(self.node.false_path))

    def test_non_string_value_error(self):
        self.node.value = 12345  # Not a string
        self.node.values = {}
        asyncio.run(self.node.execute())
        
        self.assertFalse(self.node.true_path)
        self.assertIn("Value must be a string", str(self.node.false_path))


if __name__ == "__main__":
    unittest.main()