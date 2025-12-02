from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node

@node(
    name="Continue Loop",
    category="flow",
    type="loop",
    icon='loop.svg',
)
class ContinueLoop(Node):

    async def execute(self):
        loop = self.is_in_loop()
        if loop:
            loop.continue_loop()
