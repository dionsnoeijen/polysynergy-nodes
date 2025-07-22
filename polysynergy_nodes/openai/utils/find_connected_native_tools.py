from polysynergy_node_runner.execution_context.flow import Flow
from polysynergy_node_runner.execution_context.is_compatible_provider import is_compatible_provider
from polysynergy_nodes.openai.services.native_tools.native_tool_base import NativeToolBase


def find_connected_native_tools(node_id: str, flow: Flow) -> NativeToolBase | None:
    native_tool_connections = [c for c in flow.get_in_connections(node_id) if c.target_handle == "native_tools"]

    instances = []
    for conn in native_tool_connections:
        node = flow.nodes.get(conn.source_node_id)
        if hasattr(node, "provide_instance") and is_compatible_provider(node, NativeToolBase):
            instances.append(node.provide_instance())

    return instances