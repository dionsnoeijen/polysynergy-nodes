from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node

@node(
    name="To",
    category="jump",
    type="to",
    has_enabled_switch=False
)
class To(Node):
    def execute(self):
        pass