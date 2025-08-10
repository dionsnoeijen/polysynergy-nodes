import asyncio
import pytest
from polysynergy_nodes.string.string_pad import StringPad


class TestStringPad:
    def test_pad_left(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.width = 10
        node.fill_char = " "
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path == "     hello"
        assert node.false_path is False

    def test_pad_right(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.width = 10
        node.fill_char = " "
        node.pad_type = "right"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello     "
        assert node.false_path is False

    def test_pad_center(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.width = 11
        node.fill_char = " "
        node.pad_type = "center"
        asyncio.run(node.execute())
        
        assert node.true_path == "   hello   "
        assert node.false_path is False

    def test_pad_with_custom_char(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.width = 10
        node.fill_char = "*"
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path == "*****hello"
        assert node.false_path is False

    def test_pad_with_zero(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "42"
        node.width = 5
        node.fill_char = "0"
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path == "00042"
        assert node.false_path is False

    def test_pad_no_padding_needed(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.width = 5
        node.fill_char = " "
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"  # No truncation
        assert node.false_path is False

    def test_pad_empty_string(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.width = 5
        node.fill_char = "-"
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path == "-----"
        assert node.false_path is False

    def test_pad_invalid_fill_char(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.width = 10
        node.fill_char = "ab"  # Must be single char
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Fill character must be a single character" in str(node.false_path)

    def test_pad_non_string_text(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.width = 10
        node.fill_char = " "
        node.pad_type = "left"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_pad_invalid_type(self):
        node = StringPad()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.width = 10
        node.fill_char = " "
        node.pad_type = "invalid"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Invalid pad type" in str(node.false_path)