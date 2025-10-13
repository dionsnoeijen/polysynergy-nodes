import logging
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

logger = logging.getLogger(__name__)

@node(
    name="Log Info",
    category="log",
    icon='log.svg'
)
class LogInfo(Node):

    message: str = NodeVariableSettings(
        label="Message",
        dock=True,
        has_in=True
    )

    def execute(self):
        logger.info(self.message)
        print(f"[INFO] {self.message}")