import logging
from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings

logger = logging.getLogger(__name__)

@node(
    name="Log Error",
    category="log",
    icon='log.svg'
)
class LogError(Node):
    message: str = NodeVariableSettings(
        label="Message",
        dock=True,
        has_in=True
    )

    def execute(self):
        logger.error(self.message)