from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node

@node(
    name="Continue Loop",
    category="flow",
    type="loop",
    icon='loop.svg',
)
class ContinueLoop(Node):

    def execute(self):
        loop = self.is_in_loop()
        if loop:
            loop.continue_loop()
