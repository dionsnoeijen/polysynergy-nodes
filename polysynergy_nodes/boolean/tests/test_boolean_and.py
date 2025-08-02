import pytest
from polysynergy_nodes.boolean.boolean_and import BooleanAnd


class TestBooleanAnd:
    def test_and_true_true(self):
        node = BooleanAnd()
        node.a = True
        node.b = True
        node.execute()
        
        assert node.true_path is True

    def test_and_true_false(self):
        node = BooleanAnd()
        node.a = True
        node.b = False
        node.execute()
        
        assert node.true_path is False

    def test_and_false_true(self):
        node = BooleanAnd()
        node.a = False
        node.b = True
        node.execute()
        
        assert node.true_path is False

    def test_and_false_false(self):
        node = BooleanAnd()
        node.a = False
        node.b = False
        node.execute()
        
        assert node.true_path is False

    def test_and_truthy_values(self):
        node = BooleanAnd()
        node.a = "hello"  # truthy
        node.b = 1        # truthy
        node.execute()
        
        assert node.true_path is True

    def test_and_falsy_values(self):
        node = BooleanAnd()
        node.a = ""   # falsy
        node.b = 0    # falsy
        node.execute()
        
        assert node.true_path is False

    def test_and_mixed_truthy_falsy(self):
        node = BooleanAnd()
        node.a = "hello"  # truthy
        node.b = 0        # falsy
        node.execute()
        
        assert node.true_path is False