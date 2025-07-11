from polysynergy_nodes.base.execution_context.flow import Flow
from polysynergy_nodes.agent.services.chat_memories.chat_memory_base import ChatMemoryBase
from polysynergy_nodes.base.execution_context.is_compatible_provider import is_compatible_provider


def find_connected_memory(node_id: str, flow: Flow) -> ChatMemoryBase | None:
    memory_connections = [c for c in flow.get_in_connections(node_id) if c.target_handle == "chat_memory"]

    for conn in memory_connections:
        node = flow.nodes.get(conn.source_node_id)
        if hasattr(node, "provide_instance") and is_compatible_provider(node, ChatMemoryBase):
            return node.provide_instance()

    return None