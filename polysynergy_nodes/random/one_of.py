import random
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="One Of",
    category="random",
    icon="dice.svg",
    version=2.0
)
class OneOf(Node):
    values: list = NodeVariableSettings(
        label="Values",
        has_in=True,
        dock=True
    )

    true_path: bool | str | float | int = PathSettings(label="Selected Value")
    false_path: dict = PathSettings(label="Error")

    async def execute(self):
        try:
            if not isinstance(self.values, list) or len(self.values) == 0:
                self.false_path = NodeError.format("Values must be a non-empty list")
                return

            self.true_path = random.choice(self.values)

        except Exception as e:
            self.false_path = NodeError.format(e)