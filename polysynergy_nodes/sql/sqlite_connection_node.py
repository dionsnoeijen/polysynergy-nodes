from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.service_node import ServiceNode
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection
from polysynergy_nodes.sql.sqlite_connection import SqliteConnection


@node(
    name="SQLite Connection",
    category="sql",
    icon="database.svg",
    version=1.0
)
class SQLiteConnectionNode(ServiceNode):
    """
    SQLite database connection for SQL queries.

    Provides a file-based SQLite database connection.
    Perfect for local development, testing, and lightweight applications.
    """

    database_file: str = NodeVariableSettings(
        label="Database File",
        dock=dock_property(placeholder="/path/to/database.db"),
        has_in=True,
        required=True,
        default="tmp/app.db",
        info="Path to SQLite database file"
    )

    instance: BaseSqlConnection | None = NodeVariableSettings(
        label="Connection Instance",
        has_out=True,
        info="SQLite connection instance for SQL Query nodes"
    )

    async def provide_instance(self) -> BaseSqlConnection:
        """Create and return SQLite connection instance."""
        config = {
            "database_file": self.database_file
        }

        self.instance = SqliteConnection(config)
        return self.instance
