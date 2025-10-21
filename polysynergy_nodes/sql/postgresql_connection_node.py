from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.service_node import ServiceNode
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings

from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection
from polysynergy_nodes.sql.postgresql_connection import PostgresqlConnection


@node(
    name="PostgreSQL Connection",
    category="sql",
    icon="database.svg",
    version=1.0
)
class PostgreSQLConnectionNode(ServiceNode):
    """
    PostgreSQL database connection for SQL queries.

    Provides a PostgreSQL database connection for production applications.
    Supports SSL/TLS encryption for secure connections.

    **Supabase Connection:**
    Get your connection string from Supabase Dashboard → Settings → Database → Connection Pooling.
    Example: postgresql://postgres.PROJECT:[PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres

    Parse the connection string into separate fields:
    - Host: aws-0-eu-central-1.pooler.supabase.com
    - Port: 5432 (or 6543)
    - Database Name: postgres
    - Username: postgres.PROJECT (include project ref!)
    - Password: Your database password
    - Use SSL: Enable (required for Supabase)
    """

    host: str = NodeVariableSettings(
        label="Host",
        dock=dock_property(placeholder="localhost or db.project.supabase.co"),
        has_in=True,
        required=True,
        info="PostgreSQL server hostname (e.g., aws-0-eu-central-1.pooler.supabase.com for Supabase)"
    )

    port: int = NodeVariableSettings(
        label="Port",
        dock=True,
        has_in=True,
        default=5432,
        info="PostgreSQL server port (default: 5432, Supabase pooler: 5432 or 6543)"
    )

    database_name: str = NodeVariableSettings(
        label="Database Name",
        dock=True,
        has_in=True,
        required=True,
        info="Name of the PostgreSQL database (default: postgres)"
    )

    username: str = NodeVariableSettings(
        label="Username",
        dock=True,
        has_in=True,
        required=True,
        info="PostgreSQL username (Supabase: postgres.PROJECT_REF - include the project ref!)"
    )

    password: str = NodeVariableSettings(
        label="Password",
        dock=dock_property(secret=True),
        has_in=True,
        required=True,
        info="PostgreSQL password"
    )

    use_ssl: bool = NodeVariableSettings(
        label="Use SSL/TLS",
        dock=dock_property(switch=True),
        has_in=True,
        default=False,
        info="Enable SSL/TLS connection encryption (required for Supabase and most cloud providers)"
    )

    instance: BaseSqlConnection | None = NodeVariableSettings(
        label="Connection Instance",
        has_out=True,
        info="PostgreSQL connection instance for SQL Query nodes"
    )

    async def provide_instance(self) -> BaseSqlConnection:
        """Create and return PostgreSQL connection instance."""
        config = {
            "host": self.host,
            "port": self.port,
            "database_name": self.database_name,
            "username": self.username,
            "password": self.password,
            "use_ssl": self.use_ssl
        }

        self.instance = PostgresqlConnection(config)
        return self.instance
