import unittest
from polysynergy_nodes.math.math_round import MathRound

class TestMathRoundNode(unittest.TestCase):

    def setUp(self):
        self.node = MathRound()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_round(self):
        self.node.value = 10.5678
        self.node.decimals = 2
        self.node.execute()
        self.assertEqual(self.node.true_path, round(10.5678, 2))  # Verwachte uitkomst: 10.57
        self.assertFalse(self.node.false_path)

        self.node.value = -10.5678
        self.node.decimals = 2
        self.node.execute()
        self.assertEqual(self.node.true_path, round(-10.5678, 2))  # Verwachte uitkomst: -10.57
        self.assertFalse(self.node.false_path)

        self.node.value = 10
        self.node.decimals = 2
        self.node.execute()
        self.assertEqual(self.node.true_path, round(10, 2))  # Verwachte uitkomst: 10
        self.assertFalse(self.node.false_path)

        self.node.value = 10.5678
        self.node.decimals = 0
        self.node.execute()
        self.assertEqual(self.node.true_path, round(10.5678, 0))  # Verwachte uitkomst: 11
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.value = "ten"
        self.node.decimals = 2
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: value or decimals could not be converted to number", self.node.false_path["error"])

        self.node.value = 10.5678
        self.node.decimals = "two"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: value or decimals could not be converted to number", self.node.false_path["error"])

    def test_none_input(self):
        self.node.value = None
        self.node.decimals = 2
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: value or decimals could not be converted to number", self.node.false_path["error"])

        self.node.value = 10.5678
        self.node.decimals = None
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Invalid input: value or decimals could not be converted to number", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()