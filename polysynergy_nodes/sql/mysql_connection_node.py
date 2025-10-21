from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.service_node import ServiceNode
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection
from polysynergy_nodes.sql.mysql_connection import MysqlConnection


@node(
    name="MySQL Connection",
    category="sql",
    icon="database.svg",
    version=1.0
)
class MySQLConnectionNode(ServiceNode):
    """
    MySQL database connection for SQL queries.

    Provides a MySQL database connection for applications.
    Supports SSL/TLS encryption for secure connections.
    """

    host: str = NodeVariableSettings(
        label="Host",
        dock=dock_property(placeholder="localhost or IP address"),
        has_in=True,
        required=True,
        info="MySQL server hostname or IP address"
    )

    port: int = NodeVariableSettings(
        label="Port",
        dock=True,
        has_in=True,
        default=3306,
        info="MySQL server port (default: 3306)"
    )

    database_name: str = NodeVariableSettings(
        label="Database Name",
        dock=True,
        has_in=True,
        required=True,
        info="Name of the MySQL database to connect to"
    )

    username: str = NodeVariableSettings(
        label="Username",
        dock=True,
        has_in=True,
        required=True,
        info="MySQL username"
    )

    password: str = NodeVariableSettings(
        label="Password",
        dock=dock_property(secret=True),
        has_in=True,
        required=True,
        info="MySQL password"
    )

    use_ssl: bool = NodeVariableSettings(
        label="Use SSL/TLS",
        dock=dock_property(switch=True),
        has_in=True,
        default=False,
        info="Enable SSL/TLS connection encryption"
    )

    instance: BaseSqlConnection | None = NodeVariableSettings(
        label="Connection Instance",
        has_out=True,
        info="MySQL connection instance for SQL Query nodes"
    )

    async def provide_instance(self) -> BaseSqlConnection:
        """Create and return MySQL connection instance."""
        config = {
            "host": self.host,
            "port": self.port,
            "database_name": self.database_name,
            "username": self.username,
            "password": self.password,
            "use_ssl": self.use_ssl
        }

        self.instance = MysqlConnection(config)
        return self.instance
