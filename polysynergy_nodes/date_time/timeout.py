from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

import time

from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    name="Timeout",
    icon="clock.svg",
    category="date_time"
)
class Timeout(Node):

    seconds: int = NodeVariableSettings(
        info="How long to wait before continuing execution.",
        dock=True,
        default=1
    )

    true_path: bool = PathSettings(
        info="True path for the node."
    )

    def execute(self):
        time.sleep(self.seconds)
        self.true_path = True
