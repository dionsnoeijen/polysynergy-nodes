from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="If Then Else",
    category="conditional",
    icon='condition.svg'
)
class IfThenElse(Node):
    condition: bool = NodeVariableSettings(
        label="Condition",
        info="The condition to evaluate",
        has_in=True,
        required=True
    )
    
    then_value: object = NodeVariableSettings(
        label="Then Value",
        info="Value to return if condition is true",
        has_in=True
    )
    
    else_value: object = NodeVariableSettings(
        label="Else Value", 
        info="Value to return if condition is false",
        has_in=True
    )

    true_path: object = PathSettings(
        label="Result",
        info="The selected value based on condition"
    )

    def execute(self):
        condition_result = bool(self.condition)
        
        if condition_result:
            self.true_path = self.then_value
        else:
            self.true_path = self.else_value