from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_nodes.math.utils.to_number import to_number

@node(name="Round", category="math", type="round")
class MathRound(Node):
    value: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True)
    decimals: int | str = NodeVariableSettings(default=0, has_in=True, has_out=True)

    true_path: bool | int | float = False
    false_path: bool | dict = False

    async def execute(self):
        try:
            val = to_number(self.value)
            dec = to_number(self.decimals)

            if val is None or dec is None:
                raise ValueError("Invalid input: value or decimals could not be converted to number")

            self.true_path = round(val, int(dec))
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False