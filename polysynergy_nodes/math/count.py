from typing import Any, Union, List
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Count", category="math", version=1.0, icon="count.svg")
class Count(Node):
    values: Union[List, str, dict] = NodeVariableSettings(label="Values", dock=True, has_in=True, has_out=False, info="List, string, or dict to count")
    
    count: int = NodeVariableSettings(label="Count", has_out=True, info="Number of items")
    
    true_path: int = PathSettings(label="Result", info="The count of items")
    false_path: Any = PathSettings(label="Error", info="Error information")

    async def execute(self):
        try:
            if self.values is None:
                count = 0
            elif isinstance(self.values, (list, dict, str)):
                count = len(self.values)
            else:
                # Try to get length of other iterable types
                try:
                    count = len(self.values)
                except TypeError:
                    count = 1  # Single item
            
            self.count = count
            self.true_path = count
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))