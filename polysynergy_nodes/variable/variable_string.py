from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Variable String",
    category="variable",
    icon='string.svg',
    version=1.0
)
class VariableString(Node):
    value: str = NodeVariableSettings(label="Value", dock=dock_text_area(), has_in=True)
    values: dict[str, str] = NodeVariableSettings(label="Values", dock=True, has_in=True)

    true_path: bool | str = PathSettings(label="Result", info="The value with placeholders replaced")
    false_path: bool | dict = PathSettings(label="Error", info="If the placeholder replacement fails")

    async def execute(self):
        try:
            # Convert value to string if it's not already
            if self.value is None:
                self.value = ""
            elif not isinstance(self.value, str):
                # Try to convert to string - this will work for numbers, booleans, etc.
                self.value = str(self.value)

            if not isinstance(self.values, dict):
                self.values = {}

            if self.value.strip() == "":
                self.true_path = ""
                return
            replaced_values = replace_placeholders(
                data=self.values,
                values=self.values,
                state=self.state,
                current_node=self
            )

            self.true_path = replace_placeholders(
                data=self.value,
                values=replaced_values,
                state=self.state,
                current_node=self
            )
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False