from typing import Optional

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_nodes.mongodb.mongodb_connection import MongoDBConnection


async def find_connected_mongodb(node: Node, target_handle: str = "connection") -> Optional[MongoDBConnection]:
    """
    Find a connected MongoDB connection service node.

    Args:
        node: The node to search for connected MongoDB connections
        target_handle: The handle to look for (default: "connection")

    Returns:
        The MongoDBConnection instance if found, None otherwise
    """
    connections = [c for c in node.get_in_connections() if c.target_handle == target_handle]

    print(f"[find_connected_mongodb] Looking for connections to handle '{target_handle}'")
    print(f"[find_connected_mongodb] Found {len(connections)} connections")

    for conn in connections:
        service_node = node.state.get_node_by_id(conn.source_node_id)
        print(f"[find_connected_mongodb] Checking node: {service_node.__class__.__name__}")

        if hasattr(service_node, "provide_instance"):
            print(f"[find_connected_mongodb] Node has provide_instance, calling it...")
            try:
                instance = await service_node.provide_instance()
                print(f"[find_connected_mongodb] Got instance: {type(instance)}")
                if isinstance(instance, MongoDBConnection):
                    print(f"[find_connected_mongodb] Valid MongoDB connection found!")
                    return instance
                else:
                    print(f"[find_connected_mongodb] Instance is not MongoDBConnection")
            except Exception as e:
                print(f"[find_connected_mongodb] Error getting instance from {service_node}: {e}")
                import traceback
                traceback.print_exc()
                continue
        else:
            print(f"[find_connected_mongodb] Node does not have provide_instance method")

    print(f"[find_connected_mongodb] No valid MongoDB connection found")
    return None
