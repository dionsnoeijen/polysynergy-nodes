import asyncio
import pytest
from polysynergy_nodes.string.string_substring import StringSubstring


class TestStringSubstring:
    def test_substring_basic(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.start = 0
        node.end = 5
        asyncio.run(node.execute())
        
        assert node.true_path == "hello"
        assert node.false_path is False

    def test_substring_middle(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.start = 6
        node.end = 11
        asyncio.run(node.execute())
        
        assert node.true_path == "world"
        assert node.false_path is False

    def test_substring_to_end(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.start = 6
        node.end = None
        asyncio.run(node.execute())
        
        assert node.true_path == "world"
        assert node.false_path is False

    def test_substring_negative_indices(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.start = -5
        node.end = None
        asyncio.run(node.execute())
        
        assert node.true_path == "world"
        assert node.false_path is False

    def test_substring_negative_end(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.start = 0
        node.end = -6
        asyncio.run(node.execute())
        
        assert node.true_path == "hello"
        assert node.false_path is False

    def test_substring_empty_range(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.start = 5
        node.end = 5
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_substring_out_of_bounds(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.start = 10
        node.end = 20
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_substring_single_char(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.start = 1
        node.end = 2
        asyncio.run(node.execute())
        
        assert node.true_path == "e"
        assert node.false_path is False

    def test_substring_empty_string(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.start = 0
        node.end = 5
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_substring_non_string_text(self):
        node = StringSubstring()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.start = 0
        node.end = 2
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)