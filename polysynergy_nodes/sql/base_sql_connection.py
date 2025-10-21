"""Base SQL Connection class for type hinting and connection management."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseSqlConnection(ABC):
    """Base class for SQL database connections.

    All SQL connection implementations should inherit from this class.
    This allows for proper type hinting and service discovery.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize connection with configuration."""
        self.config = config

    @abstractmethod
    async def execute_query(self, query: str, parameters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as list of dictionaries.

        Args:
            query: SQL query string to execute
            parameters: Optional parameters for parameterized queries

        Returns:
            List of dictionaries, each representing one row
        """
        pass

    @abstractmethod
    async def close(self):
        """Close the database connection."""
        pass

    @property
    @abstractmethod
    def database_type(self) -> str:
        """Return the database type (sqlite, postgresql, mysql, etc.)."""
        pass
