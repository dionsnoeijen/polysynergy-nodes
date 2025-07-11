from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.path_settings import PathSettings


@node(
    name="Schedule",
    category="mock",
    has_play_button=True,
    has_enabled_switch=False
)
class MockSchedule(Node):

    true_path: bool = PathSettings(default=True, label="Play")

    def execute(self):
        pass