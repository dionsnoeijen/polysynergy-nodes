from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="Secret",
    category="hidden",
    icon="lock.svg",
    version=1.0
)
class VariableSecret(Node):
    true_path: bool | str = PathSettings(
        label="Secret Key",
        info="The full secret id"
    )

    async def execute(self):
        pass