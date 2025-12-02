from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Variable Float", category="variable", icon='float.svg', version=1.0)
class VariableFloat(Node):
    value: float | str = NodeVariableSettings(label="Value", dock=True, has_in=True)
    values: dict[str, str] = NodeVariableSettings(label="Values", dock=True, has_in=True, default={})

    true_path: bool | float = PathSettings(label="Result", info="The float value with placeholders replaced")
    false_path: bool | dict = PathSettings(label="Error", info="If the conversion or placeholder replacement fails")

    async def execute(self):
        try:
            # Ensure values is a dict
            if not isinstance(self.values, dict):
                self.values = {}

            # Handle None value
            if self.value is None:
                self.value = 0.0

            # Convert to string for placeholder replacement
            value_str = str(self.value)

            # Replace placeholders in values dict first
            replaced_values = replace_placeholders(
                data=self.values,
                values=self.values,
                state=self.state,
                current_node=self
            )

            # Replace placeholders in value
            value_replaced = replace_placeholders(
                data=value_str,
                values=replaced_values,
                state=self.state,
                current_node=self
            )

            # Convert to float
            # Handle various formats: "123.45", "123", 123, 123.45
            if isinstance(value_replaced, str):
                value_replaced = value_replaced.strip()
                if value_replaced == "":
                    result = 0.0
                else:
                    result = float(value_replaced)
            elif isinstance(value_replaced, (int, float)):
                result = float(value_replaced)
            else:
                raise ValueError(f"Cannot convert {type(value_replaced).__name__} to float")

            self.true_path = result

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False