from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Default Value", category="utils", version=1.0)
class DefaultValue(Node):
    value: Any = NodeVariableSettings(label="Value", dock=True, has_in=True, has_out=False, info="Primary value to use")
    default: Any = NodeVariableSettings(label="Default", dock=True, has_in=True, has_out=False, info="Fallback value if primary is null/empty")
    
    result: Any = NodeVariableSettings(label="Result", has_out=True, info="The chosen value")
    
    true_path: Any = PathSettings(label="Result", info="The chosen value (primary or default)")
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
            if self.is_null_or_empty(self.value):
                result = self.default
            else:
                result = self.value
            
            self.result = result
            self.true_path = result
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))