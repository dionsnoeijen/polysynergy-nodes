import asyncio
import pytest
from polysynergy_nodes.string.string_case import StringCase


class TestStringCase:
    def test_case_uppercase(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == "HELLO WORLD"
        assert node.false_path is False

    def test_case_lowercase(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "HELLO WORLD"
        node.case_type = "lower"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_case_title_case(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "hello world universe"
        node.case_type = "title"
        asyncio.run(node.execute())
        
        assert node.true_path == "Hello World Universe"
        assert node.false_path is False

    def test_case_capitalize(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "hello world universe"
        node.case_type = "capitalize"
        asyncio.run(node.execute())
        
        assert node.true_path == "Hello world universe"
        assert node.false_path is False

    def test_case_default_lowercase(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "HELLO WORLD"
        # case_type defaults to "lower"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_case_mixed_case_to_upper(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "HeLLo WoRLd"
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == "HELLO WORLD"
        assert node.false_path is False

    def test_case_mixed_case_to_lower(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "HeLLo WoRLd"
        node.case_type = "lower"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_case_empty_string(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_case_numbers_and_symbols(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "hello123!@# world"
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == "HELLO123!@# WORLD"
        assert node.false_path is False

    def test_case_unicode_characters(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "héllo wörld"
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == "HÉLLO WÖRLD"
        assert node.false_path is False

    def test_case_title_with_apostrophes(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "don't stop believing"
        node.case_type = "title"
        asyncio.run(node.execute())
        
        assert node.true_path == "Don'T Stop Believing"
        assert node.false_path is False

    def test_case_capitalize_already_capitalized(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "Hello world"
        node.case_type = "capitalize"
        asyncio.run(node.execute())
        
        assert node.true_path == "Hello world"
        assert node.false_path is False

    def test_case_title_short_words(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "a b c d"
        node.case_type = "title"
        asyncio.run(node.execute())
        
        assert node.true_path == "A B C D"
        assert node.false_path is False

    def test_case_invalid_case_type(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.case_type = "invalid_type"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Invalid case type: invalid_type" in str(node.false_path)

    def test_case_non_string_text(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_case_preserve_whitespace(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "  hello   world  "
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == "  HELLO   WORLD  "
        assert node.false_path is False

    def test_case_newlines_and_tabs(self):
        node = StringCase()
        node.true_path = False
        node.false_path = False
        node.text = "hello\nworld\ttest"
        node.case_type = "upper"
        asyncio.run(node.execute())
        
        assert node.true_path == "HELLO\nWORLD\tTEST"
        assert node.false_path is False