"""PostgreSQL connection implementation."""

import asyncio
from typing import Any, Dict, List

from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection


class PostgresqlConnection(BaseSqlConnection):
    """PostgreSQL database connection implementation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize PostgreSQL connection.

        Args:
            config: Configuration dictionary with host, port, database_name, username, password, use_ssl
        """
        super().__init__(config)
        self.host = config.get('host')
        self.port = config.get('port', 5432)
        self.database_name = config.get('database_name')
        self.username = config.get('username')
        self.password = config.get('password')
        self.use_ssl = config.get('use_ssl', False)

        if not all([self.host, self.database_name, self.username, self.password]):
            raise ValueError("host, database_name, username, and password are required for PostgreSQL")

    async def execute_query(self, query: str, parameters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        """Execute SQL query against PostgreSQL database.

        Args:
            query: SQL query to execute
            parameters: Optional parameters for parameterized queries

        Returns:
            List of dictionaries with query results
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except ImportError:
            raise ImportError(
                "psycopg2 package required for PostgreSQL. "
                "Install with: poetry add psycopg2-binary"
            )

        def _sync_execute():
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database_name,
                user=self.username,
                password=self.password,
                sslmode='require' if self.use_ssl else 'prefer'
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            try:
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)

                # Fetch results if this is a SELECT query
                if cursor.description:
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
                else:
                    # For INSERT/UPDATE/DELETE, commit and return empty list
                    conn.commit()
                    return []
            finally:
                cursor.close()
                conn.close()

        return await asyncio.to_thread(_sync_execute)

    async def close(self):
        """Close connection (PostgreSQL connections are opened/closed per query)."""
        pass  # Connections are opened/closed in execute_query

    @property
    def database_type(self) -> str:
        """Return database type identifier."""
        return "postgresql"
