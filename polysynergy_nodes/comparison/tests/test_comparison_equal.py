import unittest
from polysynergy_nodes.comparison.comparison_equal import ComparisonEqual

class TestComparisonEqualNode(unittest.TestCase):

    def setUp(self):
        self.node = ComparisonEqual()
        self.node.true_path = False
        self.node.false_path = False

    def test_equal_integers(self):
        self.node.a = 5
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, 5)
        self.assertFalse(self.node.false_path)

    def test_equal_string_and_integer(self):
        self.node.a = "5"
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, "5")
        self.assertFalse(self.node.false_path)

    def test_not_equal(self):
        self.node.a = 5
        self.node.b = 6
        self.node.execute()
        self.assertEqual(self.node.false_path, 6)
        self.assertFalse(self.node.true_path)

    def test_boolean_true_equal(self):
        self.node.a = "true"
        self.node.b = True
        self.node.execute()
        self.assertEqual(self.node.true_path, "true")
        self.assertFalse(self.node.false_path)

    def test_boolean_false_equal(self):
        self.node.a = False
        self.node.b = "false"
        self.node.execute()
        self.assertEqual(self.node.true_path, False)
        self.assertFalse(self.node.false_path)

    def test_mismatched_types_not_equal(self):
        self.node.a = "abc"
        self.node.b = 123
        self.node.execute()
        self.assertEqual(self.node.false_path, 123)
        self.assertFalse(self.node.true_path)

if __name__ == '__main__':
    unittest.main()