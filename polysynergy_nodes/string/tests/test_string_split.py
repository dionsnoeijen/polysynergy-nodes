import asyncio
import pytest
from polysynergy_nodes.string.string_split import StringSplit


class TestStringSplit:
    def test_split_basic_space(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "hello world universe"
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == ["hello", "world", "universe"]
        assert node.false_path is False

    def test_split_default_separator(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "hello world universe"
        # separator defaults to " "
        asyncio.run(node.execute())
        
        assert node.true_path == ["hello", "world", "universe"]
        assert node.false_path is False

    def test_split_comma_separator(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "apple,banana,orange"
        node.separator = ","
        asyncio.run(node.execute())
        
        assert node.true_path == ["apple", "banana", "orange"]
        assert node.false_path is False

    def test_split_with_max_split(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "a-b-c-d-e"
        node.separator = "-"
        node.max_split = 2
        asyncio.run(node.execute())
        
        assert node.true_path == ["a", "b", "c-d-e"]
        assert node.false_path is False

    def test_split_no_separator_found(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.separator = ","
        asyncio.run(node.execute())
        
        assert node.true_path == ["hello world"]
        assert node.false_path is False

    def test_split_empty_string(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == [""]
        assert node.false_path is False

    def test_split_multichar_separator(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "hello::world::universe"
        node.separator = "::"
        asyncio.run(node.execute())
        
        assert node.true_path == ["hello", "world", "universe"]
        assert node.false_path is False

    def test_split_consecutive_separators(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "hello  world"  # Double space
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == ["hello", "", "world"]
        assert node.false_path is False

    def test_split_max_split_unlimited(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "a-b-c-d-e"
        node.separator = "-"
        node.max_split = -1  # Unlimited
        asyncio.run(node.execute())
        
        assert node.true_path == ["a", "b", "c", "d", "e"]
        assert node.false_path is False

    def test_split_max_split_zero(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "a-b-c"
        node.separator = "-"
        node.max_split = 0
        asyncio.run(node.execute())
        
        assert node.true_path == ["a-b-c"]
        assert node.false_path is False

    def test_split_non_string_text(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_split_non_string_separator(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.separator = 123
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Separator must be a string" in str(node.false_path)

    def test_split_newlines(self):
        node = StringSplit()
        node.true_path = False
        node.false_path = False
        node.text = "line1\nline2\nline3"
        node.separator = "\n"
        asyncio.run(node.execute())
        
        assert node.true_path == ["line1", "line2", "line3"]
        assert node.false_path is False