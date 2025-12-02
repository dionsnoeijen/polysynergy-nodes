import logging
import unittest
from polysynergy_nodes.json.query import JsonQuery

class TestJsonQueryNode(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)
        self.node = JsonQuery()
        self.node.true_path = False
        self.node.false_path = False

    def test_query_from_dict(self):
        self.node.json_input_as_dict = {"people": [{"name": "Alice"}, {"name": "Bob"}]}
        self.node.json_input_as_string = ""
        self.node.query = "people[0].name"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Alice")

    def test_query_from_string(self):
        self.node.json_input_as_dict = {}
        self.node.json_input_as_string = '{"people": [{"name": "Alice"}, {"name": "Bob"}]}'
        self.node.query = "people[1].name"
        self.node.execute()
        self.assertEqual(self.node.true_path, "Bob")

    def test_invalid_json(self):
        self.node.json_input_as_dict = {}
        self.node.json_input_as_string = '{invalid: true}'
        self.node.query = "invalid"
        self.node.execute()
        self.assertIn("error", self.node.false_path)

    def test_missing_query_key(self):
        self.node.json_input_as_dict = {"key": "value"}
        self.node.json_input_as_string = ""
        self.node.query = "nonexistent"
        self.node.execute()
        self.assertIsNone(self.node.true_path)

    def test_query_returns_integer(self):
        self.node.json_input_as_dict = {"count": 42, "price": 99.99}
        self.node.json_input_as_string = ""
        self.node.query = "count"
        self.node.execute()
        self.assertEqual(self.node.true_path, 42)
        self.assertIsInstance(self.node.true_path, int)

    def test_query_returns_float(self):
        self.node.json_input_as_dict = {"count": 42, "price": 99.99}
        self.node.json_input_as_string = ""
        self.node.query = "price"
        self.node.execute()
        self.assertEqual(self.node.true_path, 99.99)
        self.assertIsInstance(self.node.true_path, float)

    def test_query_returns_boolean(self):
        self.node.json_input_as_dict = {"active": True, "disabled": False}
        self.node.json_input_as_string = ""
        self.node.query = "active"
        self.node.execute()
        self.assertEqual(self.node.true_path, True)
        self.assertIsInstance(self.node.true_path, bool)

if __name__ == '__main__':
    unittest.main()
