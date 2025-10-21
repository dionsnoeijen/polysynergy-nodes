"""SQLite connection implementation."""

import sqlite3
import asyncio
from typing import Any, Dict, List

from polysynergy_nodes.sql.base_sql_connection import BaseSqlConnection


class SqliteConnection(BaseSqlConnection):
    """SQLite database connection implementation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize SQLite connection.

        Args:
            config: Configuration dictionary with 'database_file' key
        """
        super().__init__(config)
        self.database_file = config.get('database_file')
        if not self.database_file:
            raise ValueError("database_file is required for SQLite connection")

    async def execute_query(self, query: str, parameters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        """Execute SQL query against SQLite database.

        Args:
            query: SQL query to execute
            parameters: Optional parameters for parameterized queries

        Returns:
            List of dictionaries with query results
        """
        def _sync_execute():
            conn = sqlite3.connect(self.database_file)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            cursor = conn.cursor()

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
        """Close connection (SQLite connections are opened/closed per query)."""
        pass  # SQLite connections are opened/closed in execute_query

    @property
    def database_type(self) -> str:
        """Return database type identifier."""
        return "sqlite"
