import asyncio
import unittest
from polysynergy_nodes.variable.variable_float import VariableFloat


class TestVariableFloatNode(unittest.TestCase):
    def setUp(self):
        self.node = VariableFloat()

    def test_positive_float(self):
        self.node.value = 3.14159
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 3.14159)

    def test_negative_float(self):
        self.node.value = -2.5
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, -2.5)

    def test_zero_float(self):
        self.node.value = 0.0
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 0.0)

    def test_very_small_float(self):
        self.node.value = 0.000001
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 0.000001)

    def test_large_float(self):
        self.node.value = 123456.789
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 123456.789)

    def test_string_conversion(self):
        self.node.value = "123.45"
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 123.45)

    def test_integer_conversion(self):
        self.node.value = 42
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 42.0)

    def test_placeholder_replacement(self):
        self.node.value = "{{price}}"
        self.node.values = {"price": "99.99"}
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 99.99)


if __name__ == "__main__":
    unittest.main()