import unittest
from polysynergy_nodes.list.contains_list import ContainsList

class TestContainsInListNode(unittest.TestCase):

    def setUp(self):
        self.node = ContainsList()
        self.node.true_path = False
        self.node.false_path = False

    def test_simple_contains_true(self):
        self.node.input_list = ["apple", "banana", "cherry"]
        self.node.match_value = "banana"
        self.node.execute()
        self.assertTrue(self.node.true_path)
        self.assertFalse(self.node.false_path)

    def test_simple_contains_false(self):
        self.node.input_list = ["apple", "banana", "cherry"]
        self.node.value_to_find = "orange"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertTrue(self.node.false_path)

    def test_contains_key_value_match(self):
        self.node.input_list = [{"id": 1}, {"id": 2}]
        self.node.match_value = 2
        self.node.key = "id"  # <-- Cruciaal!
        self.node.execute()
        self.assertTrue(self.node.true_path)

    def test_contains_key_value_not_match(self):
        self.node.input_list = [{"name": "Alice"}, {"name": "Bob"}]
        self.node.key_field = "name"
        self.node.value_to_find = "Charlie"
        self.node.execute()
        self.assertFalse(self.node.true_path)
        self.assertTrue(self.node.false_path)

    def test_invalid_input(self):
        self.node.input_list = "not a list"
        self.node.value_to_find = "value"
        self.node.execute()
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)

if __name__ == '__main__':
    unittest.main()