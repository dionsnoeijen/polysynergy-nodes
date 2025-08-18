import asyncio
import unittest
from polysynergy_nodes.math.math_modulus import MathModulus

class TestMathModulusNode(unittest.TestCase):

    def setUp(self):
        self.node = MathModulus()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_modulus(self):
        self.node.a = 10
        self.node.b = 3
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 10 % 3)
        self.assertFalse(self.node.false_path)

        self.node.a = -10
        self.node.b = 3
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, -10 % 3)
        self.assertFalse(self.node.false_path)

        self.node.a = 10.5
        self.node.b = 3.2
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 10.5 % 3.2)
        self.assertFalse(self.node.false_path)

    def test_zero_division(self):
        self.node.a = 10
        self.node.b = 0
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Division by zero", self.node.false_path["error"])

    def test_invalid_input(self):
        self.node.a = "ten"
        self.node.b = 3
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

        self.node.a = 10
        self.node.b = "three"
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

    def test_none_input(self):
        self.node.a = None
        self.node.b = 3
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