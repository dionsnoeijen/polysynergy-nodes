from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Type Of", category="utils", version=1.0)
class TypeOf(Node):
    value: Any = NodeVariableSettings(label="Value", dock=True, has_in=True, has_out=False, info="Value to get type of")
    
    type_name: str = NodeVariableSettings(label="Type", has_out=True, info="The type name as string")
    
    true_path: str = PathSettings(label="Result", info="The type name")
    false_path: Any = PathSettings(label="Error", info="Error information")

    def get_type_name(self, value):
        """Get a friendly type name for the value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif isinstance(value, tuple):
            return "tuple"
        elif isinstance(value, set):
            return "set"
        else:
            # Use the Python type name for other types
            return type(value).__name__

    async def execute(self):
        try:
            type_name = self.get_type_name(self.value)
            
            self.type_name = type_name
            self.true_path = type_name
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))