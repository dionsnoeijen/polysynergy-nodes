import re
from typing import Any

from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_code_editor
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError

from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection
from polysynergy_nodes.sql.utils.find_connected_sql_connection import find_connected_sql_connection


@node(
    name="SQL Query",
    category="sql",
    icon="database.svg",
    version=1.0
)
class SQLQuery(Node):
    """
    Execute SQL queries against a database connection.

    **Read-only by default** - only SELECT queries are allowed for safety.
    Use with SQL Connection nodes (SQLite, PostgreSQL, MySQL).

    Perfect for:
    - Querying CRM data for AI agents
    - Retrieving customer information
    - Analyzing database records
    - Text-to-SQL AI agents
    """

    connection: BaseSqlConnection | None = NodeVariableSettings(
        label="Connection",
        dock=True,
        has_in=True,
        required=True,
        info="Database connection from SQL Connection service node"
    )

    query: str = NodeVariableSettings(
        label="SQL Query",
        dock=dock_code_editor(metadata={"language": "sql"}),
        has_in=True,
        required=True,
        info="SQL query to execute (SELECT statements only for safety)"
    )

    allow_write_operations: bool = NodeVariableSettings(
        label="Allow Write Operations",
        dock=dock_property(switch=True),
        has_in=True,
        default=False,
        info="⚠️ Enable INSERT/UPDATE/DELETE queries (use with caution)"
    )

    parameters: dict = NodeVariableSettings(
        label="Query Parameters",
        dock=True,
        has_in=True,
        default={},
        info="Optional parameters for parameterized queries (prevents SQL injection)"
    )

    # Outputs
    results: list[dict] = NodeVariableSettings(
        label="Results",
        has_out=True,
        info="Query results as list of dictionaries"
    )

    row_count: int = NodeVariableSettings(
        label="Row Count",
        has_out=True,
        info="Number of rows returned/affected"
    )

    columns: list[str] = NodeVariableSettings(
        label="Columns",
        has_out=True,
        info="List of column names in the result set"
    )

    results_json: str = NodeVariableSettings(
        label="Results (JSON)",
        has_out=True,
        info="Query results as JSON string"
    )

    info: dict = NodeVariableSettings(
        label="Query Info",
        has_out=True,
        info="Metadata about query execution (message, row_count, columns, database_type)"
    )

    true_path: list[dict] = PathSettings(
        label="Success",
        info="Query results (list of dictionaries)"
    )

    false_path: dict = PathSettings(
        label="Error",
        info="Query execution failed"
    )

    def _validate_query(self, query: str) -> None:
        """Validate SQL query for safety"""
        # Remove comments and normalize whitespace
        clean_query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
        clean_query = re.sub(r'/\*.*?\*/', '', clean_query, flags=re.DOTALL)
        clean_query = ' '.join(clean_query.split()).strip().upper()

        if not clean_query:
            raise ValueError("Query is empty")

        # Check for dangerous operations if write operations not allowed
        if not self.allow_write_operations:
            dangerous_patterns = [
                r'\bINSERT\b',
                r'\bUPDATE\b',
                r'\bDELETE\b',
                r'\bDROP\b',
                r'\bTRUNCATE\b',
                r'\bALTER\b',
                r'\bCREATE\b',
                r'\bGRANT\b',
                r'\bREVOKE\b',
                r'\bEXEC\b',
                r'\bEXECUTE\b',
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, clean_query):
                    # Extract operation name without regex markers for error message
                    operation_name = pattern.strip(r'\b').replace('\\', '')
                    raise ValueError(
                        f"Write operations not allowed. "
                        f"Enable 'Allow Write Operations' to use {operation_name} statements."
                    )

        # Must start with SELECT (or WITH for CTEs) when read-only
        if not self.allow_write_operations:
            if not (clean_query.startswith('SELECT') or clean_query.startswith('WITH')):
                raise ValueError(
                    "Only SELECT queries are allowed in read-only mode. "
                    "Enable 'Allow Write Operations' for other query types."
                )

    async def execute(self):
        try:
            # Find the connected SQL connection using the service discovery pattern
            connection = await find_connected_sql_connection(self, "connection")

            if not connection:
                raise ValueError("No SQL connection found. Connect a SQL Connection node to the 'connection' input.")

            if not self.query or not self.query.strip():
                raise ValueError("SQL query is required")

            # Validate query for safety
            self._validate_query(self.query)

            # Execute query using the connection instance
            results = await connection.execute_query(self.query, self.parameters if self.parameters else None)

            # Convert non-JSON-serializable types (Decimal, datetime, etc.) to serializable types
            def convert_value(val):
                """Convert non-JSON-serializable types to strings or native types"""
                from decimal import Decimal
                from datetime import datetime, date, time

                if isinstance(val, Decimal):
                    # Convert Decimal to float for JSON compatibility
                    return float(val)
                elif isinstance(val, (datetime, date, time)):
                    # Convert datetime objects to ISO format strings
                    return val.isoformat()
                elif isinstance(val, bytes):
                    # Convert bytes to base64 string
                    import base64
                    return base64.b64encode(val).decode('utf-8')
                else:
                    return val

            # Convert all values in results
            serializable_results = []
            for row in results:
                serializable_row = {key: convert_value(val) for key, val in row.items()}
                serializable_results.append(serializable_row)

            # Set outputs
            self.results = serializable_results
            self.row_count = len(serializable_results)

            if serializable_results and len(serializable_results) > 0:
                self.columns = list(serializable_results[0].keys())
            else:
                self.columns = []

            # JSON output for easy consumption by AI agents
            import json
            self.results_json = json.dumps(serializable_results, indent=2)

            # Metadata in info output
            self.info = {
                "message": f"Query executed successfully. {self.row_count} rows returned.",
                "row_count": self.row_count,
                "columns": self.columns,
                "database_type": connection.database_type
            }

            # Results in true_path for easy flow control
            self.true_path = serializable_results
            self.false_path = False

        except Exception as e:
            self.false_path = NodeError.format(e)
            self.true_path = False
            self.results = []
            self.row_count = 0
            self.columns = []
            self.results_json = "[]"
            self.info = {}
