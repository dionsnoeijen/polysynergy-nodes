import asyncio
import unittest
from polysynergy_nodes.variable.variable_integer import VariableInteger


class TestVariableIntegerNode(unittest.TestCase):
    def setUp(self):
        self.node = VariableInteger()

    def test_positive_integer(self):
        self.node.value = 42
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 42)

    def test_negative_integer(self):
        self.node.value = -15
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, -15)

    def test_zero(self):
        self.node.value = 0
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 0)

    def test_large_integer(self):
        self.node.value = 999999999
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 999999999)

    def test_string_conversion(self):
        self.node.value = "123"
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 123)

    def test_float_string_conversion(self):
        self.node.value = "123.7"
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 123)

    def test_placeholder_replacement(self):
        self.node.value = "{{count}}"
        self.node.values = {"count": "42"}
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 42)


if __name__ == "__main__":
    unittest.main()