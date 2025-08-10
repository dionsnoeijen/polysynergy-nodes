from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="If Then Else", category="conditional", version=1.0)
class IfThenElse(Node):
    condition: Any = NodeVariableSettings(label="Condition", dock=True, has_in=True, has_out=False)
    then_value: Any = NodeVariableSettings(label="Then Value", dock=True, has_in=True, has_out=False)
    else_value: Any = NodeVariableSettings(label="Else Value", dock=True, has_in=True, has_out=False)
    
    true_path: Any = PathSettings(label="Result", info="The selected value based on condition")
    false_path: Any = PathSettings(label="Error", info="Error information")

    def coerce_to_bool(self, value):
        """Convert value to boolean following common conventions."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower().strip() not in ('', 'false', '0', 'null', 'none', 'undefined')
        if isinstance(value, (int, float)):
            return value != 0
        if value is None:
            return False
        return bool(value)

    async def execute(self):
        try:
            condition_result = self.coerce_to_bool(self.condition)
            
            if condition_result:
                self.true_path = self.then_value
            else:
                self.true_path = self.else_value
                
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))