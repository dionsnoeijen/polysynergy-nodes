import re
from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Pattern Router",
    category="route",
    icon='route.svg'
)
class PatternRouter(Node):
    out_connections: list[Connection] = []
    
    value: object = NodeVariableSettings(
        label="Value",
        info="The string value to match against patterns",
        has_in=True,
        dock=True,
        required=True
    )

    patterns: dict = NodeVariableSettings(
        label="Patterns",
        dock=dock_dict(
            key_label="Regex Pattern",
            in_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=True,
            out_switch_enabled=False,
            info="Regular expression patterns for matching - use 'default' for fallback",
        ),
        default=[{
            "type": "str",
            "value": "",
            "handle": "default",
            "has_in": False,
            "has_out": True,
            "published": False
        }]
    )

    false_path: dict = PathSettings(
        label="No Match", 
        info="Triggered when no pattern matches and no default exists"
    )

    def execute(self):
        if not self.get_out_connections():
            self.false_path = {"error": "No output connections available"}
            return

        # Convert input value to string
        str_value = str(self.value)
        
        # Check which pattern matches
        matched_pattern = None
        for pattern_key in self.patterns.keys():
            if pattern_key == "default":
                continue
                
            if self._value_matches_pattern(str_value, pattern_key):
                matched_pattern = pattern_key
                break
        
        # If no match, try default
        if matched_pattern is None and "default" in self.patterns:
            matched_pattern = "default"
        
        if matched_pattern:
            # Kill connections that don't match the selected pattern
            for connection in self.get_out_connections():
                handle = connection.source_handle
                if handle.startswith("patterns."):
                    handle = handle[len("patterns."):]
                
                if handle != matched_pattern:
                    connection.make_killer()
                else:
                    # Pass the input value through the matched pattern
                    self.patterns[matched_pattern] = self.value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.get_out_connections():
                connection.make_killer()
            self.false_path = {"error": f"No matching pattern for value: {self.value}"}

    def _value_matches_pattern(self, value: str, pattern: str) -> bool:
        """Check if a string value matches a regex pattern"""
        try:
            return bool(re.match(pattern, value))
        except re.error:
            # Invalid regex pattern
            return False