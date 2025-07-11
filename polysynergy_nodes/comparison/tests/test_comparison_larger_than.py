import unittest
from polysynergy_nodes.comparison.comparison_larger_than import ComparisonLargerThan

class TestComparisonLargerThanNode(unittest.TestCase):

    def setUp(self):
        self.node = ComparisonLargerThan()
        self.node.true_path = False
        self.node.false_path = False

    def test_int_larger_than(self):
        self.node.a = 10
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, 10)
        self.assertFalse(self.node.false_path)

    def test_int_not_larger_than(self):
        self.node.a = 3
        self.node.b = 8
        self.node.execute()
        self.assertEqual(self.node.false_path, 8)
        self.assertFalse(self.node.true_path)

    def test_equal_values(self):
        self.node.a = 7
        self.node.b = 7
        self.node.execute()
        self.assertEqual(self.node.false_path, 7)
        self.assertFalse(self.node.true_path)

    def test_float_comparison(self):
        self.node.a = 5.5
        self.node.b = 2.2
        self.node.execute()
        self.assertEqual(self.node.true_path, 5.5)
        self.assertFalse(self.node.false_path)

    def test_string_numeric_comparison(self):
        self.node.a = "9"
        self.node.b = "3"
        self.node.execute()
        self.assertEqual(self.node.true_path, "9")
        self.assertFalse(self.node.false_path)

    def test_invalid_string_input(self):
        self.node.a = "abc"
        self.node.b = 5
        self.node.execute()
        self.assertTrue(self.node.false_path)
        self.assertFalse(self.node.true_path)

    def test_invalid_both(self):
        self.node.a = "abc"
        self.node.b = "xyz"
        self.node.execute()
        self.assertTrue(self.node.false_path)
        self.assertFalse(self.node.true_path)

if __name__ == "__main__":
    unittest.main()