import unittest
from polysynergy_nodes.list.sort_list import SortList

class TestSortListNode(unittest.TestCase):

    def setUp(self):
        self.node = SortList()
        self.node.true_path = False
        self.node.false_path = False

    def test_sort_numbers_ascending(self):
        self.node.input_list = [5, 2, 9, 1]
        self.node.sort_order = "asc"
        self.node.execute()
        self.assertEqual(self.node.true_path, [1, 2, 5, 9])

    def test_sort_numbers_descending(self):
        self.node.input_list = [5, 2, 9, 1]
        self.node.sort_order = "desc"
        self.node.execute()
        self.assertEqual(self.node.true_path, [9, 5, 2, 1])

    def test_sort_dicts_by_key_ascending(self):
        self.node.input_list = [{"name": "Charlie"}, {"name": "Alice"}, {"name": "Bob"}]
        self.node.sort_order = "asc"
        self.node.key = "name"
        self.node.execute()
        self.assertEqual(self.node.true_path, [{"name": "Alice"}, {"name": "Bob"}, {"name": "Charlie"}])

    def test_sort_dicts_by_key_descending(self):
        self.node.input_list = [{"score": 10}, {"score": 30}, {"score": 20}]
        self.node.sort_order = "desc"
        self.node.key = "score"
        self.node.execute()
        self.assertEqual(self.node.true_path, [{"score": 30}, {"score": 20}, {"score": 10}])

    def test_invalid_list(self):
        self.node.input_list = "not a list"
        self.node.execute()
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()