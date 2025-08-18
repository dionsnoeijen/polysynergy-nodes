import asyncio
import unittest
from polysynergy_nodes.math.math_add import MathAdd

class TestMathAddNode(unittest.TestCase):

    def setUp(self):
        self.node = MathAdd()
        self.node.true_path = False
        self.node.false_path = False

    def test_add_integers(self):
        self.node.a = 10
        self.node.b = 5
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 15)
        self.assertFalse(self.node.false_path)

    def test_add_floats(self):
        self.node.a = 3.2
        self.node.b = 2.8
        asyncio.run(self.node.execute())
        self.assertAlmostEqual(self.node.true_path, 6.0)
        self.assertFalse(self.node.false_path)

    def test_add_strings_that_represent_numbers(self):
        self.node.a = "7"
        self.node.b = "8"
        asyncio.run(self.node.execute())
        self.assertEqual(self.node.true_path, 15)
        self.assertFalse(self.node.false_path)

    def test_add_invalid_string(self):
        self.node.a = "not_a_number"
        self.node.b = 5
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertTrue(self.node.false_path)

    def test_add_none(self):
        self.node.a = None
        self.node.b = 10
        asyncio.run(self.node.execute())
        self.assertFalse(self.node.true_path)
        self.assertTrue(self.node.false_path)

if __name__ == "__main__":
    unittest.main()