from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Boolean NOT",
    category="boolean",
    icon='boolean.svg'
)
class BooleanNot(Node):
    value: bool = NodeVariableSettings(
        label="Value",
        has_in=True,
        required=True
    )

    true_path: bool = PathSettings(
        label="Result",
        info="The inverted boolean value"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if input is invalid"
    )

    def execute(self):
        try:
            # Convert input to boolean value and invert it
            bool_value = bool(self.value)
            self.true_path = not bool_value
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False