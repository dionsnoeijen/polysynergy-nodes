import json

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Variable List",
    category="variable",
    icon='list.svg',
    version=1.0
)
class VariableList(Node):
    value: list | str = NodeVariableSettings(
        label="Value",
        dock=True,
        has_in=True,
        default=[]
    )

    append: list | dict | str | int | float | None = NodeVariableSettings(
        label="Append",
        has_in=True,
        default=[]
    )

    output_list: list = NodeVariableSettings(
        label="Output List",
        has_out=True,
        info="The resulting list"
    )

    true_path: bool | list = PathSettings(
        label="List",
        info="Returns the list value"
    )
    false_path: bool | dict = PathSettings(
        label="Error",
        info="Triggered if parsing fails"
    )

    async def execute(self):
        try:
            # Auto-parse JSON string to list
            if isinstance(self.value, str):
                try:
                    self.value = json.loads(self.value)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Input string is not valid JSON: {str(e)}")

            # If it's a list with a single string element that looks like JSON, parse it
            # This happens when a string is connected to the value input (framework wraps it in a list)
            elif isinstance(self.value, list) and len(self.value) == 1 and isinstance(self.value[0], str):
                try:
                    parsed = json.loads(self.value[0])
                    if isinstance(parsed, list):
                        self.value = parsed
                    # If parsed is not a list, keep the original list with 1 element
                except (json.JSONDecodeError, TypeError):
                    # Not JSON, keep as is
                    pass

            # Ensure value is a list
            if not isinstance(self.value, list):
                self.value = [self.value]

            if self.append:
                self.value.append(self.append)

            self.output_list = self.value
            self.true_path = self.value
            self.false_path = False

        except Exception as e:
            self.false_path = {"error": str(e)}
            self.true_path = False
            self.output_list = []
