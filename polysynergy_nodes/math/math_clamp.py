from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_nodes.math.utils.to_number import to_number

@node(name="Clamp", category="math", type="clamp", icon="clamp.svg")
class MathClamp(Node):
    value: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True)
    min_value: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True)
    max_value: int | float | str = NodeVariableSettings(default=100, has_in=True, has_out=True)

    true_path: bool | int | float = False
    false_path: bool | dict = False

    async def execute(self):
        try:
            val = to_number(self.value)
            min_val = to_number(self.min_value)
            max_val = to_number(self.max_value)

            if None in (val, min_val, max_val):
                raise ValueError("Cannot convert input(s) to number")

            self.true_path = max(min_val, min(val, max_val))
        except Exception as e:
            self.false_path = NodeError.format(e)