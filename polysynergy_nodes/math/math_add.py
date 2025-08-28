from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.math.utils.to_number import to_number


@node(name="Add", category="math", type="add", icon="add.svg")
class MathAdd(Node):
    a: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True, dock=True)
    b: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True, dock=True)

    true_path: bool | int | float = PathSettings("Result", info="The sum of a and b")
    false_path: bool | int | float = PathSettings("Error", info="Triggered if a or b cannot be converted to a number")

    async def execute(self):

        a = to_number(self.a)
        b = to_number(self.b)

        if a is None or b is None:
            self.false_path = True
            self.true_path = False
        else:
            self.true_path = a + b
            self.false_path = False
