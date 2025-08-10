import asyncio
import unittest
from polysynergy_nodes.variable.variable_integer import VariableInteger


class TestVariableIntegerNode(unittest.TestCase):
    def setUp(self):
        self.node = VariableInteger()

    def test_positive_integer(self):
        self.node.value = 42
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 42)
        self.assertEqual(self.node.value, 42)

    def test_negative_integer(self):
        self.node.value = -15
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, -15)
        self.assertEqual(self.node.value, -15)

    def test_zero(self):
        self.node.value = 0
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 0)
        self.assertEqual(self.node.value, 0)

    def test_large_integer(self):
        self.node.value = 999999999
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 999999999)
        self.assertEqual(self.node.value, 999999999)


if __name__ == "__main__":
    unittest.main()