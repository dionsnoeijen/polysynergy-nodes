from typing import Any, List, Union
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Array Get", category="collection", version=1.0)
class ArrayGet(Node):
    array: List = NodeVariableSettings(label="Array", dock=True, has_in=True, has_out=False, info="Array to get item from")
    index: int = NodeVariableSettings(label="Index", dock=True, has_in=True, has_out=False, info="Index of item to get (0-based)")
    
    item: Any = NodeVariableSettings(label="Item", has_out=True, info="The item at the specified index")
    
    true_path: Any = PathSettings(label="Result", info="The item at the index")
    false_path: Any = PathSettings(label="Error", info="Error information")

    async def execute(self):
        try:
            if not isinstance(self.array, list):
                raise ValueError("Input must be a list/array")
            
            if not isinstance(self.index, int):
                try:
                    index = int(self.index)
                except (ValueError, TypeError):
                    raise ValueError("Index must be an integer")
            else:
                index = self.index
            
            # Support negative indexing
            if index < 0:
                index = len(self.array) + index
            
            if index < 0 or index >= len(self.array):
                raise IndexError(f"Index {self.index} out of range for array of length {len(self.array)}")
            
            item = self.array[index]
            self.item = item
            self.true_path = item
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))