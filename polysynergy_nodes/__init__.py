"""
PolySynergy Nodes Package

This package contains the production nodes for the PolySynergy orchestration system.
Nodes are auto-discovered by the gather_nodes_service via filesystem scanning.
The registered_nodes list below documents the available nodes for reference.
"""

registered_nodes = [
    "polysynergy_nodes.ssh.ssh_tunnel_node.SSHTunnelNode",
    "polysynergy_nodes.mongodb.mongodb_connection_node.MongoDBConnectionNode",
    "polysynergy_nodes.mongodb.mongodb_query_node.MongoDBQuery",
]
