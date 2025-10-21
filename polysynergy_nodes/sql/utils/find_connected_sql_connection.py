from typing import Optional
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection


async def find_connected_sql_connection(node: Node, target_handle: str = "connection") -> Optional[BaseSqlConnection]:
    """
    Find a connected SQL connection service node.

    Args:
        node: The node to search for connected SQL connections
        target_handle: The handle to look for (default: "connection")

    Returns:
        The SQL connection instance if found, None otherwise
    """
    connections = [c for c in node.get_in_connections() if c.target_handle == target_handle]

    print(f"[find_connected_sql_connection] Looking for connections to handle '{target_handle}'")
    print(f"[find_connected_sql_connection] Found {len(connections)} connections")

    for conn in connections:
        service_node = node.state.get_node_by_id(conn.source_node_id)
        print(f"[find_connected_sql_connection] Checking node: {service_node.__class__.__name__}")

        if hasattr(service_node, "provide_instance"):
            print(f"[find_connected_sql_connection] Node has provide_instance, calling it...")
            try:
                instance = await service_node.provide_instance()
                print(f"[find_connected_sql_connection] Got instance: {type(instance)}")
                if isinstance(instance, BaseSqlConnection):
                    print(f"[find_connected_sql_connection] ✓ Valid SQL connection found!")
                    return instance
                else:
                    print(f"[find_connected_sql_connection] Instance is not BaseSqlConnection")
            except Exception as e:
                print(f"[find_connected_sql_connection] Error getting instance from {service_node}: {e}")
                import traceback
                traceback.print_exc()
                continue
        else:
            print(f"[find_connected_sql_connection] Node does not have provide_instance method")

    print(f"[find_connected_sql_connection] No valid SQL connection found")
    return None
