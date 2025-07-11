import unittest
from polysynergy_nodes.list.compare_lists import CompareLists

class TestCompareLists(unittest.TestCase):

    def setUp(self):
        self.node = CompareLists()
        self.node.true_path = False
        self.node.false_path = False

    def test_only_in_a(self):
        self.node.list_a = [1, 2, 3]
        self.node.list_b = [2, 3, 4]
        self.node.comparison_type = "only_in_a"
        self.node.execute()
        self.assertEqual(set(self.node.true_path), {1})
        self.assertFalse(self.node.false_path)

    def test_only_in_b(self):
        self.node.list_a = [1, 2, 3]
        self.node.list_b = [2, 3, 4]
        self.node.comparison_type = "only_in_b"
        self.node.execute()
        self.assertEqual(set(self.node.true_path), {4})
        self.assertFalse(self.node.false_path)

    def test_intersection(self):
        self.node.list_a = [1, 2, 3]
        self.node.list_b = [2, 3, 4]
        self.node.comparison_type = "intersection"
        self.node.execute()
        self.assertEqual(set(self.node.true_path), {2, 3})
        self.assertFalse(self.node.false_path)

    def test_symmetric_difference(self):
        self.node.list_a = [1, 2, 3]
        self.node.list_b = [2, 3, 4]
        self.node.comparison_type = "symmetric_difference"
        self.node.execute()
        self.assertEqual(set(self.node.true_path), {1, 4})
        self.assertFalse(self.node.false_path)

    def test_invalid_comparison_type(self):
        self.node.list_a = [1]
        self.node.list_b = [2]
        self.node.comparison_type = "not_a_real_type"
        self.node.execute()
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

if __name__ == '__main__':
    unittest.main()