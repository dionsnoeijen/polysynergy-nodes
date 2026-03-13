from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Property Router",
    category="route",
    icon='route.svg'
)
class PropertyRouter(Node):
    out_connections: list[Connection] = []
    
    value: object = NodeVariableSettings(
        label="Object",
        info="The object to extract property value from",
        has_in=True,
        dock=True,
        required=True
    )
    
    property_path: str = NodeVariableSettings(
        label="Property Path",
        info="Dot notation path to the property (e.g., 'status', 'user.role', 'config.settings.theme')",
        has_in=True,
        dock=True,
        required=True
    )

    routes: dict = NodeVariableSettings(
        label="Routes",
        dock=dock_dict(
            enabled=False,
            key_label="Property Value",
            in_switch=False,
            out_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=False,
            info="Routes based on property values",
        ),
        default=[
            {
                "handle": "default",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            }
        ]
    )

    false_path: dict = PathSettings(
        label="No Match", 
        info="Triggered when property doesn't exist or no route matches"
    )

    def execute(self):
        if not self.get_out_connections():
            self.false_path = {"error": "No output connections available"}
            return

        # Extract property value from object
        property_value = self._get_property_value(self.value, self.property_path)
        
        if property_value is None:
            # Property doesn't exist - check for default
            if "default" in self.routes:
                for connection in self.get_out_connections():
                    handle = connection.source_handle
                    if handle.startswith("routes."):
                        handle = handle[len("routes."):]
                    
                    if handle != "default":
                        connection.make_killer()
                    else:
                        self.routes["default"] = self.value
                return
            else:
                # No default - kill all connections and trigger false_path
                for connection in self.get_out_connections():
                    connection.make_killer()
                self.false_path = {"error": f"Property '{self.property_path}' not found"}
                return
        
        # Convert property value to string for matching
        str_property_value = str(property_value)
        
        # Check which route matches
        matched_route = None
        if str_property_value in self.routes:
            matched_route = str_property_value
        elif "default" in self.routes:
            matched_route = "default"
        
        if matched_route:
            # Kill connections that don't match the selected route
            for connection in self.get_out_connections():
                handle = connection.source_handle
                if handle.startswith("routes."):
                    handle = handle[len("routes."):]
                
                if handle != matched_route:
                    connection.make_killer()
                else:
                    # Pass the original input value through the matched route
                    self.routes[matched_route] = self.value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.get_out_connections():
                connection.make_killer()
            self.false_path = {"error": f"No matching route for property value: {property_value}"}

    def _get_property_value(self, obj, path: str):
        """Extract property value from object using dot notation path"""
        if not isinstance(obj, dict):
            return None
            
        parts = path.split('.')
        current = obj
        
        try:
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            return current
        except (KeyError, TypeError):
            return None