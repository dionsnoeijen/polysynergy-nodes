from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_nodes.math.utils.to_number import to_number

@node(name="Absolute", category="math", type="absolute")
class MathAbsolute(Node):
    value: int | float | str = NodeVariableSettings(default=0, dock=True, has_in=True, has_out=True)

    true_path: bool | int | float = False
    false_path: bool | dict = False

    async def execute(self):
        try:
            val = to_number(self.value)
            if val is None:
                raise ValueError(f"Cannot convert '{self.value}' to number")
            self.true_path = abs(val)
        except Exception as e:
            self.false_path = NodeError.format(e)