import unittest
from polysynergy_nodes.comparison.comparison_smaller_than import ComparisonSmallerThan

class TestComparisonSmallerThan(unittest.TestCase):

    def setUp(self):
        self.node = ComparisonSmallerThan()
        self.node.true_path = False
        self.node.false_path = False

    def test_a_smaller_than_b(self):
        self.node.a = 3
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, 3)
        self.assertFalse(self.node.false_path)

    def test_a_equal_b(self):
        self.node.a = 5
        self.node.b = 5
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertEqual(self.node.false_path, 5)

    def test_a_larger_than_b(self):
        self.node.a = 10
        self.node.b = 5
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertEqual(self.node.false_path, 5)

    def test_string_input(self):
        self.node.a = "2"
        self.node.b = "10"
        self.node.execute()
        self.assertEqual(self.node.true_path, "2")
        self.assertFalse(self.node.false_path)

    def test_invalid_input(self):
        self.node.a = "abc"
        self.node.b = 5
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertTrue(self.node.false_path)

    def test_none_input(self):
        self.node.a = None
        self.node.b = 5
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertTrue(self.node.false_path)

if __name__ == '__main__':
    unittest.main()