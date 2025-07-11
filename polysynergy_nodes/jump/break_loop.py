from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node

@node(
    name="Break Loop",
    category="flow",
    type="loop",
    icon='loop.svg',
)
class BreakLoop(Node):

    def execute(self):
        loop = self.is_in_loop()
        if loop:
            loop.break_loop()
