import logging
import time

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

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

    async def execute(self):
        print(f"\n\n=== JUMP EXECUTE START ===\n\n")
        if self.has_max_retries and self.counter >= self.max_retries:
            self.false_path = {"error": "Max retries reached"}
            return

        is_retry = self.has_max_retries and self.counter > 0

        self.counter += 1
        print(f"JUMP: Jumping to {self.to} (attempt {self.counter})")
        logger.info(f"Jumping to {self.to} (attempt {self.counter})")

        if is_retry and self.retry_timeout > 0:
            logger.debug(f"Sleeping for {self.retry_timeout} seconds before retrying jump")
            time.sleep(self.retry_timeout)

        try:
            to_node = self.state.get_node_by_handle(self.to)
            if not to_node:
                raise ValueError(f"Node with handle '{self.to}' not found")
            logger.info(f"Jumping to node: {to_node.__class__.__name__}")
        except ValueError as e:
            self.false_path = {"error": str(e)}
            return

        # Check if it's a To node (class name starts with "To" due to versioning like "ToV1_0")
        if not to_node.__class__.__name__.startswith("To"):
            self.false_path = {"error": f"You must jump to a \"To\" node, but found {to_node.__class__.__name__}"}
            return

        # Recursively resurrect all nodes forward from TO node
        # until we hit another Jump node
        visited = set()
        all_nodes = []

        def collect_forward(node):
            """Collect all nodes going forward via out_connections"""
            if node.id in visited:
                return
            visited.add(node.id)

            # Skip Jump nodes to prevent infinite recursion
            if node.__class__.__name__.startswith("Jump"):
                return

            all_nodes.append(node)
            print(f"    Collected: {node.__class__.__name__} ({node.handle})")

            # Continue forward through ALL out_connections (both flow and data)
            for connection in node.get_out_connections():
                target_node = self.state.get_node_by_id(connection.target_node_id)
                if target_node:
                    print(f"      -> following connection to {target_node.__class__.__name__} ({target_node.handle})")
                    collect_forward(target_node)

        print(f"=== Collecting nodes from TO forward ===")
        collect_forward(to_node)
        print(f"=== Found {len(all_nodes)} nodes to resurrect ===")

        # Resurrect all nodes AND their connections
        for node in all_nodes:
            print(f"  Resurrecting: {node.__class__.__name__} ({node.handle})")
            node.resurrect()
            # FORCEFULLY resurrect all connections
            for conn in node.get_out_connections():
                if conn.is_killer():
                    print(f"    Connection was killer, force resurrecting: {conn.source_handle} -> {conn.target_handle}")
                    conn.resurrect()
                if conn.is_killer():
                    print(f"    ERROR: Connection STILL killer after force resurrect!")
            for conn in node.get_in_connections():
                if conn.is_killer():
                    conn.resurrect()

        # Resurrect TO node
        to_node.resurrect()

        # Execute TO which triggers the flow
        print(f"=== Executing TO ===")
        await self.flow.execute_node(to_node)

        # After execution, resurrect all nodes again
        # This is critical because connections may have been killed during execution
        print(f"=== Re-resurrecting all nodes after execution ===")
        for node in all_nodes:
            print(f"  Re-resurrecting: {node.__class__.__name__} ({node.handle})")
            node.resurrect()
        to_node.resurrect()

        print(f"=== JUMP COMPLETE ===\n\n")
