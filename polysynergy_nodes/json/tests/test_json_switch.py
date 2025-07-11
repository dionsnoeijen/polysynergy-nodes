import unittest
from unittest.mock import MagicMock
from polysynergy_nodes.json.json_switch import Switch

class TestSwitchNode(unittest.TestCase):

    def setUp(self):
        self.node = Switch()
        self.node.false_path = False
        self.node.out_connections = []

    def test_branch_match(self):
        self.node.json_as_dict = {"type": "apple", "data": {"a": 1}}
        self.node.json_path = "type"
        self.node.branches = {
            "apple": None,
            "banana": None
        }

        conn_apple = MagicMock()
        conn_apple.source_handle = "branches.apple"
        conn_banana = MagicMock()
        conn_banana.source_handle = "branches.banana"

        self.node.out_connections = [conn_apple, conn_banana]
        self.node.execute()

        conn_apple.make_killer.assert_not_called()
        conn_banana.make_killer.assert_called_once()
        self.assertEqual(self.node.branches["apple"], {"type": "apple", "data": {"a": 1}})

    def test_branch_no_match(self):
        self.node.json_as_dict = {"type": "grape"}
        self.node.json_path = "type"
        self.node.branches = {
            "apple": None,
            "banana": None
        }

        conn_apple = MagicMock()
        conn_apple.source_handle = "branches.apple"
        conn_banana = MagicMock()
        conn_banana.source_handle = "branches.banana"

        self.node.out_connections = [conn_apple, conn_banana]
        self.node.execute()

        conn_apple.make_killer.assert_called_once()
        conn_banana.make_killer.assert_called_once()

    def test_invalid_json_string(self):
        self.node.json_as_dict = None
        self.node.json_as_string = "{invalid}"
        self.node.json_path = "type"
        self.node.branches = {}
        self.node.execute()

        self.assertIn("error", self.node.false_path)

    def test_missing_value_to_check(self):
        self.node.json_as_dict = {"something": "else"}
        self.node.json_path = "type"
        self.node.branches = {}
        self.node.execute()

        self.assertIn("error", self.node.false_path)

if __name__ == "__main__":
    unittest.main()