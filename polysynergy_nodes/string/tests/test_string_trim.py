import asyncio
import pytest
from polysynergy_nodes.string.string_trim import StringTrim


class TestStringTrim:
    def test_trim_whitespace_default(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "  hello world  "
        node.characters = ""  # Default whitespace trimming
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_leading_whitespace(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "   hello world"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_trailing_whitespace(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "hello world   "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_tabs_and_newlines(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "\t\n  hello world  \n\t"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_specific_characters(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "xxxhello worldxxx"
        node.characters = "x"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_multiple_characters(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "xyzabc hello world abczyx"
        node.characters = "xyzabc"
        asyncio.run(node.execute())
        
        assert node.true_path == " hello world "
        assert node.false_path is False

    def test_trim_no_characters_to_trim(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_empty_string(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = ""
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_trim_only_whitespace(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "   \t\n   "
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_trim_only_specified_characters(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "xxxxxx"
        node.characters = "x"
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_trim_mixed_whitespace_and_characters(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = " x hello world x "
        node.characters = " x"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_digits(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "123hello world456"
        node.characters = "0123456789"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_punctuation(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "!!!hello world!!!"
        node.characters = "!"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_trim_non_string_text(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.characters = " "
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_trim_case_sensitive(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "AAAhello worldAAA"
        node.characters = "a"  # lowercase 'a'
        asyncio.run(node.execute())
        
        assert node.true_path == "AAAhello worldAAA"  # No trimming since case doesn't match
        assert node.false_path is False

    def test_trim_special_characters(self):
        node = StringTrim()
        node.true_path = False
        node.false_path = False
        node.text = "***hello@world***"
        node.characters = "*"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello@world"
        assert node.false_path is False