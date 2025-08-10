import asyncio
import pytest
from polysynergy_nodes.string.string_reverse import StringReverse


class TestStringReverse:
    def test_reverse_basic(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        asyncio.run(node.execute())
        
        assert node.true_path == "olleh"
        assert node.false_path is False

    def test_reverse_with_spaces(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        asyncio.run(node.execute())
        
        assert node.true_path == "dlrow olleh"
        assert node.false_path is False

    def test_reverse_palindrome(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "racecar"
        asyncio.run(node.execute())
        
        assert node.true_path == "racecar"
        assert node.false_path is False

    def test_reverse_empty_string(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = ""
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_reverse_single_char(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "a"
        asyncio.run(node.execute())
        
        assert node.true_path == "a"
        assert node.false_path is False

    def test_reverse_special_characters(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "!@#$%^&*()"
        asyncio.run(node.execute())
        
        assert node.true_path == ")(*&^%$#@!"
        assert node.false_path is False

    def test_reverse_unicode(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "hello 🚀 world"
        asyncio.run(node.execute())
        
        assert node.true_path == "dlrow 🚀 olleh"
        assert node.false_path is False

    def test_reverse_numbers(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = "12345"
        asyncio.run(node.execute())
        
        assert node.true_path == "54321"
        assert node.false_path is False

    def test_reverse_non_string_text(self):
        node = StringReverse()
        node.true_path = False
        node.false_path = False
        node.text = 123
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)