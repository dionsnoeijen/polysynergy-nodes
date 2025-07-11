import unittest
from polysynergy_nodes.list.count_list import CountList

class TestCountListNode(unittest.TestCase):

    def setUp(self):
        self.node = CountList()
        self.node.true_path = False
        self.node.false_path = False

    def test_non_empty_list(self):
        self.node.input_list = [1, 2, 3]
        self.node.execute()
        self.assertEqual(self.node.true_path, 3)
        self.assertFalse(self.node.false_path)

    def test_empty_list(self):
        self.node.input_list = []
        self.node.execute()
        self.assertEqual(self.node.false_path, True)
        self.assertFalse(self.node.true_path)

if __name__ == '__main__':
    unittest.main()
