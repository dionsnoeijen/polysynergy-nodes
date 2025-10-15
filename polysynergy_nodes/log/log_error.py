import json
import logging
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

logger = logging.getLogger(__name__)

@node(
    name="Log Error",
    category="log",
    icon='log.svg'
)
class LogError(Node):
    message: str | dict = NodeVariableSettings(
        label="Message",
        dock=True,
        has_in=True
    )

    def execute(self):
        if isinstance(self.message, dict):
            formatted_message = json.dumps(self.message, indent=2, ensure_ascii=False)
            logger.error(formatted_message)
            print(f"[ERROR] {formatted_message}")
        else:
            logger.error(self.message)
            print(f"[ERROR] {self.message}")