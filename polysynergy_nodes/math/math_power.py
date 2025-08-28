from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_nodes.math.utils.to_number import to_number

@node(name="Power", category="math", type="power", icon="power.svg")
class MathPower(Node):
    a: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True)
    b: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True)

    result: int | float = 0
    true_path: bool | int | float = False
    false_path: bool | dict = False

    async def execute(self):
        try:
            a_val = to_number(self.a)
            b_val = to_number(self.b)

            if a_val is None or b_val is None:
                raise ValueError("Invalid input: a or b could not be converted to number")

            self.true_path = a_val ** b_val
            self.false_path = False
        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False