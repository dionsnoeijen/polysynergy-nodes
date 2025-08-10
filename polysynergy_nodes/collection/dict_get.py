from typing import Any, Dict, Union
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Dict Get", category="collection", version=1.0)
class DictGet(Node):
    dict_obj: Dict = NodeVariableSettings(label="Dictionary", dock=True, has_in=True, has_out=False, info="Dictionary to get value from")
    key: str = NodeVariableSettings(label="Key", dock=True, has_in=True, has_out=False, info="Key to look up")
    default_value: Any = NodeVariableSettings(label="Default", dock=True, has_in=True, has_out=False, info="Default value if key not found")
    
    value: Any = NodeVariableSettings(label="Value", has_out=True, info="The value for the key")
    
    true_path: Any = PathSettings(label="Result", info="The value for the key")
    false_path: Any = PathSettings(label="Error", info="Error information")

    async def execute(self):
        try:
            if not isinstance(self.dict_obj, dict):
                raise ValueError("Input must be a dictionary")
            
            if not isinstance(self.key, str):
                key = str(self.key)
            else:
                key = self.key
            
            # Use get method with default value
            value = self.dict_obj.get(key, self.default_value)
            
            self.value = value
            self.true_path = value
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))