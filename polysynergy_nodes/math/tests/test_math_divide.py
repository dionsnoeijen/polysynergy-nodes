import unittest
from polysynergy_nodes.math.math_divide import MathDivide

class TestMathDivideNode(unittest.TestCase):

    def setUp(self):
        self.node = MathDivide()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_division(self):
        self.node.a = 10
        self.node.b = 2
        self.node.execute()
        self.assertEqual(self.node.true_path, 5.0)
        self.assertFalse(self.node.false_path)

    def test_zero_division(self):
        self.node.a = 10
        self.node.b = 0
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Division by zero", self.node.false_path["error"])

    def test_invalid_input(self):
        self.node.a = "ten"
        self.node.b = 2
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("could not be converted", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()