import asyncio
import pytest
from polysynergy_nodes.string.string_ends_with import StringEndsWith


class TestStringEndsWith:
    def test_ends_with_true(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.suffix = "world"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_ends_with_false(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.suffix = "hello"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_ends_with_case_sensitive(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "Hello World"
        node.suffix = "world"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_ends_with_case_insensitive(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "Hello World"
        node.suffix = "world"
        node.case_sensitive = False
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_ends_with_empty_suffix(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.suffix = ""
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True  # Empty string is always at the end
        assert node.false_path is False

    def test_ends_with_file_extension(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "document.pdf"
        node.suffix = ".pdf"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_ends_with_special_characters(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello@#$%"
        node.suffix = "@#$%"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_ends_with_non_string_text(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.suffix = "3"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_ends_with_non_string_suffix(self):
        node = StringEndsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.suffix = 123
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Suffix must be a string" in str(node.false_path)