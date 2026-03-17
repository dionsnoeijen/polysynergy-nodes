"""MongoDB connection implementation."""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

import pymongo
from bson import ObjectId


class MongoDBConnection:
    """MongoDB database connection implementation."""

    _WRITE_OPERATIONS = {"insert_one", "insert_many", "update_one", "update_many", "delete_one", "delete_many"}

    def __init__(self, config: Dict[str, Any], read_only: bool = True):
        """Initialize MongoDB connection.

        Args:
            config: Configuration dictionary with host, port, database, username,
                    password, auth_source, and optionally connection_string
            read_only: When True, blocks all write operations
        """
        self.config = config
        self.read_only = read_only
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 27017)
        self.database = config.get("database")
        self.username = config.get("username")
        self.password = config.get("password")
        self.auth_source = config.get("auth_source", "admin")
        self.connection_string = config.get("connection_string")

        if not self.database:
            raise ValueError("database is required for MongoDB connection")

    def _check_write_allowed(self, operation: str):
        """Raise an error if a write operation is attempted in read-only mode."""
        if self.read_only and operation in self._WRITE_OPERATIONS:
            raise PermissionError(f"Operation '{operation}' is blocked: connection is in read-only mode")

    def _build_client(self):
        """Build and return a MongoClient instance."""
        if self.connection_string:
            client = pymongo.MongoClient(self.connection_string)
        else:
            kwargs: Dict[str, Any] = {
                "host": self.host,
                "port": self.port,
            }
            if self.username and self.password:
                kwargs["username"] = self.username
                kwargs["password"] = self.password
                kwargs["authSource"] = self.auth_source

            client = pymongo.MongoClient(**kwargs)

        return client

    def get_collection(self, name: str):
        """Return a collection from the configured database.

        Args:
            name: Collection name

        Returns:
            pymongo Collection object
        """
        client = self._build_client()
        db = client[self.database]
        return db[name]

    async def list_collections(self) -> List[str]:
        """List all collection names in the configured database."""
        def _sync_list():
            client = self._build_client()
            try:
                return client[self.database].list_collection_names()
            finally:
                client.close()

        return await asyncio.to_thread(_sync_list)

    async def find(
        self,
        collection: str,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Any]] = None,
        limit: int = 0,
        sort: Optional[List] = None,
    ) -> List[Dict[str, Any]]:
        """Find documents in a collection.

        Args:
            collection: Collection name
            query: MongoDB query filter (default: {})
            projection: Fields to include/exclude
            limit: Maximum number of documents to return (0 = no limit)
            sort: Sort specification as list of (key, direction) tuples

        Returns:
            List of matching documents
        """
        def _sync_find():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                cursor = col.find(query or {}, projection or {})
                if sort:
                    cursor = cursor.sort(sort)
                if limit:
                    cursor = cursor.limit(limit)
                return [self._serialize_doc(doc) for doc in cursor]
            finally:
                client.close()

        return await asyncio.to_thread(_sync_find)

    async def aggregate(
        self,
        collection: str,
        pipeline: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Run an aggregation pipeline on a collection.

        Args:
            collection: Collection name
            pipeline: MongoDB aggregation pipeline

        Returns:
            List of result documents
        """
        def _sync_aggregate():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                return [self._serialize_doc(doc) for doc in col.aggregate(pipeline)]
            finally:
                client.close()

        return await asyncio.to_thread(_sync_aggregate)

    async def insert_one(
        self,
        collection: str,
        document: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Insert a single document into a collection.

        Args:
            collection: Collection name
            document: Document to insert

        Returns:
            Result dict with inserted_id
        """
        self._check_write_allowed("insert_one")

        def _sync_insert_one():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                result = col.insert_one(document)
                return {"inserted_id": str(result.inserted_id)}
            finally:
                client.close()

        return await asyncio.to_thread(_sync_insert_one)

    async def insert_many(
        self,
        collection: str,
        documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Insert multiple documents into a collection.

        Args:
            collection: Collection name
            documents: List of documents to insert

        Returns:
            Result dict with inserted_ids and inserted_count
        """
        self._check_write_allowed("insert_many")

        def _sync_insert_many():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                result = col.insert_many(documents)
                return {
                    "inserted_ids": [str(oid) for oid in result.inserted_ids],
                    "inserted_count": len(result.inserted_ids),
                }
            finally:
                client.close()

        return await asyncio.to_thread(_sync_insert_many)

    async def update_one(
        self,
        collection: str,
        filter: Dict[str, Any],
        update: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update a single document matching the filter.

        Args:
            collection: Collection name
            filter: Query filter to select the document
            update: Update operations to apply

        Returns:
            Result dict with matched_count and modified_count
        """
        self._check_write_allowed("update_one")

        def _sync_update_one():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                result = col.update_one(filter, update)
                return {
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count,
                }
            finally:
                client.close()

        return await asyncio.to_thread(_sync_update_one)

    async def update_many(
        self,
        collection: str,
        filter: Dict[str, Any],
        update: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update all documents matching the filter.

        Args:
            collection: Collection name
            filter: Query filter to select documents
            update: Update operations to apply

        Returns:
            Result dict with matched_count and modified_count
        """
        self._check_write_allowed("update_many")

        def _sync_update_many():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                result = col.update_many(filter, update)
                return {
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count,
                }
            finally:
                client.close()

        return await asyncio.to_thread(_sync_update_many)

    async def delete_one(
        self,
        collection: str,
        filter: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Delete a single document matching the filter.

        Args:
            collection: Collection name
            filter: Query filter to select the document

        Returns:
            Result dict with deleted_count
        """
        self._check_write_allowed("delete_one")

        def _sync_delete_one():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                result = col.delete_one(filter)
                return {"deleted_count": result.deleted_count}
            finally:
                client.close()

        return await asyncio.to_thread(_sync_delete_one)

    async def delete_many(
        self,
        collection: str,
        filter: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Delete all documents matching the filter.

        Args:
            collection: Collection name
            filter: Query filter to select documents

        Returns:
            Result dict with deleted_count
        """
        self._check_write_allowed("delete_many")

        def _sync_delete_many():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                result = col.delete_many(filter)
                return {"deleted_count": result.deleted_count}
            finally:
                client.close()

        return await asyncio.to_thread(_sync_delete_many)

    async def count_documents(
        self,
        collection: str,
        filter: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Count documents in a collection matching the filter.

        Args:
            collection: Collection name
            filter: Query filter (default: {})

        Returns:
            Number of matching documents
        """
        def _sync_count():
            client = self._build_client()
            try:
                col = client[self.database][collection]
                return col.count_documents(filter or {})
            finally:
                client.close()

        return await asyncio.to_thread(_sync_count)

    async def close(self):
        """Close connection (connections are opened/closed per operation)."""
        pass  # Connections are opened and closed per operation

    @property
    def database_type(self) -> str:
        """Return database type identifier."""
        return "mongodb"

    @staticmethod
    def _serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize a MongoDB document to a JSON-compatible dict.

        Converts ObjectId and other BSON types to their string representations.

        Args:
            doc: Raw MongoDB document

        Returns:
            JSON-serializable dictionary
        """
        result = {}
        for key, value in doc.items():
            result[key] = MongoDBConnection._serialize_value(value)
        return result

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Recursively serialize a BSON value to a JSON-compatible type."""
        if isinstance(value, ObjectId):
            return str(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, dict):
            return {k: MongoDBConnection._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [MongoDBConnection._serialize_value(item) for item in value]
        else:
            return value
