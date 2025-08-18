import asyncio
import unittest
from polysynergy_nodes.math.math_absolute import MathAbsolute

class TestMathAbsolute(unittest.TestCase):

    def setUp(self):
        self.node = MathAbsolute()
        self.node.true_path = False
        self.node.false_path = False

    def test_positive_number(self):
        self.node.value = 5
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 5)
        self.assertFalse(self.node.false_path)

    def test_negative_number(self):
        self.node.value = -7
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 7)
        self.assertFalse(self.node.false_path)

    def test_string_number(self):
        self.node.value = "-12"
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 12)
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.value = "abc"
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()