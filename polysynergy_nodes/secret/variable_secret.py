from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.path_settings import PathSettings

@node(
    name="Secret",
    category="hidden",
    icon="lock.svg"
)
class VariableSecret(Node):
    true_path: bool | str = PathSettings(
        label="Secret Key",
        info="The full secret id"
    )

    def execute(self):
        pass