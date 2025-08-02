from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Boolean Value",
    category="boolean",
    icon='boolean.svg'
)
class BooleanValue(Node):
    value: bool = NodeVariableSettings(
        label="Boolean Value",
        default=False,
        has_in=True,
        has_out=True
    )

    true_path: bool = PathSettings(
        label="Result",
        info="The boolean value"
    )

    def execute(self):
        try:
            # Ensure the value is a proper boolean
            self.true_path = bool(self.value)
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False