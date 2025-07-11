import unittest
from polysynergy_nodes.comparison.comparison_not_equal import ComparisonNotEqual

class TestComparisonNotEqual(unittest.TestCase):

    def setUp(self):
        self.node = ComparisonNotEqual()
        self.node.true_path = False
        self.node.false_path = False

    def test_numeric_not_equal(self):
        self.node.a = 10
        self.node.b = 5
        self.node.execute()
        self.assertEqual(self.node.true_path, 10)
        self.assertFalse(self.node.false_path)

    def test_numeric_equal(self):
        self.node.a = 10
        self.node.b = 10
        self.node.execute()
        self.assertEqual(self.node.false_path, 10)
        self.assertFalse(self.node.true_path)

    def test_string_vs_int(self):
        self.node.a = "10"
        self.node.b = 10
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertEqual(self.node.false_path, 10)

    def test_bool_vs_string(self):
        self.node.a = "true"
        self.node.b = True
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertEqual(self.node.false_path, True)

    def test_different_types(self):
        self.node.a = "hello"
        self.node.b = "world"
        self.node.execute()
        self.assertEqual(self.node.true_path, "hello")
        self.assertFalse(self.node.false_path)

    def test_none_value(self):
        self.node.a = None
        self.node.b = "value"
        self.node.execute()
        self.assertEqual(self.node.true_path, None)
        self.assertFalse(self.node.false_path)

if __name__ == "__main__":
    unittest.main()