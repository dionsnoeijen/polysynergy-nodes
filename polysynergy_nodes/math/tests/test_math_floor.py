import unittest
import math
from polysynergy_nodes.math.math_floor import MathFloor

class TestMathFloorNode(unittest.TestCase):

    def setUp(self):
        self.node = MathFloor()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_floor(self):
        self.node.value = 10.7
        self.node.execute()
        self.assertEqual(self.node.true_path, math.floor(10.7))  # Verwachte vloerwaarde: 10
        self.assertFalse(self.node.false_path)

        self.node.value = -10.7
        self.node.execute()
        self.assertEqual(self.node.true_path, math.floor(-10.7))  # Verwachte vloerwaarde: -11
        self.assertFalse(self.node.false_path)

        self.node.value = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, math.floor(5))  # Verwachte vloerwaarde: 5
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.value = "ten"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Cannot convert 'ten' to number", self.node.false_path["error"])

    def test_none_input(self):
        self.node.value = None
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertIn("Cannot convert 'None' to number", self.node.false_path["error"])

if __name__ == "__main__":
    unittest.main()