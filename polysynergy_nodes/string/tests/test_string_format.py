import asyncio
import pytest
from polysynergy_nodes.string.string_format import StringFormat


class TestStringFormat:
    def test_format_with_dict(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "Hello {name}, you are {age} years old"
        node.values = {"name": "Alice", "age": 30}
        asyncio.run(node.execute())
        
        assert node.true_path == "Hello Alice, you are 30 years old"
        assert node.false_path is False

    def test_format_with_list(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "The {} is {} and {}"
        node.values = ["sky", "blue", "beautiful"]
        asyncio.run(node.execute())
        
        assert node.true_path == "The sky is blue and beautiful"
        assert node.false_path is False

    def test_format_numbered_placeholders(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "{0} {1} {0}"
        node.values = ["hello", "world"]
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world hello"
        assert node.false_path is False

    def test_format_empty_template(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = ""
        node.values = {"key": "value"}
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_format_no_placeholders(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "No placeholders here"
        node.values = {"key": "value"}
        asyncio.run(node.execute())
        
        assert node.true_path == "No placeholders here"
        assert node.false_path is False

    def test_format_missing_key(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "Hello {name}"
        node.values = {"age": 30}
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is not False

    def test_format_missing_index(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "Item {0} and {1}"
        node.values = ["first"]
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is not False

    def test_format_non_string_template(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = 123
        node.values = {"key": "value"}
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Template must be a string" in str(node.false_path)

    def test_format_invalid_values_type(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "Hello {}"
        node.values = "not a dict or list"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Values must be a dictionary or list" in str(node.false_path)

    def test_format_mixed_types_in_dict(self):
        node = StringFormat()
        node.true_path = False
        node.false_path = False
        node.template = "{str} {num} {bool}"
        node.values = {"str": "text", "num": 42, "bool": True}
        asyncio.run(node.execute())
        
        assert node.true_path == "text 42 True"
        assert node.false_path is False