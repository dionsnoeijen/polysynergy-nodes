import uuid

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.path_settings import PathSettings

@node(
    name="UUID Nil",
    category="uuid",
    icon="hash.svg",
    version=1.0
)
class UUIDNil(Node):
    """
    Generate the nil UUID (00000000-0000-0000-0000-000000000000).
    Useful for representing null/empty UUID values.
    """
    
    true_path: str | bool = PathSettings(
        label="UUID",
        info="Nil UUID (all zeros)"
    )
    
    false_path: dict | bool = PathSettings(
        label="Error",
        info="Error information if generation fails"
    )

    async def execute(self):
        try:
            # Return the nil UUID
            self.true_path = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
            self.false_path = False
        except Exception as e:
            self.true_path = False
            self.false_path = NodeError.format(e)