import asyncio
import pytest
from polysynergy_nodes.string.string_index_of import StringIndexOf


class TestStringIndexOf:
    def test_index_of_found(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello world"
        node.search = "world"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == 6
        assert node.false_path is False

    def test_index_of_not_found(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello world"
        node.search = "foo"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == -1
        assert node.false_path is False

    def test_index_of_first_occurrence(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello hello world"
        node.search = "hello"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == 0
        assert node.false_path is False

    def test_index_of_last_occurrence(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello hello world"
        node.search = "hello"
        node.start = 0
        node.find_last = True
        asyncio.run(node.execute())
        
        assert node.true_path == 6
        assert node.false_path is False

    def test_index_of_with_start_position(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello hello world"
        node.search = "hello"
        node.start = 5
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == 6
        assert node.false_path is False

    def test_index_of_single_char(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello world"
        node.search = "o"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == 4
        assert node.false_path is False

    def test_index_of_empty_search(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello"
        node.search = ""
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == 0  # Empty string is found at position 0
        assert node.false_path is False

    def test_index_of_empty_text(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = ""
        node.search = "hello"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == -1
        assert node.false_path is False

    def test_index_of_case_sensitive(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "Hello World"
        node.search = "hello"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == -1  # Case sensitive
        assert node.false_path is False

    def test_index_of_non_string_text(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = 123
        node.search = "1"
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == -1
        assert "Text must be a string" in str(node.false_path)

    def test_index_of_non_string_search(self):
        node = StringIndexOf()
        node.true_path = -1
        node.false_path = False
        node.text = "hello"
        node.search = 123
        node.start = 0
        node.find_last = False
        asyncio.run(node.execute())
        
        assert node.true_path == -1
        assert "Search value must be a string" in str(node.false_path)