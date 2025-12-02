import json
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

    message: str | dict | list | int | float = NodeVariableSettings(
        label="Message",
        dock=True,
        has_in=True
    )

    def execute(self):
        if isinstance(self.message, dict):
            formatted_message = json.dumps(self.message, indent=2, ensure_ascii=False)
            logger.info(formatted_message)
            print(f"[INFO] {formatted_message}")
        else:
            logger.info(self.message)
            print(f"[INFO] {self.message}")