import unittest
from unittest.mock import Mock
from polysynergy_nodes.route.property_router import PropertyRouter


class TestPropertyRouter(unittest.TestCase):

    def setUp(self):
        self.node = PropertyRouter()
        
        # Reset paths
        self.node.false_path = False
        
        # Mock connections with source_handle
        self.mock_connection_active = Mock()
        self.mock_connection_active.source_handle = "routes.active"
        self.mock_connection_active.make_killer = Mock()
        
        self.mock_connection_inactive = Mock()
        self.mock_connection_inactive.source_handle = "routes.inactive"
        self.mock_connection_inactive.make_killer = Mock()
        
        self.mock_connection_admin = Mock()
        self.mock_connection_admin.source_handle = "routes.admin"
        self.mock_connection_admin.make_killer = Mock()
        
        self.mock_connection_default = Mock()
        self.mock_connection_default.source_handle = "routes.default"
        self.mock_connection_default.make_killer = Mock()

    def test_no_connections_triggers_false_path(self):
        self.node.out_connections = []
        self.node.value = {"status": "active"}
        self.node.property_path = "status"
        
        self.node.execute()
        
        self.assertIn("error", self.node.false_path)

    def test_simple_property_match(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_inactive]
        self.node.routes = {"active": None, "inactive": None}
        self.node.value = {"status": "active"}
        self.node.property_path = "status"
        
        self.node.execute()
        
        # Active route connection should not be killed
        self.mock_connection_active.make_killer.assert_not_called()
        # Inactive route connection should be killed
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Original object should be stored in the active route
        self.assertEqual(self.node.routes["active"], {"status": "active"})

    def test_nested_property_match(self):
        self.node.out_connections = [self.mock_connection_admin, self.mock_connection_inactive]
        self.node.routes = {"admin": None, "user": None}
        self.node.value = {"user": {"role": "admin", "name": "John"}}
        self.node.property_path = "user.role"
        
        self.node.execute()
        
        # Admin route connection should not be killed
        self.mock_connection_admin.make_killer.assert_not_called()
        # User route connection should be killed
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Original object should be stored in the admin route
        self.assertEqual(self.node.routes["admin"], {"user": {"role": "admin", "name": "John"}})

    def test_deep_nested_property_match(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_inactive]
        self.node.routes = {"dark": None, "light": None}
        self.node.value = {"config": {"settings": {"theme": "dark"}}}
        self.node.property_path = "config.settings.theme"
        
        self.node.execute()
        
        # Dark theme route should not be killed
        self.mock_connection_active.make_killer.assert_not_called()
        # Light theme route should be killed
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Original object should be stored in the dark route
        self.assertEqual(self.node.routes["dark"], {"config": {"settings": {"theme": "dark"}}})

    def test_numeric_property_value_match(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_inactive]
        self.mock_connection_active.source_handle = "routes.25"
        self.mock_connection_inactive.source_handle = "routes.30"
        self.node.routes = {"25": None, "30": None}
        self.node.value = {"age": 25}
        self.node.property_path = "age"
        
        self.node.execute()
        
        # Age 25 route should not be killed
        self.mock_connection_active.make_killer.assert_not_called()
        # Age 30 route should be killed
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Original object should be stored in the 25 route
        self.assertEqual(self.node.routes["25"], {"age": 25})

    def test_boolean_property_value_match(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_inactive]
        self.mock_connection_active.source_handle = "routes.True"
        self.mock_connection_inactive.source_handle = "routes.False"
        self.node.routes = {"True": None, "False": None}
        self.node.value = {"is_enabled": True}
        self.node.property_path = "is_enabled"
        
        self.node.execute()
        
        # True route should not be killed
        self.mock_connection_active.make_killer.assert_not_called()
        # False route should be killed
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Original object should be stored in the True route
        self.assertEqual(self.node.routes["True"], {"is_enabled": True})

    def test_property_not_found_uses_default(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_default]
        self.node.routes = {"active": None, "default": None}
        self.node.value = {"name": "John"}  # No status property
        self.node.property_path = "status"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Active connection should be killed
        self.mock_connection_active.make_killer.assert_called_once()
        # Original object should be stored in default
        self.assertEqual(self.node.routes["default"], {"name": "John"})

    def test_nested_property_not_found_uses_default(self):
        self.node.out_connections = [self.mock_connection_admin, self.mock_connection_default]
        self.node.routes = {"admin": None, "default": None}
        self.node.value = {"user": {"name": "John"}}  # No role property
        self.node.property_path = "user.role"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Admin connection should be killed
        self.mock_connection_admin.make_killer.assert_called_once()
        # Original object should be stored in default
        self.assertEqual(self.node.routes["default"], {"user": {"name": "John"}})

    def test_property_not_found_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_inactive]
        self.node.routes = {"active": None, "inactive": None}
        self.node.value = {"name": "John"}  # No status property
        self.node.property_path = "status"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_active.make_killer.assert_called_once()
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_no_route_match_uses_default(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_default]
        self.node.routes = {"active": None, "default": None}
        self.node.value = {"status": "pending"}  # Status exists but no route for "pending"
        self.node.property_path = "status"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Active connection should be killed
        self.mock_connection_active.make_killer.assert_called_once()
        # Original object should be stored in default
        self.assertEqual(self.node.routes["default"], {"status": "pending"})

    def test_no_route_match_no_default_triggers_false_path(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_inactive]
        self.node.routes = {"active": None, "inactive": None}
        self.node.value = {"status": "pending"}  # Status exists but no route for "pending"
        self.node.property_path = "status"
        
        self.node.execute()
        
        # All connections should be killed
        self.mock_connection_active.make_killer.assert_called_once()
        self.mock_connection_inactive.make_killer.assert_called_once()
        # Should trigger false path
        self.assertIn("error", self.node.false_path)

    def test_non_dict_input_uses_default(self):
        self.node.out_connections = [self.mock_connection_active, self.mock_connection_default]
        self.node.routes = {"active": None, "default": None}
        self.node.value = "not a dictionary"
        self.node.property_path = "status"
        
        self.node.execute()
        
        # Default connection should be chosen
        self.mock_connection_default.make_killer.assert_not_called()
        # Active connection should be killed
        self.mock_connection_active.make_killer.assert_called_once()
        # Original value should be stored in default
        self.assertEqual(self.node.routes["default"], "not a dictionary")

    def test_get_property_value_method(self):
        # Test property extraction method directly
        test_obj = {"status": "active", "user": {"role": "admin", "name": "John"}}
        
        self.assertEqual(self.node._get_property_value(test_obj, "status"), "active")
        self.assertEqual(self.node._get_property_value(test_obj, "user.role"), "admin")
        self.assertEqual(self.node._get_property_value(test_obj, "user.name"), "John")
        self.assertIsNone(self.node._get_property_value(test_obj, "nonexistent"))
        self.assertIsNone(self.node._get_property_value(test_obj, "user.nonexistent"))
        self.assertIsNone(self.node._get_property_value(test_obj, "nonexistent.role"))
        
        # Test with non-dict input
        self.assertIsNone(self.node._get_property_value("not a dict", "status"))
        self.assertIsNone(self.node._get_property_value(None, "status"))
        
        # Test with nested non-dict
        nested_obj = {"user": "not a dict"}
        self.assertIsNone(self.node._get_property_value(nested_obj, "user.role"))


if __name__ == "__main__":
    unittest.main()