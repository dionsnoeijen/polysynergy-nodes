import unittest
from polysynergy_nodes.list.merge_list import MergeLists

class TestMergeListsNode(unittest.TestCase):

    def setUp(self):
        self.node = MergeLists()
        self.node.true_path = False
        self.node.false_path = False

    def test_merge_two_lists(self):
        self.node.list_a = [1, 2, 3]
        self.node.list_b = [4, 5, 6]
        self.node.execute()
        self.assertEqual(self.node.true_path, [1, 2, 3, 4, 5, 6])
        self.assertFalse(self.node.false_path)

    def test_merge_empty_and_list(self):
        self.node.list_a = []
        self.node.list_b = ["a", "b"]
        self.node.execute()
        self.assertEqual(self.node.true_path, ["a", "b"])

    def test_merge_list_and_empty(self):
        self.node.list_a = ["x"]
        self.node.list_b = []
        self.node.execute()
        self.assertEqual(self.node.true_path, ["x"])

    def test_invalid_input_a(self):
        self.node.list_a = "not a list"
        self.node.list_b = [1]
        self.node.execute()
        self.assertIn("error", self.node.false_path)

    def test_invalid_input_b(self):
        self.node.list_a = [1]
        self.node.list_b = None
        self.node.execute()
        self.assertIn("error", self.node.false_path)

if __name__ == '__main__':
    unittest.main()
