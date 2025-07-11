import unittest
from polysynergy_nodes.math.math_subtract import MathSubtract

class TestMathSubtractNode(unittest.TestCase):

    def setUp(self):
        self.node = MathSubtract()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_subtraction(self):
        self.node.a = 10
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, 10 - 5)
        self.assertFalse(self.node.false_path)

        self.node.a = -10
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, -10 - 5)
        self.assertFalse(self.node.false_path)

        self.node.a = 10
        self.node.b = 3.5
        self.node.execute()
        self.assertEqual(self.node.true_path, 10 - 3.5)
        self.assertFalse(self.node.false_path)

        self.node.a = 15.5
        self.node.b = 5.5
        self.node.execute()
        self.assertEqual(self.node.true_path, 15.5 - 5.5)
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.a = "ten"
        self.node.b = 5
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

        self.node.a = 10
        self.node.b = "five"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

    def test_none_input(self):
        self.node.a = None
        self.node.b = 5
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

        self.node.a = 10
        self.node.b = None
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: a or b could not be converted to number", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()