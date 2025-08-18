import asyncio
import unittest
from polysynergy_nodes.math.math_power import MathPower

class TestMathPowerNode(unittest.TestCase):

    def setUp(self):
        self.node = MathPower()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_power(self):
        self.node.a = 2
        self.node.b = 3
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 2 ** 3)
        self.assertFalse(self.node.false_path)

        self.node.a = 2
        self.node.b = -3
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 2 ** -3)
        self.assertFalse(self.node.false_path)

        self.node.a = 9
        self.node.b = 0.5
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 9 ** 0.5)
        self.assertFalse(self.node.false_path)

        self.node.a = 5
        self.node.b = 0
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 5 ** 0)
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.a = "ten"
        self.node.b = 3
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

        self.node.a = 2
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

        self.node.a = 2
        self.node.b = None
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()