import unittest
from polysynergy_nodes.math.math_ceil import MathCeil

class TestMathCeil(unittest.TestCase):

    def setUp(self):
        self.node = MathCeil()

    def test_ceil_with_integer(self):
        self.node.value = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, 5)
        self.assertFalse(self.node.false_path)

    def test_ceil_with_float(self):
        self.node.value = 5.2
        self.node.execute()
        self.assertEqual(self.node.true_path, 6)
        self.assertFalse(self.node.false_path)

    def test_ceil_with_string_number(self):
        self.node.value = "4.7"
        self.node.execute()
        self.assertEqual(self.node.true_path, 5)
        self.assertFalse(self.node.false_path)

    def test_ceil_with_invalid_string(self):
        self.node.value = "not_a_number"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()