from typing import Any
from polysynergy_node_runner.setup_context.dock_property import dock_select_values
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

@node(name="Switch", category="conditional", version=1.0)
class Switch(Node):
    value: Any = NodeVariableSettings(label="Value", dock=True, has_in=True, has_out=False)
    case_1: Any = NodeVariableSettings(label="Case 1", dock=True, has_in=True, has_out=False)
    result_1: Any = NodeVariableSettings(label="Result 1", dock=True, has_in=True, has_out=False)
    case_2: Any = NodeVariableSettings(label="Case 2", dock=True, has_in=True, has_out=False)
    result_2: Any = NodeVariableSettings(label="Result 2", dock=True, has_in=True, has_out=False)
    case_3: Any = NodeVariableSettings(label="Case 3", dock=True, has_in=True, has_out=False)
    result_3: Any = NodeVariableSettings(label="Result 3", dock=True, has_in=True, has_out=False)
    default_result: Any = NodeVariableSettings(label="Default", dock=True, has_in=True, has_out=False)
    
    true_path: Any = PathSettings(label="Result", info="The matched result value")
    false_path: Any = PathSettings(label="Error", info="Error information")

    async def execute(self):
        try:
            # Check each case in order
            if self.case_1 is not None and self.value == self.case_1:
                self.true_path = self.result_1
            elif self.case_2 is not None and self.value == self.case_2:
                self.true_path = self.result_2
            elif self.case_3 is not None and self.value == self.case_3:
                self.true_path = self.result_3
            else:
                # Use default if no cases match
                self.true_path = self.default_result
                
            self.false_path = False
                
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(str(e))