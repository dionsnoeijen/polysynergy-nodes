import pytest
from polysynergy_nodes.string.string_contains import StringContains


class TestStringContains:
    def test_contains_basic_true(self):
        node = StringContains()
        node.text = "hello world"
        node.search = "world"
        node.execute()
        
        assert node.true_path is True
        assert node.false_path is None

    def test_contains_basic_false(self):
        node = StringContains()
        node.text = "hello world"
        node.search = "foo"
        node.execute()
        
        assert node.true_path is False
        assert node.false_path is None

    def test_contains_case_sensitive_true(self):
        node = StringContains()
        node.text = "Hello World"
        node.search = "Hello"
        node.case_sensitive = True
        node.execute()
        
        assert node.true_path is True

    def test_contains_case_sensitive_false(self):
        node = StringContains()
        node.text = "Hello World"
        node.search = "hello"
        node.case_sensitive = True
        node.execute()
        
        assert node.true_path is False

    def test_contains_case_insensitive(self):
        node = StringContains()
        node.text = "Hello World"
        node.search = "hello"
        node.case_sensitive = False
        node.execute()
        
        assert node.true_path is True

    def test_contains_non_string_text(self):
        node = StringContains()
        node.text = 123
        node.search = "1"
        node.execute()
        
        assert node.true_path is False
        assert "Text must be a string" in str(node.false_path)

    def test_contains_non_string_search(self):
        node = StringContains()
        node.text = "hello"
        node.search = 123
        node.execute()
        
        assert node.true_path is False
        assert "Search value must be a string" in str(node.false_path)