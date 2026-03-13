from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Type Router",
    category="route",
    icon='route.svg'
)
class TypeRouter(Node):
    out_connections: list[Connection] = []
    
    value: object = NodeVariableSettings(
        label="Value",
        info="The value to analyze for type routing",
        has_in=True,
        dock=True,
        required=True
    )

    types: dict = NodeVariableSettings(
        label="Types",
        dock=dock_dict(
            enabled=False,
            key_label="Type Name",
            in_switch=False,
            out_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=False,
            info="Type routing cases - predefined types for routing",
        ),
        default=[
            {
                "handle": "string",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "number",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "boolean",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "array",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "object",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
            {
                "handle": "null",
                "has_in": False,
                "has_out": True,
                "published": False,
                "type": "str",
                "value": "",
            },
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
        info="Triggered when no type matches and no default exists"
    )

    def execute(self):
        if not self.get_out_connections():
            self.false_path = {"error": "No output connections available"}
            return

        # Determine the type of the input value
        type_name = self._get_type_name(self.value)
        
        # Check if type matches any case key
        matched_type = None
        if type_name in self.types:
            matched_type = type_name
        else:
            # Check if "default" case exists
            if "default" in self.types:
                matched_type = "default"
        
        if matched_type:
            # Kill connections that don't match the selected type
            for connection in self.get_out_connections():
                handle = connection.source_handle
                if handle.startswith("types."):
                    handle = handle[len("types."):]
                
                if handle != matched_type:
                    connection.make_killer()
                else:
                    # Pass the input value through the matched type
                    self.types[matched_type] = self.value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.get_out_connections():
                connection.make_killer()
            self.false_path = {"error": f"No matching type case for: {type_name}"}

    def _get_type_name(self, value) -> str:
        """Convert Python types to user-friendly type names"""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean" 
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            # For other types, use the actual type name
            return type(value).__name__.lower()