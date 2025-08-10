import unittest
from unittest.mock import Mock
from polysynergy_nodes.route.switch_case import SwitchCase


class TestSwitchCase(unittest.TestCase):

    def setUp(self):
        self.node = SwitchCase()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_success = Mock()
        self.mock_connection_success.source_handle = "cases.success"
        self.mock_connection_success.make_killer = Mock()
        
        self.mock_connection_error = Mock()
        self.mock_connection_error.source_handle = "cases.error"
        self.mock_connection_error.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "cases.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.cases = {"success": None}
        self.node.value = "success"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_exact_case_match_selects_correct_path(self):
        self.node.out_connections = [self.mock_connection_success, self.mock_connection_error]
        self.node.cases = {"success": None, "error": None}
        self.node.value = "success"
        
        self.node.execute()
        
        # Chosen connection should not be killed
        self.mock_connection_success.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_error.make_killer.assert_called_once()
        # Value should be stored in the matched case
        self.assertEqual(self.node.cases["success"], "success")

    def test_default_case_when_no_match(self):
        self.node.out_connections = [self.mock_connection_success, self.mock_connection_default]
        self.node.cases = {"success": None, "default": None}
        self.node.value = "unknown_case"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_success.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.cases["default"], "unknown_case")

    def test_no_match_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_success, self.mock_connection_error]
        self.node.cases = {"success": None, "error": None}
        self.node.value = "unknown_case"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_success.make_killer.assert_called_once()
        self.mock_connection_error.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_numeric_value_matching(self):
        self.node.out_connections = [self.mock_connection_success]
        self.mock_connection_success.source_handle = "cases.42"
        self.node.cases = {"42": None}
        self.node.value = 42
        
        self.node.execute()
        
        self.mock_connection_success.make_killer.assert_not_called()
        self.assertEqual(self.node.cases["42"], 42)

    def test_boolean_value_matching(self):
        self.node.out_connections = [self.mock_connection_success]
        self.mock_connection_success.source_handle = "cases.True"
        self.node.cases = {"True": None}
        self.node.value = True
        
        self.node.execute()
        
        self.mock_connection_success.make_killer.assert_not_called()
        self.assertEqual(self.node.cases["True"], True)

    def test_none_value_handling(self):
        # None value converts to string "None"
        self.node.out_connections = [self.mock_connection_success]
        self.mock_connection_success.source_handle = "cases.None"
        self.node.cases = {"None": None}
        self.node.value = None
        
        self.node.execute()
        
        self.mock_connection_success.make_killer.assert_not_called()
        self.assertEqual(self.node.cases["None"], None)

    def test_string_value_exact_match(self):
        # Set up connections that properly map to the case keys
        self.mock_connection_success.source_handle = "cases.pending"
        self.mock_connection_error.source_handle = "cases.completed"
        
        self.node.out_connections = [self.mock_connection_success, self.mock_connection_error]
        self.node.cases = {"pending": None, "completed": None}
        self.node.value = "completed"
        
        self.node.execute()
        
        # pending connection should be killed
        self.mock_connection_success.make_killer.assert_called_once()
        # completed connection should not be killed
        self.mock_connection_error.make_killer.assert_not_called()
        # Value should be stored in completed case
        self.assertEqual(self.node.cases["completed"], "completed")


if __name__ == "__main__":
    unittest.main()