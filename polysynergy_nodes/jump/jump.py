import logging
import time

from polysynergy_nodes.base.setup_context.node import Node
from polysynergy_nodes.base.setup_context.node_decorator import node
from polysynergy_nodes.base.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.base.setup_context.path_settings import PathSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@node(
    name="Jump",
    category="flow",
    type="jump",
    icon='jump.svg',
)
class Jump(Node):
    to: str = NodeVariableSettings(dock=True, required=True)

    has_max_retries: bool = NodeVariableSettings(label="Has Max Retries", dock=True, default=False)
    max_retries: int = NodeVariableSettings(dock=True, required=True, default=5)
    retry_timeout: int = NodeVariableSettings(label="Retry Timeout (seconds)", dock=True, default=5)

    counter: int = 0
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        if self.has_max_retries and self.counter >= self.max_retries:
            self.false_path = {"error": "Max retries reached"}
            return

        is_retry = self.has_max_retries and self.counter > 0

        self.counter += 1
        logger.info(f"Jumping to {self.to} (attempt {self.counter})")

        if is_retry and self.retry_timeout > 0:
            logger.debug(f"Sleeping for {self.retry_timeout} seconds before retrying jump")
            time.sleep(self.retry_timeout)

        try:
            to_node = self.flow.get_node(self.to)
            logger.info(f"Jumping to node: {to_node.__class__.__name__}")
        except ValueError as e:
            self.false_path = {"error": str(e)}
            return

        if to_node.__class__.__name__ != "To":
            self.false_path = {"error": "You must jump to a \"To\" node"}
            return

        nodes_for_jump, jump_end_node = self.find_nodes_for_jump()

        for node_for_jump in nodes_for_jump:
            node_for_jump.resurrect()

        self.flow.execute_node(to_node)
