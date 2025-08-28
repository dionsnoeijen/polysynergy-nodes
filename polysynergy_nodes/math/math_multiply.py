from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_nodes.math.utils.to_number import to_number


@node(name="Multiply", category="math", type="multiply", icon="multiply.svg")
class MathMultiply(Node):
    a: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True, dock=True)
    b: int | float | str = NodeVariableSettings(default=0, has_in=True, has_out=True, dock=True)

    true_path: bool | float = PathSettings(label="Result")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        try:
            a = to_number(self.a)
            b = to_number(self.b)

            if a is None or b is None:
                raise ValueError("Invalid input: a or b could not be converted to number.")

            self.true_path = a * b

        except Exception as e:
            self.false_path = {"error": str(e)}