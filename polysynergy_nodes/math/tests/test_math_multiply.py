import asyncio
import unittest
from polysynergy_nodes.math.math_multiply import MathMultiply

class TestMathMultiplyNode(unittest.TestCase):

    def setUp(self):
        self.node = MathMultiply()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_multiplication(self):
        self.node.a = 10
        self.node.b = 5
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 10 * 5)
        self.assertFalse(self.node.false_path)

        self.node.a = -10
        self.node.b = 5
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, -10 * 5)
        self.assertFalse(self.node.false_path)

        # Test met een integer en een float
        self.node.a = 5
        self.node.b = 3.2
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 5 * 3.2)
        self.assertFalse(self.node.false_path)

        # Test met float-getallen
        self.node.a = 10.5
        self.node.b = 2.0
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 10.5 * 2.0)
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.a = "ten"
        self.node.b = 5
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

        self.node.a = 10
        self.node.b = "five"
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

    def test_none_input(self):
        self.node.a = None
        self.node.b = 5
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

        self.node.a = 10
        self.node.b = None
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()