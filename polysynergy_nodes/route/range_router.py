from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.dock_property import dock_dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Range Router",
    category="route",
    icon='route.svg'
)
class RangeRouter(Node):
    out_connections: list[Connection] = []
    
    value: object = NodeVariableSettings(
        label="Value",
        info="The numeric value to check against ranges",
        has_in=True,
        dock=True,
        required=True
    )

    ranges: dict = NodeVariableSettings(
        label="Ranges",
        dock=dock_dict(
            key_label="Range (e.g., '0-100', '>50', '<=10')",
            in_switch=False,
            value_field=False,
            type_field=False,
            out_switch_default=True,
            out_switch_enabled=False,
            info="Range conditions - supports: '0-100', '<10', '>50', '<=20', '>=30', '==5'",
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
        info="Triggered when no range matches and no default exists"
    )

    def execute(self):
        if not self.out_connections:
            self.false_path = {"error": "No output connections available"}
            return

        # Convert input value to number
        try:
            numeric_value = float(self.value)
        except (ValueError, TypeError):
            # Not a number - check for default case
            if "default" in self.ranges:
                for connection in self.out_connections:
                    handle = connection.source_handle
                    if handle.startswith("ranges."):
                        handle = handle[len("ranges."):]
                    
                    if handle != "default":
                        connection.make_killer()
                    else:
                        self.ranges["default"] = self.value
                return
            else:
                # No default - kill all connections and trigger false_path
                for connection in self.out_connections:
                    connection.make_killer()
                self.false_path = {"error": f"Value is not numeric: {self.value}"}
                return
        
        # Check which range matches
        matched_range = None
        for range_key in self.ranges.keys():
            if range_key == "default":
                continue
                
            if self._value_matches_range(numeric_value, range_key):
                matched_range = range_key
                break
        
        # If no match, try default
        if matched_range is None and "default" in self.ranges:
            matched_range = "default"
        
        if matched_range:
            # Kill connections that don't match the selected range
            for connection in self.out_connections:
                handle = connection.source_handle
                if handle.startswith("ranges."):
                    handle = handle[len("ranges."):]
                
                if handle != matched_range:
                    connection.make_killer()
                else:
                    # Pass the input value through the matched range
                    self.ranges[matched_range] = self.value
        else:
            # No match found and no default - kill all connections and trigger false_path
            for connection in self.out_connections:
                connection.make_killer()
            self.false_path = {"error": f"No matching range for value: {self.value}"}

    def _value_matches_range(self, value: float, range_str: str) -> bool:
        """Check if a numeric value matches a range specification"""
        range_str = range_str.strip()
        
        try:
            # Handle different range formats
            if '-' in range_str and not range_str.startswith('-') and range_str.count('-') == 1:
                # Range format: "0-100"
                parts = range_str.split('-')
                min_val = float(parts[0])
                max_val = float(parts[1])
                return min_val <= value <= max_val
                
            elif range_str.startswith('>='):
                # Greater than or equal: ">=30"
                threshold = float(range_str[2:])
                return value >= threshold
                
            elif range_str.startswith('<='):
                # Less than or equal: "<=10"
                threshold = float(range_str[2:])
                return value <= threshold
                
            elif range_str.startswith('>'):
                # Greater than: ">50"
                threshold = float(range_str[1:])
                return value > threshold
                
            elif range_str.startswith('<'):
                # Less than: "<10"
                threshold = float(range_str[1:])
                return value < threshold
                
            elif range_str.startswith('=='):
                # Equal to: "==5"
                threshold = float(range_str[2:])
                return value == threshold
                
            else:
                # Try to parse as exact value
                threshold = float(range_str)
                return value == threshold
                
        except ValueError:
            # Invalid range format
            return False