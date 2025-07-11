import unittest
from polysynergy_nodes.list.unique_list import UniqueList

class TestUniqueListNode(unittest.TestCase):

    def setUp(self):
        self.node = UniqueList()
        self.node.true_path = False
        self.node.false_path = False

    def test_unique_simple_list(self):
        self.node.input_list = [1, 2, 2, 3, 3, 3]
        self.node.execute()
        self.assertEqual(self.node.true_path, [1, 2, 3])
        self.assertFalse(self.node.false_path)

    def test_unique_dict_list_by_key(self):
        self.node.input_list = [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
            {"id": 1, "name": "A"},
            {"id": 3, "name": "C"},
        ]
        self.node.key = "id"
        self.node.execute()
        self.assertEqual(
            self.node.true_path,
            [
                {"id": 1, "name": "A"},
                {"id": 2, "name": "B"},
                {"id": 3, "name": "C"},
            ]
        )

    def test_unique_with_invalid_input(self):
        self.node.input_list = "not a list"
        self.node.execute()
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()
