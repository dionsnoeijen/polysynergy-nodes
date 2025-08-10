import asyncio
import pytest
from polysynergy_nodes.string.string_join import StringJoin


class TestStringJoin:
    def test_join_basic_list(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello", "world", "universe"]
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello world universe"
        assert node.false_path is False

    def test_join_default_separator(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello", "world", "universe"]
        # separator defaults to ""
        asyncio.run(node.execute())
        
        assert node.true_path == "helloworlduniverse"
        assert node.false_path is False

    def test_join_comma_separator(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["apple", "banana", "orange"]
        node.separator = ", "
        asyncio.run(node.execute())
        
        assert node.true_path == "apple, banana, orange"
        assert node.false_path is False

    def test_join_empty_list(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = []
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == ""
        assert node.false_path is False

    def test_join_single_item(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello"]
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello"
        assert node.false_path is False

    def test_join_mixed_types(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello", 42, True, 3.14]
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello 42 True 3.14"
        assert node.false_path is False

    def test_join_numeric_items(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = [1, 2, 3, 4, 5]
        node.separator = "-"
        asyncio.run(node.execute())
        
        assert node.true_path == "1-2-3-4-5"
        assert node.false_path is False

    def test_join_empty_strings_in_list(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello", "", "world"]
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello  world"
        assert node.false_path is False

    def test_join_multichar_separator(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["a", "b", "c"]
        node.separator = " | "
        asyncio.run(node.execute())
        
        assert node.true_path == "a | b | c"
        assert node.false_path is False

    def test_join_special_separator(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["line1", "line2", "line3"]
        node.separator = "\n"
        asyncio.run(node.execute())
        
        assert node.true_path == "line1\nline2\nline3"
        assert node.false_path is False

    def test_join_non_list_items(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = "not a list"
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Items must be a list" in str(node.false_path)

    def test_join_non_string_separator(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello", "world"]
        node.separator = 123
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Separator must be a string" in str(node.false_path)

    def test_join_none_in_list(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = ["hello", None, "world"]
        node.separator = " "
        asyncio.run(node.execute())
        
        assert node.true_path == "hello None world"
        assert node.false_path is False

    def test_join_boolean_items(self):
        node = StringJoin()
        node.true_path = False
        node.false_path = False
        node.items = [True, False, True]
        node.separator = ","
        asyncio.run(node.execute())
        
        assert node.true_path == "True,False,True"
        assert node.false_path is False