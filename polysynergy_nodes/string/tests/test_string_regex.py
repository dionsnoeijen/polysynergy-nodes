import asyncio
import pytest
from polysynergy_nodes.string.string_regex import StringRegex


class TestStringRegex:
    def test_regex_match_true(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "hello123"
        node.pattern = r"^hello\d+$"
        node.operation = "match"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_regex_match_false(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.pattern = r"^\d+$"
        node.operation = "match"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_regex_search(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "The year is 2024"
        node.pattern = r"\d{4}"
        node.operation = "search"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path == "2024"
        assert node.false_path is False

    def test_regex_search_not_found(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "No numbers here"
        node.pattern = r"\d+"
        node.operation = "search"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path is None
        assert node.false_path is False

    def test_regex_findall(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "Phone: 123-456-7890, Fax: 098-765-4321"
        node.pattern = r"\d{3}-\d{3}-\d{4}"
        node.operation = "findall"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path == ["123-456-7890", "098-765-4321"]
        assert node.false_path is False

    def test_regex_split(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "apple,banana;orange|grape"
        node.pattern = r"[,;|]"
        node.operation = "split"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path == ["apple", "banana", "orange", "grape"]
        assert node.false_path is False

    def test_regex_replace(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "The price is $123.45"
        node.pattern = r"\$\d+\.\d{2}"
        node.operation = "replace"
        node.replacement = "REDACTED"
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path == "The price is REDACTED"
        assert node.false_path is False

    def test_regex_ignore_case_flag(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "Hello WORLD"
        node.pattern = r"hello"
        node.operation = "search"
        node.replacement = ""
        node.flags = "ignorecase"
        asyncio.run(node.execute())
        
        assert node.true_path == "Hello"
        assert node.false_path is False

    def test_regex_multiline_flag(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "line1\nline2\nline3"
        node.pattern = r"^line\d"
        node.operation = "findall"
        node.replacement = ""
        node.flags = "multiline"
        asyncio.run(node.execute())
        
        assert node.true_path == ["line1", "line2", "line3"]
        assert node.false_path is False

    def test_regex_dotall_flag(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "line1\nline2"
        node.pattern = r"line1.*line2"
        node.operation = "search"
        node.replacement = ""
        node.flags = "dotall"
        asyncio.run(node.execute())
        
        assert node.true_path == "line1\nline2"
        assert node.false_path is False

    def test_regex_invalid_pattern(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = "hello"
        node.pattern = r"[invalid"  # Unclosed bracket
        node.operation = "search"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Regex error" in str(node.false_path)

    def test_regex_non_string_text(self):
        node = StringRegex()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.pattern = r"\d+"
        node.operation = "search"
        node.replacement = ""
        node.flags = "none"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)