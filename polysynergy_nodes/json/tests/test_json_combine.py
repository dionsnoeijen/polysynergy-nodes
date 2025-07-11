import unittest
from polysynergy_nodes.json.combine import JsonCombine

class TestJsonCombineNode(unittest.TestCase):

    def setUp(self):
        self.node = JsonCombine()
        self.node.true_path = False
        self.node.false_path = False

    def test_combine_valid_dicts(self):
        self.node.combine = {
            "a": {"key1": "value1"},
            "b": {"key2": "value2"},
        }
        self.node.execute()
        self.assertEqual(self.node.true_path, {"key1": "value1", "key2": "value2"})
        self.assertFalse(self.node.false_path)

    def test_ignore_empty_dict(self):
        self.node.combine = {
            "a": {"x": 1},
            "b": {},
        }
        self.node.execute()
        self.assertEqual(self.node.true_path, {"x": 1})
        self.assertFalse(self.node.false_path)

    def test_error_on_non_dict_value(self):
        self.node.combine = {
            "a": {"key": "val"},
            "b": "not a dict",
        }
        self.node.execute()
        self.assertTrue(isinstance(self.node.false_path, dict))
        self.assertIn("error", self.node.false_path)

if __name__ == '__main__':
    unittest.main()
