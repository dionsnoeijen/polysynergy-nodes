import uuid

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="UUID v4",
    category="uuid",
    icon="hash.svg",
    version=1.0
)
class UUIDv4(Node):
    true_path: str | bool = PathSettings(label="UUID", info="Random UUID v4")
    false_path: dict | bool = PathSettings(label="Error", info="Error information if generation fails")

    async def execute(self):
        try:
            self.true_path = str(uuid.uuid4())
            self.false_path = False
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(e)