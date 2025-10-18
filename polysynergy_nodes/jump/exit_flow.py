from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings


@node(name="Exit Flow", category="flow", version=1.0)
class ExitFlow(Node):
    """
    Stops the entire flow execution immediately.

    All unprocessed nodes (including parallel branches) will be killed.
    The flow will exit with success status.

    Usage:
        Connect this node when you want to gracefully stop the entire flow,
        for example when a validation fails or required data is missing.
    """

    message: str = NodeVariableSettings(
        label="Exit Message",
        dock=True,
        has_in=True,
        default="Flow stopped",
        info="Reason for stopping the flow (will be logged)"
    )

    async def execute(self):
        print(f"[EXIT FLOW] {self.message}")

        # Get all nodes from state
        all_nodes = self.context.state.nodes

        # Kill ALL nodes that haven't been processed yet
        for node in all_nodes:
            if not node.is_processed() and node.id != self.id:
                print(f"[EXIT] Killing node: {node.handle} {node.__class__.__name__}")
                node.kill()

        # Kill self to ensure no further execution
        self.kill()
