import pytest
from polysynergy_nodes.string.string_length import StringLength


class TestStringLength:
    def test_string_length_basic(self):
        node = StringLength()
        node.text = "hello"
        node.execute()
        
        assert node.true_path == 5
        assert node.false_path is None

    def test_string_length_empty(self):
        node = StringLength()
        node.text = ""
        node.execute()
        
        assert node.true_path == 0
        assert node.false_path is None

    def test_string_length_unicode(self):
        node = StringLength()
        node.text = "héllo wörld 🚀"
        node.execute()
        
        assert node.true_path == 13
        assert node.false_path is None

    def test_string_length_non_string_input(self):
        node = StringLength()
        node.text = 123
        node.execute()
        
        assert node.true_path is False
        assert "Input must be a string" in str(node.false_path)