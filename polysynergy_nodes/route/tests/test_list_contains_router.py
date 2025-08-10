import unittest
from unittest.mock import Mock
from polysynergy_nodes.route.list_contains_router import ListContainsRouter


class TestListContainsRouter(unittest.TestCase):

    def setUp(self):
        self.node = ListContainsRouter()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_fruits = Mock()
        self.mock_connection_fruits.source_handle = "lists.fruits"
        self.mock_connection_fruits.make_killer = Mock()
        
        self.mock_connection_colors = Mock()
        self.mock_connection_colors.source_handle = "lists.colors"
        self.mock_connection_colors.make_killer = Mock()
        
        self.mock_connection_numbers = Mock()
        self.mock_connection_numbers.source_handle = "lists.numbers"
        self.mock_connection_numbers.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "lists.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.value = "apple"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_value_found_in_first_list(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_colors]
        self.node.lists = {
            "fruits": ["apple", "banana", "orange"],
            "colors": ["red", "green", "blue"]
        }
        self.node.value = "apple"
        
        self.node.execute()
        
        # Fruits connection should not be killed
        self.mock_connection_fruits.make_killer.assert_not_called()
        # Colors connection should be killed
        self.mock_connection_colors.make_killer.assert_called_once()
        # Value should be stored in the fruits list
        self.assertEqual(self.node.lists["fruits"], "apple")

    def test_value_found_in_second_list(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_colors]
        self.node.lists = {
            "fruits": ["apple", "banana", "orange"],
            "colors": ["red", "green", "blue"]
        }
        self.node.value = "red"
        
        self.node.execute()
        
        # Colors connection should not be killed
        self.mock_connection_colors.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in the colors list
        self.assertEqual(self.node.lists["colors"], "red")

    def test_numeric_value_in_list(self):
        self.node.out_connections = [self.mock_connection_numbers, self.mock_connection_fruits]
        self.node.lists = {
            "numbers": [1, 2, 3, 4, 5],
            "fruits": ["apple", "banana", "orange"]
        }
        self.node.value = 3
        
        self.node.execute()
        
        # Numbers connection should not be killed
        self.mock_connection_numbers.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in the numbers list
        self.assertEqual(self.node.lists["numbers"], 3)

    def test_mixed_type_list_with_string_comparison(self):
        self.node.out_connections = [self.mock_connection_numbers, self.mock_connection_fruits]
        self.node.lists = {
            "numbers": [{"key": "value"}, [1, 2, 3]],  # Unhashable types
            "fruits": ["apple", "banana", "orange"]
        }
        self.node.value = {"key": "value"}
        
        self.node.execute()
        
        # Numbers connection should not be killed (string comparison fallback)
        self.mock_connection_numbers.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in the numbers list
        self.assertEqual(self.node.lists["numbers"], {"key": "value"})

    def test_default_case_when_no_match(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_default]
        self.node.lists = {
            "fruits": ["apple", "banana", "orange"],
            "default": None
        }
        self.node.value = "car"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.lists["default"], "car")

    def test_no_match_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_colors]
        self.node.lists = {
            "fruits": ["apple", "banana", "orange"],
            "colors": ["red", "green", "blue"]
        }
        self.node.value = "car"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        self.mock_connection_colors.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_empty_list_no_match(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_default]
        self.node.lists = {
            "fruits": [],
            "default": None
        }
        self.node.value = "apple"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.lists["default"], "apple")

    def test_non_list_value_no_match(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_default]
        self.node.lists = {
            "fruits": "not a list",  # String instead of list
            "default": None
        }
        self.node.value = "apple"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.lists["default"], "apple")

    def test_none_value_in_list(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_colors]
        self.node.lists = {
            "fruits": ["apple", None, "orange"],
            "colors": ["red", "green", "blue"]
        }
        self.node.value = None
        
        self.node.execute()
        
        # Fruits connection should not be killed
        self.mock_connection_fruits.make_killer.assert_not_called()
        # Colors connection should be killed
        self.mock_connection_colors.make_killer.assert_called_once()
        # Value should be stored in the fruits list
        self.assertEqual(self.node.lists["fruits"], None)

    def test_case_sensitive_string_matching(self):
        self.node.out_connections = [self.mock_connection_fruits, self.mock_connection_default]
        self.node.lists = {
            "fruits": ["Apple", "Banana", "Orange"],  # Capitalized
            "default": None
        }
        self.node.value = "apple"  # Lowercase
        
        self.node.execute()
        
        # Should not match due to case sensitivity, default should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Fruits connection should be killed
        self.mock_connection_fruits.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.lists["default"], "apple")

    def test_value_in_list_method(self):
        # Test the helper method directly
        self.assertTrue(self.node._value_in_list("apple", ["apple", "banana", "orange"]))
        self.assertFalse(self.node._value_in_list("grape", ["apple", "banana", "orange"]))
        self.assertTrue(self.node._value_in_list(1, [1, 2, 3]))
        self.assertFalse(self.node._value_in_list(4, [1, 2, 3]))
        # Test non-list input
        self.assertFalse(self.node._value_in_list("apple", "not a list"))
        self.assertFalse(self.node._value_in_list("apple", None))
        # Test unhashable types with string fallback
        test_dict = {"key": "value"}
        self.assertTrue(self.node._value_in_list(test_dict, [test_dict, "other"]))


if __name__ == "__main__":
    unittest.main()