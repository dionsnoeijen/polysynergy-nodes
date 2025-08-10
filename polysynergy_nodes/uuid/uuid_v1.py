import uuid

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="UUID v1",
    category="uuid",
    icon="hash.svg",
    version=1.0
)
class UUIDv1(Node):
    """
    Generate a UUID v1 (time and MAC address based).
    Note: This can leak MAC address information.
    """
    
    true_path: str | bool = PathSettings(
        label="UUID", 
        info="Time and MAC-based UUID v1"
    )
    false_path: dict | bool = PathSettings(
        label="Error", 
        info="Error information if generation fails"
    )

    async def execute(self):
        try:
            self.true_path = str(uuid.uuid1())
            self.false_path = False
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(e)