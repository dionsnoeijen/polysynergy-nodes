import asyncio
import unittest
from polysynergy_nodes.variable.variable_float import VariableFloat


class TestVariableFloatNode(unittest.TestCase):
    def setUp(self):
        self.node = VariableFloat()

    def test_positive_float(self):
        self.node.value = 3.14159
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 3.14159)
        self.assertEqual(self.node.value, 3.14159)

    def test_negative_float(self):
        self.node.value = -2.5
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, -2.5)
        self.assertEqual(self.node.value, -2.5)

    def test_zero_float(self):
        self.node.value = 0.0
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 0.0)
        self.assertEqual(self.node.value, 0.0)

    def test_very_small_float(self):
        self.node.value = 0.000001
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 0.000001)
        self.assertEqual(self.node.value, 0.000001)

    def test_large_float(self):
        self.node.value = 123456.789
        result = asyncio.run(self.node.execute())
        
        self.assertEqual(result, 123456.789)
        self.assertEqual(self.node.value, 123456.789)


if __name__ == "__main__":
    unittest.main()