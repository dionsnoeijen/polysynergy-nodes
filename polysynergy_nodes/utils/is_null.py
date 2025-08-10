from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Is Null", category="utils", version=1.0)
class IsNull(Node):
    value: Any = NodeVariableSettings(label="Value", dock=True, has_in=True, has_out=False, info="Value to check for null/empty")
    
    is_null: bool = NodeVariableSettings(label="Is Null", has_out=True, info="True if value is null/empty")
    
    true_path: bool = PathSettings(label="Result", info="True if value is null/empty")
    false_path: Any = PathSettings(label="Error", info="Error information")

    def is_null_or_empty(self, value):
        """Check if value is null, None, empty string, empty list, etc."""
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
            return True
        if isinstance(value, str) and value.lower() in ("null", "none", "undefined"):
            return True
        return False

    async def execute(self):
        try:
            is_null = self.is_null_or_empty(self.value)
            
            self.is_null = is_null
            self.true_path = is_null
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))