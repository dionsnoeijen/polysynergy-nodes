import random

from polysynergy_node_runner.execution_context.connection import Connection
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="Random Path",
    category="random",
    icon='dice.svg',
    version=2.0
)
class RandomPath(Node):
    out_connections: list[Connection] = []
    in_connections: list[Connection] = []

    true_path: bool | int | float | dict | list | str = PathSettings(label="Chosen Path", info="The path that was taken")
    false_path: dict = PathSettings(label="Error")

    async def execute(self):
        try:
            if not self.out_connections:
                self.false_path = NodeError.format("No output connections available for random selection")
                return

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
        except Exception as e:
            self.false_path = NodeError.format(e)