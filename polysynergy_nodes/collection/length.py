from typing import Any, Union, List, Dict
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Length", category="collection", version=1.0)
class Length(Node):
    value: Union[List, Dict, str, Any] = NodeVariableSettings(label="Value", dock=True, has_in=True, has_out=False, info="Collection to get length of")
    
    length: int = NodeVariableSettings(label="Length", has_out=True, info="Number of items/characters")
    
    true_path: int = PathSettings(label="Result", info="The length/count")
    false_path: Any = PathSettings(label="Error", info="Error information")

    async def execute(self):
        try:
            if self.value is None:
                length = 0
            elif isinstance(self.value, (list, dict, str, tuple, set)):
                length = len(self.value)
            else:
                # Try to get length of other iterable types
                try:
                    length = len(self.value)
                except TypeError:
                    raise ValueError(f"Cannot get length of type {type(self.value).__name__}")
            
            self.length = length
            self.true_path = length
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))