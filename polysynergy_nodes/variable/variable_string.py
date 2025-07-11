import json

from polysynergy_nodes.base.execution_context.replace_placeholders import replace_placeholders
from polysynergy_nodes.base.setup_context.dock_property import dock_text_area
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="String Variable",
    category="variable",
    icon='string.svg',
    version=1.02
)
class VariableString(Node):
    value: str = NodeVariableSettings(label="Value", dock=dock_text_area(), has_in=True)
    values: dict[str, str] = NodeVariableSettings(label="Values", dock=True, has_in=True, has_out=True)

    true_path: bool | str = PathSettings(label="Result", info="The value with placeholders replaced")
    false_path: bool | dict = PathSettings(label="Error", info="If the placeholder replacement fails")

    def execute(self):
        if not isinstance(self.value, str):
            raise ValueError("VariableString: Value must be a string")

        if not isinstance(self.values, dict):
            self.values = {}

        if self.value.strip() == "":
            self.true_path = ""
            return

        try:
            replaced_values = replace_placeholders(
                data=self.values,
                values=self.values,
                state=self.state
            )

            self.true_path = replace_placeholders(
                data=self.value,
                values=replaced_values,
                state=self.state
            )
        except ValueError as e:
            self.false_path = {"error": str(e)}
            self.true_path = False