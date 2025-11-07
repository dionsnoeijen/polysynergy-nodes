from typing import Any
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Get First Item",
    category="list",
    icon="list.svg",
    version=1.0
)
class GetFirstItem(Node):
    input_list: list = NodeVariableSettings(
        label="Input List",
        has_in=True,
        dock=True,
        info="The list to get the first item from"
    )

    default_value: Any = NodeVariableSettings(
        label="Default Value",
        default=None,
        dock=True,
        has_in=True,
        info="Value to return if list is empty"
    )

    item: Any = NodeVariableSettings(
        label="First Item",
        has_out=True,
        info="The first item in the list"
    )

    list_length: int = NodeVariableSettings(
        label="List Length",
        has_out=True,
        info="Total length of the list"
    )

    true_path: bool | Any = PathSettings(
        label="Item Found",
        info="Returns the first item"
    )
    false_path: bool | dict = PathSettings(
        label="Empty List",
        info="Triggered if list is empty"
    )

    def execute(self):
        try:
            if not isinstance(self.input_list, list):
                raise ValueError("Input is not a list")

            self.list_length = len(self.input_list)

            # Check if list is empty
            if len(self.input_list) == 0:
                self.item = self.default_value
                self.true_path = self.default_value
                self.false_path = {
                    "error": "List is empty",
                    "default_value": self.default_value
                }
                return

            # Get first item
            self.item = self.input_list[0]
            self.true_path = self.item
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.item = None
            self.list_length = 0
