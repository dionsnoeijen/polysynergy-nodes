import unittest
from polysynergy_nodes.math.math_clamp import MathClamp

class TestMathClampNode(unittest.TestCase):
    def setUp(self):
        self.node = MathClamp()
        self.node.true_path = False
        self.node.false_path = False

    def test_clamp_within_bounds(self):
        self.node.value = 50
        self.node.min_value = 0
        self.node.max_value = 100
        self.node.execute()
        self.assertEqual(self.node.true_path, 50)
        self.assertFalse(self.node.false_path)

    def test_clamp_below_min(self):
        self.node.value = -10
        self.node.min_value = 0
        self.node.max_value = 100
        self.node.execute()
        self.assertEqual(self.node.true_path, 0)
        self.assertFalse(self.node.false_path)

    def test_clamp_above_max(self):
        self.node.value = 150
        self.node.min_value = 0
        self.node.max_value = 100
        self.node.execute()
        self.assertEqual(self.node.true_path, 100)
        self.assertFalse(self.node.false_path)

    def test_clamp_with_strings(self):
        self.node.value = "75"
        self.node.min_value = "50"
        self.node.max_value = "100"
        self.node.execute()
        self.assertEqual(self.node.true_path, 75)
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.value = "abc"
        self.node.min_value = 0
        self.node.max_value = 100
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()