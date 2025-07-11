import uuid

from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.path_settings import PathSettings

@node(
    name="UUID v4",
    category="uuid",
    icon="hash.svg"
)
class UUIDv4(Node):
    true_path: str | bool = PathSettings(label="UUID")

    def execute(self):
        self.true_path = str(uuid.uuid4())