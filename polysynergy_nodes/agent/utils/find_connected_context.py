from polysynergy_nodes.agent.services.contexts.context_base import ContextBase
from polysynergy_node_runner.execution_context.flow import Flow
from polysynergy_node_runner.execution_context.is_compatible_provider import is_compatible_provider


def find_connected_context_client(node_id: str, flow: Flow) -> ContextBase | None:
    client_connections = [c for c in flow.get_in_connections(node_id) if c.target_handle == "context"]

    for conn in client_connections:
        node = flow.nodes.get(conn.source_node_id)
        if hasattr(node, "provide_instance") and is_compatible_provider(node, ContextBase):
            return node.provide_instance()

    return None