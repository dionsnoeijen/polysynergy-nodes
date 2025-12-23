from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.service_node import ServiceNode


async def find_connected_components(node: Node, target_handle: str = "components") -> dict[str, ServiceNode]:
    """
    Find all component nodes connected to the given handle.

    Returns a dict mapping component handles to their instances.

    Args:
        node: The Layout node to search for connected components
        target_handle: The handle to look for connections (default: "components")

    Returns:
        Dict of {component_handle: ServiceNode instance with render() method}
    """
    connections = [
        c for c in node.get_in_connections()
        if c.target_handle.startswith(f"{target_handle}.")
    ]

    components = {}

    for conn in connections:
        # Extract the key from "components.table_users" -> "table_users"
        key = conn.target_handle.split(".", 1)[-1] if "." in conn.target_handle else conn.target_handle

        source_node = node.state.get_node_by_id(conn.source_node_id)

        if source_node is None:
            continue

        # Direct component node
        if hasattr(source_node, "provide_instance"):
            instance = await source_node.provide_instance()
            if hasattr(instance, "render"):
                # Use the component's handle property if available, otherwise use connection key
                handle = getattr(instance, "handle", None) or key
                components[handle] = instance
                continue

        # Handle GroupNode case
        if _is_group_node(source_node):
            actual_component = await _find_component_in_group(
                source_node, conn.source_handle, node.state
            )
            if actual_component:
                handle = getattr(actual_component, "handle", None) or key
                components[handle] = actual_component

    return components


def _is_group_node(node) -> bool:
    """Detect if node is a GroupNode by class name pattern."""
    return node.__class__.__name__.startswith("GroupNode_")


async def _find_component_in_group(group_node, source_handle: str, state) -> ServiceNode | None:
    """
    Find the actual component provider inside a GroupNode.
    """
    import string

    if "_" not in source_handle:
        return None

    prefix, original_handle = source_handle.split("_", 1)

    # Find all connections that target this group
    group_input_connections = [
        c for c in state.connections if c.target_node_id == group_node.id
    ]

    # Build prefix mapping
    prefix_to_node_id = {}
    unique_source_nodes = []
    for conn in group_input_connections:
        if conn.source_node_id not in unique_source_nodes:
            unique_source_nodes.append(conn.source_node_id)

    for i, node_id in enumerate(unique_source_nodes):
        prefix_to_node_id[string.ascii_lowercase[i]] = node_id

    if prefix not in prefix_to_node_id:
        return None

    target_node_id = prefix_to_node_id[prefix]
    internal_node = state.get_node_by_id(target_node_id)

    if hasattr(internal_node, "provide_instance"):
        instance = await internal_node.provide_instance()
        if hasattr(instance, "render"):
            return instance

    return None
