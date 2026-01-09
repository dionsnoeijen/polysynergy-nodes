from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from typing import Any

from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(name="Is Not Empty", category="conditional", icon="comparison.svg")
class IsNotEmpty(Node):
    """
    Checks if a value is not empty (similar to PHP's !empty() function).

    Returns true_path if value is NOT empty.
    Returns false_path if value IS empty.

    Empty values include: null, false, 0, "0", "", [], {}

    Supports {{placeholder}} syntax in string values.
    """

    value: any = NodeVariableSettings(
        label="Value",
        dock=True,
        has_in=True,
        info="Value to check for emptiness. Supports {{placeholder}} syntax."
    )

    true_path: any = PathSettings(label="Value")
    false_path: any = PathSettings(label="Is Empty")

    def _is_empty(self, val: any) -> bool:
        if val is None:
            return True
        if val is False:
            return True
        if val == 0 or val == "0":
            return True
        if val == "":
            return True
        if isinstance(val, (list, dict)) and len(val) == 0:
            return True
        return False

    def execute(self):
        # Replace placeholders in value
        resolved_value = replace_placeholders(
            data=self.value,
            values={},
            state=self.state,
            current_node=self
        )

        is_empty = self._is_empty(resolved_value)

        if not is_empty:
            self.true_path = resolved_value
            self.false_path = False
        else:
            self.true_path = False
            self.false_path = "Value is empty"
