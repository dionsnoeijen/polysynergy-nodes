import json

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Variable List",
    category="variable",
    icon='list.svg'
)
class VariableList(Node):
    value: list = NodeVariableSettings(
        label="Value",
        dock=True,
        has_out=True,
        default=[]
    )

    append: list | dict | str | int | float | None = NodeVariableSettings(
        label="Append",
        has_in=True,
        default=[]
    )

    true_path: bool | list = PathSettings(label="List")

    def execute(self):
        if self.append:
            self.value.append(self.append)

        self.true_path = self.value
