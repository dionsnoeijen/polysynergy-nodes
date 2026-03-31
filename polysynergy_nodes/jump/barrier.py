from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Barrier",
    category="flow",
    icon="jump.svg",
    version=1.0,
)
class Barrier(Node):
    """
    A pass-through node that never traverses backward.

    Use this to merge two or more flow paths without triggering
    back-traversal. Whatever reaches the Barrier first will pass
    through; the node does not wait for (or look at) other inputs.
    """

    _no_backward_traversal = True

    input: str | int | float | dict | list | bool = NodeVariableSettings(
        label="Input",
        has_in=True,
        info="Any value to pass through"
    )

    true_path: str | int | float | dict | list | bool = PathSettings(label="Output")

    async def execute(self):
        self.true_path = self.input
