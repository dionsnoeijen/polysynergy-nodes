import unittest
from unittest.mock import Mock
from polysynergy_nodes.route.type_router import TypeRouter


class TestTypeRouter(unittest.TestCase):

    def setUp(self):
        self.node = TypeRouter()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_string = Mock()
        self.mock_connection_string.source_handle = "types.string"
        self.mock_connection_string.make_killer = Mock()
        
        self.mock_connection_number = Mock()
        self.mock_connection_number.source_handle = "types.number"
        self.mock_connection_number.make_killer = Mock()
        
        self.mock_connection_boolean = Mock()
        self.mock_connection_boolean.source_handle = "types.boolean"
        self.mock_connection_boolean.make_killer = Mock()
        
        self.mock_connection_array = Mock()
        self.mock_connection_array.source_handle = "types.array"
        self.mock_connection_array.make_killer = Mock()
        
        self.mock_connection_object = Mock()
        self.mock_connection_object.source_handle = "types.object"
        self.mock_connection_object.make_killer = Mock()
        
        self.mock_connection_null = Mock()
        self.mock_connection_null.source_handle = "types.null"
        self.mock_connection_null.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "types.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.value = "test"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_string_type_routing(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_number]
        self.node.types = {"string": None, "number": None}
        self.node.value = "hello world"
        
        self.node.execute()
        
        # String connection should not be killed
        self.mock_connection_string.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_number.make_killer.assert_called_once()
        # Value should be stored in the string type
        self.assertEqual(self.node.types["string"], "hello world")

    def test_number_type_routing_int(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_number]
        self.node.types = {"string": None, "number": None}
        self.node.value = 42
        
        self.node.execute()
        
        # Number connection should not be killed
        self.mock_connection_number.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in the number type
        self.assertEqual(self.node.types["number"], 42)

    def test_number_type_routing_float(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_number]
        self.node.types = {"string": None, "number": None}
        self.node.value = 3.14
        
        self.node.execute()
        
        # Number connection should not be killed
        self.mock_connection_number.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in the number type
        self.assertEqual(self.node.types["number"], 3.14)

    def test_boolean_type_routing(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_boolean]
        self.node.types = {"string": None, "boolean": None}
        self.node.value = True
        
        self.node.execute()
        
        # Boolean connection should not be killed
        self.mock_connection_boolean.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in the boolean type
        self.assertEqual(self.node.types["boolean"], True)

    def test_array_type_routing(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_array]
        self.node.types = {"string": None, "array": None}
        self.node.value = [1, 2, 3]
        
        self.node.execute()
        
        # Array connection should not be killed
        self.mock_connection_array.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in the array type
        self.assertEqual(self.node.types["array"], [1, 2, 3])

    def test_object_type_routing(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_object]
        self.node.types = {"string": None, "object": None}
        self.node.value = {"key": "value"}
        
        self.node.execute()
        
        # Object connection should not be killed
        self.mock_connection_object.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in the object type
        self.assertEqual(self.node.types["object"], {"key": "value"})

    def test_null_type_routing(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_null]
        self.node.types = {"string": None, "null": None}
        self.node.value = None
        
        self.node.execute()
        
        # Null connection should not be killed
        self.mock_connection_null.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in the null type
        self.assertEqual(self.node.types["null"], None)

    def test_default_case_when_no_match(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_default]
        self.node.types = {"string": None, "default": None}
        # Use a custom type that doesn't match standard types
        self.node.value = set([1, 2, 3])
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Other connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        # Value should be stored in default case
        self.assertEqual(self.node.types["default"], {1, 2, 3})

    def test_no_match_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_string, self.mock_connection_number]
        self.node.types = {"string": None, "number": None}
        # Use a custom type that doesn't match
        self.node.value = set([1, 2, 3])
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_string.make_killer.assert_called_once()
        self.mock_connection_number.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_get_type_name_method(self):
        # Test type detection method directly
        self.assertEqual(self.node._get_type_name("test"), "string")
        self.assertEqual(self.node._get_type_name(42), "number")
        self.assertEqual(self.node._get_type_name(3.14), "number")
        self.assertEqual(self.node._get_type_name(True), "boolean")
        self.assertEqual(self.node._get_type_name([1, 2, 3]), "array")
        self.assertEqual(self.node._get_type_name({"key": "value"}), "object")
        self.assertEqual(self.node._get_type_name(None), "null")
        self.assertEqual(self.node._get_type_name(set([1, 2, 3])), "set")


if __name__ == "__main__":
    unittest.main()