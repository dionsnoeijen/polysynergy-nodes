import asyncio
import pytest
from polysynergy_nodes.string.string_starts_with import StringStartsWith


class TestStringStartsWith:
    def test_starts_with_true(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.prefix = "hello"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_starts_with_false(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.prefix = "world"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_starts_with_case_sensitive(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "Hello World"
        node.prefix = "hello"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_starts_with_case_insensitive(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "Hello World"
        node.prefix = "hello"
        node.case_sensitive = False
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_starts_with_empty_prefix(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.prefix = ""
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True  # Empty string is always at the start
        assert node.false_path is False

    def test_starts_with_empty_text(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.prefix = "hello"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_starts_with_exact_match(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.prefix = "hello"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_starts_with_special_characters(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "@#$%hello"
        node.prefix = "@#$%"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_starts_with_non_string_text(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.prefix = "1"
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_starts_with_non_string_prefix(self):
        node = StringStartsWith()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.prefix = 123
        node.case_sensitive = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Prefix must be a string" in str(node.false_path)