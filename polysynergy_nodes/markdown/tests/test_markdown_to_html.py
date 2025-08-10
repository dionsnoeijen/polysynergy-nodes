import unittest
import asyncio
from polysynergy_nodes.markdown.markdown_to_html import MarkdownToHtml


class TestMarkdownToHtmlNode(unittest.TestCase):

    def setUp(self):
        self.node = MarkdownToHtml()
        self.node.true_path = False
        self.node.false_path = False

    def test_simple_markdown(self):
        self.node.markdown_input = "# Hello World"
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "<h1>Hello World</h1>")
        self.assertFalse(self.node.false_path)

    def test_paragraph_markdown(self):
        self.node.markdown_input = "This is a simple paragraph."
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "<p>This is a simple paragraph.</p>")
        self.assertFalse(self.node.false_path)

    def test_bold_italic_markdown(self):
        self.node.markdown_input = "**bold** and *italic* text"
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "<p><strong>bold</strong> and <em>italic</em> text</p>")
        self.assertFalse(self.node.false_path)

    def test_list_markdown(self):
        markdown_text = "- Item 1\n- Item 2\n- Item 3"
        expected_html = "<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n<li>Item 3</li>\n</ul>"
        self.node.markdown_input = markdown_text
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, expected_html)
        self.assertFalse(self.node.false_path)

    def test_code_block_markdown(self):
        markdown_text = "```python\nprint('hello')\n```"
        self.node.markdown_input = markdown_text
        asyncio.run(self.node.execute())
        self.assertIn('<code class="language-python">', self.node.true_path)
        self.assertIn("print('hello')", self.node.true_path)
        self.assertFalse(self.node.false_path)

    def test_link_markdown(self):
        self.node.markdown_input = "[Google](https://google.com)"
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, '<p><a href="https://google.com">Google</a></p>')
        self.assertFalse(self.node.false_path)

    def test_table_markdown(self):
        markdown_text = "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |"
        self.node.markdown_input = markdown_text
        asyncio.run(self.node.execute())
        self.assertIn("<table>", self.node.true_path)
        self.assertIn("<th>Header 1</th>", self.node.true_path)
        self.assertIn("<td>Cell 1</td>", self.node.true_path)
        self.assertFalse(self.node.false_path)

    def test_empty_markdown(self):
        self.node.markdown_input = ""
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, "")
        self.assertFalse(self.node.false_path)

    def test_complex_markdown(self):
        markdown_text = """# Main Title

## Subtitle

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2

[Link to example](https://example.com)

```
code block
```
"""
        self.node.markdown_input = markdown_text
        asyncio.run(self.node.execute())
        result = self.node.true_path
        self.assertIn("<h1>Main Title</h1>", result)
        self.assertIn("<h2>Subtitle</h2>", result)
        self.assertIn("<strong>bold</strong>", result)
        self.assertIn("<em>italic</em>", result)
        self.assertIn("<ul>", result)
        self.assertIn('<a href="https://example.com">Link to example</a>', result)
        self.assertFalse(self.node.false_path)

    def test_smarty_extension(self):
        self.node.markdown_input = '"Smart quotes" and -- dashes'
        asyncio.run(self.node.execute())
        # Smarty extension converts quotes and dashes to HTML entities
        self.assertIn("Smart quotes", self.node.true_path)
        self.assertIn("&ndash;", self.node.true_path)  # HTML entity for en-dash
        self.assertIn("&ldquo;", self.node.true_path)  # HTML entity for left double quote
        self.assertIn("&rdquo;", self.node.true_path)  # HTML entity for right double quote
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()