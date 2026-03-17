from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.service_node import ServiceNode
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

from polysynergy_nodes.mongodb.mongodb_connection import MongoDBConnection
from polysynergy_nodes.ssh.ssh_tunnel_instance import SshTunnelInstance


@node(
    name="MongoDB Connection",
    category="mongodb",
    icon="mongodb.svg",
    version=1.0
)
class MongoDBConnectionNode(ServiceNode):
    """
    MongoDB database connection for document queries.

    Provides a MongoDB connection that can be used by MongoDB Query nodes.
    Supports both standard host/port configuration and full connection string URI.

    **Connection String example:**
    mongodb://username:password@host:27017/database?authSource=admin

    **MongoDB Atlas example:**
    mongodb+srv://username:password@cluster.mongodb.net/database

    When a connection_string is provided it takes precedence over the
    individual host, port, username, password and auth_source fields.

    **SSH Tunnel:**
    Connect an SSH Tunnel node to the ssh_tunnel input to route the
    connection through an SSH tunnel. The tunnel's local_host and
    local_port will be used instead of the configured host and port.
    """

    host: str = NodeVariableSettings(
        label="Host",
        dock=dock_property(placeholder="localhost"),
        has_in=True,
        required=True,
        default="localhost",
        info="MongoDB server hostname or IP address"
    )

    port: int = NodeVariableSettings(
        label="Port",
        dock=True,
        has_in=True,
        default=27017,
        info="MongoDB server port (default: 27017)"
    )

    database: str = NodeVariableSettings(
        label="Database",
        dock=True,
        has_in=True,
        required=True,
        info="Name of the MongoDB database to connect to"
    )

    username: str = NodeVariableSettings(
        label="Username",
        dock=True,
        has_in=True,
        required=False,
        info="MongoDB username for authentication"
    )

    password: str = NodeVariableSettings(
        label="Password",
        dock=dock_property(secret=True),
        has_in=True,
        required=False,
        info="MongoDB password for authentication"
    )

    auth_source: str = NodeVariableSettings(
        label="Auth Source",
        dock=True,
        has_in=True,
        required=False,
        default="admin",
        info="Authentication database (default: admin)"
    )

    connection_string: str = NodeVariableSettings(
        label="Connection String",
        dock=dock_property(placeholder="mongodb://user:pass@host:27017/db"),
        has_in=True,
        required=False,
        info="Full MongoDB URI. When provided, overrides host, port, username, password and auth_source"
    )

    read_only: bool = NodeVariableSettings(
        label="Read Only",
        dock=True,
        has_in=True,
        default=True,
        info="When enabled, blocks all write operations (insert, update, delete)"
    )

    ssh_tunnel: SshTunnelInstance | None = NodeVariableSettings(
        label="SSH Tunnel",
        dock=True,
        has_in=True,
        required=False,
        info="SSH tunnel ServiceNode instance. When connected, the tunnel's local_host and local_port are used instead of the configured host and port"
    )

    instance: MongoDBConnection | None = NodeVariableSettings(
        label="Connection Instance",
        has_out=True,
        info="MongoDB connection instance for MongoDB Query nodes"
    )

    async def _find_ssh_tunnel(self):
        """Find connected SSH tunnel service node and get its instance."""
        connections = [c for c in self.get_in_connections() if c.target_handle == "ssh_tunnel"]
        for conn in connections:
            tunnel_node = self.state.get_node_by_id(conn.source_node_id)
            if hasattr(tunnel_node, "provide_instance"):
                instance = await tunnel_node.provide_instance()
                if hasattr(instance, "local_host") and hasattr(instance, "local_port"):
                    return instance
        return None

    async def provide_instance(self) -> MongoDBConnection:
        """Create and return MongoDB connection instance."""
        effective_host = self.host or "localhost"
        effective_port = int(self.port or 27017)

        # Look up connected SSH tunnel
        tunnel = await self._find_ssh_tunnel()
        if tunnel:
            print(f"[MongoDBConnection] Using SSH tunnel: {tunnel.local_host}:{tunnel.local_port}")
            effective_host = tunnel.local_host
            effective_port = tunnel.local_port

        config = {
            "host": effective_host,
            "port": effective_port,
            "database": self.database,
            "username": self.username,
            "password": self.password,
            "auth_source": self.auth_source,
            "connection_string": self.connection_string,
        }

        self.instance = MongoDBConnection(config, read_only=self.read_only if self.read_only is not None else True)
        return self.instance
