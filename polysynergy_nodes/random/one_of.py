import random
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="One Of",
    category="data",
    icon="dice.svg"
)
class OneOf(Node):
    values: list = NodeVariableSettings(
        label="Values",
        has_in=True,
        dock=True
    )

    true_path: bool | str | float | int = PathSettings(label="Selected Value")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            if not isinstance(self.values, list) or len(self.values) == 0:
                raise ValueError("Values must be a non-empty list")

            self.true_path = random.choice(self.values)

        except Exception as e:
            self.false_path = {"error": str(e)}