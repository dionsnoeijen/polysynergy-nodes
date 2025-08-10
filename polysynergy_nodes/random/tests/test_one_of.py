import asyncio
import unittest
from polysynergy_nodes.random.one_of import OneOf

class TestOneOfNode(unittest.TestCase):

    def setUp(self):
        self.node = OneOf()
        self.node.true_path = False
        self.node.false_path = False

    def test_valid_selection(self):
        self.node.values = [1, 2, 3, "apple", "banana"]
        asyncio.run(self.node.execute())

        self.assertIn(self.node.true_path, [1, 2, 3, "apple", "banana"])
        self.assertFalse(self.node.false_path)

    def test_empty_list(self):
        self.node.values = []
        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIsNotNone(self.node.false_path)

    def test_non_list_input(self):
        self.node.values = "not a list"
        asyncio.run(self.node.execute())

        self.assertFalse(self.node.true_path)
        self.assertIsNotNone(self.node.false_path)

    def test_single_value_list(self):
        self.node.values = [10]
        asyncio.run(self.node.execute())

        self.assertEqual(self.node.true_path, 10)
        self.assertFalse(self.node.false_path)

if __name__ == "__main__":
    unittest.main()