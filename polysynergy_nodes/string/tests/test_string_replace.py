import asyncio
import pytest
from polysynergy_nodes.string.string_replace import StringReplace


class TestStringReplace:
    def test_replace_basic(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.old = "world"
        node.new = "universe"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello universe"
        assert node.false_path is False

    def test_replace_multiple_occurrences(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world world"
        node.old = "world"
        node.new = "universe"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello universe universe"
        assert node.false_path is False

    def test_replace_with_count_limit(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world world world"
        node.old = "world"
        node.new = "universe"
        node.count = 2
        asyncio.run(node.execute())
        
        assert node.true_path == "hello universe universe world"
        assert node.false_path is False

    def test_replace_no_match(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.old = "foo"
        node.new = "bar"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world"
        assert node.false_path is False

    def test_replace_empty_string(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = ""
        node.old = "world"
        node.new = "universe"
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_replace_with_empty_replacement(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.old = "world"
        node.new = ""
        asyncio.run(node.execute())
        
        assert node.true_path == "hello "
        assert node.false_path is False

    def test_replace_case_sensitive(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "Hello World"
        node.old = "world"
        node.new = "universe"
        asyncio.run(node.execute())
        
        assert node.true_path == "Hello World"  # No match due to case
        assert node.false_path is False

    def test_replace_non_string_text(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = 123
        node.old = "1"
        node.new = "2"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_replace_non_string_old(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.old = 123
        node.new = "universe"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Find value must be a string" in str(node.false_path)

    def test_replace_non_string_new(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world"
        node.old = "world"
        node.new = 123
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Replace value must be a string" in str(node.false_path)

    def test_replace_count_zero(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello world world"
        node.old = "world"
        node.new = "universe"
        node.count = 0
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world world"  # No replacements made
        assert node.false_path is False

    def test_replace_special_characters(self):
        node = StringReplace()
        node.true_path = False
        node.false_path = False
        node.text = "hello@world.com"
        node.old = "@"
        node.new = "_at_"
        asyncio.run(node.execute())
        
        assert node.true_path == "hello_at_world.com"
        assert node.false_path is False