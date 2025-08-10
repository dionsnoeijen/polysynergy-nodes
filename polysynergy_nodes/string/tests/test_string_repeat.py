import asyncio
import pytest
from polysynergy_nodes.string.string_repeat import StringRepeat


class TestStringRepeat:
    def test_repeat_basic(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.count = 3
        node.separator = ""
        asyncio.run(node.execute())
        
        assert node.true_path == "hellohellohello"
        assert node.false_path is False

    def test_repeat_with_separator(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.count = 3
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello hello hello"
        assert node.false_path is False

    def test_repeat_with_custom_separator(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "A"
        node.count = 5
        node.separator = "-"
        asyncio.run(node.execute())
        
        assert node.true_path == "A-A-A-A-A"
        assert node.false_path is False

    def test_repeat_zero_times(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.count = 0
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_repeat_once(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.count = 1
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello"
        assert node.false_path is False

    def test_repeat_empty_string(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.count = 5
        node.separator = ","
        asyncio.run(node.execute())
        
        assert node.true_path == ",,,,"
        assert node.false_path is False

    def test_repeat_multiline_separator(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "line"
        node.count = 3
        node.separator = "\n"
        asyncio.run(node.execute())
        
        assert node.true_path == "line\nline\nline"
        assert node.false_path is False

    def test_repeat_negative_count(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.count = -1
        node.separator = ""
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Count must be a non-negative integer" in str(node.false_path)

    def test_repeat_non_string_text(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.count = 3
        node.separator = ""
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_repeat_non_string_separator(self):
        node = StringRepeat()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.count = 3
        node.separator = 123
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Separator must be a string" in str(node.false_path)