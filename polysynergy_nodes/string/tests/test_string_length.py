import asyncio
import pytest
from polysynergy_nodes.string.string_length import StringLength


class TestStringLength:
    def test_string_length_basic(self):
        node = StringLength()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        asyncio.run(node.execute())
        
        assert node.true_path == 5
        assert node.false_path is False

    def test_string_length_empty(self):
        node = StringLength()
        node.true_path = False
        node.false_path = False
        node.text = ""
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.false_path is False

    def test_string_length_unicode(self):
        node = StringLength()
        node.true_path = False
        node.false_path = False
        node.text = "héllo wörld 🚀"
        asyncio.run(node.execute())
        
        assert node.true_path == 13
        assert node.false_path is False

    def test_string_length_non_string_input(self):
        node = StringLength()
        node.text = 123
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Input must be a string" in str(node.false_path)