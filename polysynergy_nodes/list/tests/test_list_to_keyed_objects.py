import unittest
from polysynergy_nodes.list.list_to_keyed_objects import ListToKeyedObjects


class TestListToKeyedObjectsNode(unittest.TestCase):

    def setUp(self):
        self.node = ListToKeyedObjects()
        self.node.true_path = False
        self.node.false_path = False

    def test_basic_transformation(self):
        """Test basic list to keyed objects transformation"""
        self.node.input_list = ["a", "b", "c"]
        self.node.key_name = "letter"
        self.node.execute()
        
        expected = [
            {"letter": "a"},
            {"letter": "b"},
            {"letter": "c"}
        ]
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_numeric_values(self):
        """Test with numeric values"""
        self.node.input_list = [1, 2, 3]
        self.node.key_name = "number"
        self.node.execute()
        
        expected = [
            {"number": 1},
            {"number": 2},
            {"number": 3}
        ]
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_mixed_types(self):
        """Test with mixed data types"""
        self.node.input_list = ["text", 42, True, None]
        self.node.key_name = "value"
        self.node.execute()
        
        expected = [
            {"value": "text"},
            {"value": 42},
            {"value": True},
            {"value": None}
        ]
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_empty_list(self):
        """Test with empty list"""
        self.node.input_list = []
        self.node.key_name = "item"
        self.node.execute()
        
        self.assertEqual(self.node.true_path, [])
        self.assertFalse(self.node.false_path)

    def test_default_key_name(self):
        """Test with default key name"""
        self.node.input_list = ["x", "y"]
        # key_name defaults to "value"
        self.node.execute()
        
        expected = [
            {"value": "x"},
            {"value": "y"}
        ]
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)

    def test_invalid_input_not_list(self):
        """Test error handling for non-list input"""
        self.node.input_list = "not a list"
        self.node.key_name = "key"
        self.node.execute()
        
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)
        self.assertFalse(self.node.true_path)

    def test_invalid_key_name(self):
        """Test error handling for invalid key name"""
        self.node.input_list = [1, 2, 3]
        self.node.key_name = ""  # Empty string
        self.node.execute()
        
        self.assertIsInstance(self.node.false_path, dict)
        self.assertIn("error", self.node.false_path)
        self.assertFalse(self.node.true_path)

    def test_complex_objects_in_list(self):
        """Test with complex objects in the list"""
        self.node.input_list = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        self.node.key_name = "user"
        self.node.execute()
        
        expected = [
            {"user": {"id": 1, "name": "Alice"}},
            {"user": {"id": 2, "name": "Bob"}}
        ]
        self.assertEqual(self.node.true_path, expected)
        self.assertFalse(self.node.false_path)


if __name__ == "__main__":
    unittest.main()