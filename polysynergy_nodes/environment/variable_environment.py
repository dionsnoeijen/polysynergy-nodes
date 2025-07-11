from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Env Variable",
    category="environment",
    icon="environment.svg"
)
class VariableEnvironment(Node):
    true_path: bool | str = PathSettings(
        label="Key",
        info="The environment variable key"
    )

    def execute(self):
        pass