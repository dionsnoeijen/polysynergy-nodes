import asyncio
import pytest
from polysynergy_nodes.boolean.boolean_and import BooleanAnd
from polysynergy_nodes.boolean.boolean_or import BooleanOr
from polysynergy_nodes.boolean.boolean_not import BooleanNot
from polysynergy_nodes.boolean.boolean_xor import BooleanXor


class TestBooleanAnd:
    def test_true_and_true(self):
        node = BooleanAnd()
        node.true_path = False
        node.false_path = False
        node.a = True
        node.b = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_true_and_false(self):
        node = BooleanAnd()
        node.true_path = False
        node.false_path = False
        node.a = True
        node.b = False
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_false_and_false(self):
        node = BooleanAnd()
        node.true_path = False
        node.false_path = False
        node.a = False
        node.b = False
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_string_coercion(self):
        node = BooleanAnd()
        node.true_path = False
        node.false_path = False
        node.a = "true"
        node.b = "hello"
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_number_coercion(self):
        node = BooleanAnd()
        node.true_path = False
        node.false_path = False
        node.a = 1
        node.b = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False


class TestBooleanOr:
    def test_true_or_false(self):
        node = BooleanOr()
        node.true_path = False
        node.false_path = False
        node.a = True
        node.b = False
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_false_or_false(self):
        node = BooleanOr()
        node.true_path = False
        node.false_path = False
        node.a = False
        node.b = False
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_false_or_true(self):
        node = BooleanOr()
        node.true_path = False
        node.false_path = False
        node.a = False
        node.b = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_string_coercion(self):
        node = BooleanOr()
        node.true_path = False
        node.false_path = False
        node.a = ""
        node.b = "false"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False


class TestBooleanNot:
    def test_not_true(self):
        node = BooleanNot()
        node.true_path = False
        node.false_path = False
        node.a = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_not_false(self):
        node = BooleanNot()
        node.true_path = False
        node.false_path = False
        node.a = False
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_not_string_empty(self):
        node = BooleanNot()
        node.true_path = False
        node.false_path = False
        node.a = ""
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_not_number(self):
        node = BooleanNot()
        node.true_path = False
        node.false_path = False
        node.a = 5
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False


class TestBooleanXor:
    def test_true_xor_false(self):
        node = BooleanXor()
        node.true_path = False
        node.false_path = False
        node.a = True
        node.b = False
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_false_xor_true(self):
        node = BooleanXor()
        node.true_path = False
        node.false_path = False
        node.a = False
        node.b = True
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False

    def test_true_xor_true(self):
        node = BooleanXor()
        node.true_path = False
        node.false_path = False
        node.a = True
        node.b = True
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_false_xor_false(self):
        node = BooleanXor()
        node.true_path = False
        node.false_path = False
        node.a = False
        node.b = False
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.false_path is False

    def test_mixed_types(self):
        node = BooleanXor()
        node.true_path = False
        node.false_path = False
        node.a = "hello"  # truthy
        node.b = 0        # falsy
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False