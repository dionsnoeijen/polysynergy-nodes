import random

from polysynergy_nodes.base.execution_context.connection import Connection
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Random Path",
    category="flow",
    icon='dice.svg',
)
class RandomPath(Node):
    out_connections: list[Connection] = []
    in_connections: list[Connection] = []

    true_path: bool | int | float | dict | list | str = PathSettings(label="Chosen Path", info="The path that was taken")

    def execute(self):
        if not self.out_connections:
            self.true_path = None
            return None

        chosen_connection = random.choice(self.out_connections)
        for connection in self.out_connections:
            if connection is not chosen_connection:
                connection.make_killer()
            else:
                if self.in_connections:
                    source_node = self.state.get_node_by_id(self.in_connections[0].source_node_id)
                    if hasattr(source_node, 'true_path'):
                        self.true_path = source_node.true_path
                    else:
                        self.true_path = True
                else:
                    self.true_path = True