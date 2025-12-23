"""Content Repository for Nodes - Dynamic CRUD on section content tables"""

import os
import json
from uuid import UUID
from typing import Any, Optional
from datetime import datetime, timezone, date
from decimal import Decimal

from sqlalchemy import create_engine, text


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Decimal, UUID, datetime types."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to float
            return float(obj)
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class NodeContentRepository:
    """
    Repository for dynamic CRUD operations on section content tables.

    This is a simplified version adapted from api-local's ContentRepository,
    designed for use in nodes without project authentication context.

    Supports automatic vectorization when section has vectorization_config enabled.
    """

    def __init__(self, section_info: dict):
        """
        Initialize repository with section information.

        Args:
            section_info: Dict from NodeSectionRepository.get_by_id() containing:
                - id: UUID
                - schema_name: str
                - table_name: str
                - database_url: str
                - field_assignments: list
                - vectorization_config: dict (optional)
                - label: str (optional, section name)
        """
        self.section_id = str(section_info["id"])
        self.section_label = section_info.get("label", "Unknown Section")
        self.schema_name = section_info["schema_name"]
        self.table_name = section_info["table_name"]
        self.full_table_name = f'"{self.schema_name}"."{self.table_name}"'
        self.field_assignments = section_info["field_assignments"]
        self.vectorization_config = section_info.get("vectorization_config")

        # DEBUG: Print vectorization config
        print(f"[NodeContentRepository.__init__] Section: {self.section_label} ({self.section_id})")
        print(f"[NodeContentRepository.__init__] vectorization_config type: {type(self.vectorization_config)}")
        print(f"[NodeContentRepository.__init__] vectorization_config: {self.vectorization_config}")

        if self.vectorization_config:
            print(f"[NodeContentRepository.__init__] enabled: {self.vectorization_config.get('enabled')}")

        # Create engine for content database
        self.content_engine = create_engine(section_info["database_url"])
        self.database_url = section_info["database_url"]

        # Initialize vector DB if vectorization is enabled
        self.vector_db = None
        if self.vectorization_config and self.vectorization_config.get("enabled"):
            print(f"[NodeContentRepository.__init__] ✓ Vectorization is enabled, calling _init_vector_db()")
            self._init_vector_db()
        else:
            print(f"[NodeContentRepository.__init__] ✗ Vectorization NOT enabled (config={self.vectorization_config})")

    def _prepare_data_for_db(self, data: dict) -> dict:
        """
        Prepare data for database insertion/update.

        Converts dict/list values to JSON strings for JSONB fields.
        PostgreSQL JSONB fields need to be passed as JSON strings when using text() SQL.

        Also detects and parses JSON strings that come from AI agents.
        """
        prepared_data = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # Serialize dict/list to JSON string for JSONB fields
                prepared_data[key] = json.dumps(value)
            elif isinstance(value, str) and value.strip().startswith(('[', '{')):
                # Detect JSON strings and parse them first, then re-serialize
                # This handles AI agents that return JSON as strings
                try:
                    parsed = json.loads(value)
                    prepared_data[key] = json.dumps(parsed)
                except json.JSONDecodeError:
                    # Not valid JSON, treat as regular string
                    prepared_data[key] = value
            else:
                prepared_data[key] = value
        return prepared_data

    def _serialize_result(self, row_mapping: dict) -> dict:
        """
        Serialize database result for JSON output.

        Converts UUID, datetime, Decimal, and other non-JSON-serializable types to strings.
        """
        result = {}
        for key, value in row_mapping.items():
            if isinstance(value, UUID):
                result[key] = str(value)
            elif isinstance(value, (datetime, date)):
                result[key] = value.isoformat()
            elif isinstance(value, Decimal):
                # Convert Decimal to float for JSON serialization
                result[key] = float(value)
            else:
                result[key] = value
        return result

    def create(self, data: dict) -> dict:
        """
        Create a new record in the content table.

        Args:
            data: Dictionary with field values

        Returns:
            Created record with id and timestamps
        """
        if not data:
            raise ValueError("No data provided for record creation")

        # Prepare data (serialize JSONB fields)
        prepared_data = self._prepare_data_for_db(data)

        # Build column and value lists
        columns = list(prepared_data.keys())
        placeholders = [f":{col}" for col in columns]

        columns_sql = ', '.join([f'"{col}"' for col in columns])
        placeholders_sql = ', '.join(placeholders)

        # Insert query with RETURNING
        sql = f"""
            INSERT INTO {self.full_table_name} ({columns_sql})
            VALUES ({placeholders_sql})
            RETURNING id, created_at, updated_at, {columns_sql}
        """

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), prepared_data)
            conn.commit()

            row = result.fetchone()
            if not row:
                raise RuntimeError("Failed to create record")

            # Convert row to dict and serialize UUIDs
            created_record = self._serialize_result(dict(row._mapping))

        # Sync to vector DB if vectorization is enabled
        self._sync_to_vector_db(created_record)

        return created_record

    def get_by_id(self, record_id: UUID) -> Optional[dict]:
        """
        Get a single record by ID.

        Args:
            record_id: UUID of the record

        Returns:
            Record dict or None if not found
        """
        sql = f"""
            SELECT * FROM {self.full_table_name}
            WHERE id = :record_id
        """

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), {"record_id": str(record_id)})
            row = result.fetchone()

            if not row:
                return None

            return self._serialize_result(dict(row._mapping))

    def get_all(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "created_at",
        order_direction: str = "DESC",
        search: Optional[str] = None,
        select_columns: list[str] | None = None
    ) -> list[dict]:
        """
        Get all records with pagination and optional search.

        Args:
            limit: Max number of records to return
            offset: Number of records to skip
            order_by: Column to order by
            order_direction: ASC or DESC
            search: Optional search term (searches all text fields using PostgreSQL FTS)
            select_columns: Optional list of column names to select. If None, selects all columns.

        Returns:
            List of record dicts
        """
        # Validate order_direction
        if order_direction.upper() not in ["ASC", "DESC"]:
            order_direction = "DESC"

        # Build SELECT clause
        if select_columns:
            columns_sql = ', '.join([f'"{col}"' for col in select_columns])
        else:
            columns_sql = '*'

        # Build WHERE clause for search
        where_clause = ""
        params = {"limit": limit, "offset": offset}

        if search:
            # Get all searchable columns from field assignments
            text_columns = []
            for field in self.field_assignments:
                field_type = field["field_type_handle"]
                # Include text, email, url fields in search
                if field_type in ['text', 'email', 'url']:
                    text_columns.append(field["handle"])

            if text_columns:
                # Use PostgreSQL Full Text Search with to_tsvector
                columns_concat = ' || \' \' || '.join([
                    f'COALESCE("{col}"::text, \'\')'
                    for col in text_columns
                ])

                # Use plainto_tsquery for simple search
                where_clause = f"""
                    WHERE to_tsvector('simple', {columns_concat}) @@ plainto_tsquery('simple', :search)
                """
                params['search'] = search

        sql = f"""
            SELECT {columns_sql} FROM {self.full_table_name}
            {where_clause}
            ORDER BY "{order_by}" {order_direction}
            LIMIT :limit OFFSET :offset
        """

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), params)
            return [self._serialize_result(dict(row._mapping)) for row in result.fetchall()]

    def count(self, search: Optional[str] = None) -> int:
        """
        Count total number of records.

        Args:
            search: Optional search term to filter count

        Returns:
            Total record count
        """
        where_clause = ""
        params = {}

        if search:
            # Get searchable columns
            text_columns = []
            for field in self.field_assignments:
                field_type = field["field_type_handle"]
                if field_type in ['text', 'email', 'url']:
                    text_columns.append(field["handle"])

            if text_columns:
                columns_concat = ' || \' \' || '.join([
                    f'COALESCE("{col}"::text, \'\')'
                    for col in text_columns
                ])
                where_clause = f"""
                    WHERE to_tsvector('simple', {columns_concat}) @@ plainto_tsquery('simple', :search)
                """
                params['search'] = search

        sql = f"SELECT COUNT(*) as count FROM {self.full_table_name} {where_clause}"

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), params)
            row = result.fetchone()
            return row[0] if row else 0

    def update(self, record_id: UUID, data: dict) -> dict:
        """
        Update a record.

        Args:
            record_id: UUID of the record
            data: Dictionary with field values to update

        Returns:
            Updated record dict
        """
        if not data:
            raise ValueError("No data provided for update")

        # Add updated_at timestamp
        data['updated_at'] = datetime.now(timezone.utc)

        # Prepare data (serialize JSONB fields)
        prepared_data = self._prepare_data_for_db(data)

        # Build SET clause
        set_clauses = [f'"{col}" = :{col}' for col in prepared_data.keys()]
        set_sql = ', '.join(set_clauses)

        sql = f"""
            UPDATE {self.full_table_name}
            SET {set_sql}
            WHERE id = :record_id
            RETURNING *
        """

        params = {**prepared_data, "record_id": str(record_id)}

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), params)
            conn.commit()

            row = result.fetchone()
            if not row:
                raise ValueError(f"Record {record_id} not found")

            updated_record = self._serialize_result(dict(row._mapping))

        # Sync to vector DB if vectorization is enabled
        self._sync_to_vector_db(updated_record)

        return updated_record

    def delete(self, record_id: UUID) -> bool:
        """
        Delete a record.

        Args:
            record_id: UUID of the record

        Returns:
            True if deleted, False if not found
        """
        sql = f"""
            DELETE FROM {self.full_table_name}
            WHERE id = :record_id
        """

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), {"record_id": str(record_id)})
            conn.commit()

            deleted = result.rowcount > 0

        # Delete from vector DB if vectorization is enabled
        if deleted:
            self._delete_from_vector_db(record_id)

        return deleted

    def query_with_where(
        self,
        where_clause: str,
        limit: int = 100,
        offset: int = 0,
        select_columns: list[str] | None = None
    ) -> list[dict]:
        """
        Execute custom WHERE query.

        Args:
            where_clause: SQL WHERE condition (without 'WHERE' keyword)
            limit: Max records to return
            offset: Number of records to skip
            select_columns: Optional list of column names to select. If None, selects all columns.

        Returns:
            List of matching records

        Warning:
            This method is potentially unsafe if where_clause contains
            user input without proper validation. Use with caution.
        """
        if not where_clause:
            return self.get_all(limit=limit, offset=offset, select_columns=select_columns)

        # Build SELECT clause
        if select_columns:
            columns_sql = ', '.join([f'"{col}"' for col in select_columns])
        else:
            columns_sql = '*'

        # Note: This is a simple implementation - production code should
        # validate/sanitize the where_clause to prevent SQL injection
        sql = f"""
            SELECT {columns_sql} FROM {self.full_table_name}
            WHERE {where_clause}
            LIMIT :limit OFFSET :offset
        """

        params = {"limit": limit, "offset": offset}

        with self.content_engine.connect() as conn:
            result = conn.execute(text(sql), params)
            return [self._serialize_result(dict(row._mapping)) for row in result.fetchall()]

    def _init_vector_db(self):
        """
        Initialize SectionPgVector instance for automatic embedding sync.

        Uses vectorization_config to set up embedder and vector search settings.
        """
        try:
            from polysynergy_nodes.section.vectordb.section_pgvector import SectionPgVector
            from agno.vectordb.search import SearchType
            from agno.vectordb.distance import Distance

            # Get embedder based on provider
            embedder = self._create_embedder()
            if not embedder:
                print(f"[Vectorization] Failed to create embedder - skipping vectorization for section {self.section_id}")
                return

            # Get search and distance settings
            search_type_str = self.vectorization_config.get("search_type", "hybrid")
            distance_str = self.vectorization_config.get("distance", "cosine")

            # Map strings to enums
            search_type = getattr(SearchType, search_type_str, SearchType.hybrid)
            distance = getattr(Distance, distance_str, Distance.cosine)

            # Create vector DB instance
            self.vector_db = SectionPgVector(
                section_id=self.section_id,
                project_schema=self.schema_name,
                db_url=self.database_url,
                embedder=embedder,
                search_type=search_type,
                distance=distance
            )

            print(f"[Vectorization] Initialized vector DB for section '{self.section_label}' with {search_type_str} search")

        except Exception as e:
            print(f"[Vectorization] Error initializing vector DB: {e}")
            self.vector_db = None

    def _create_embedder(self):
        """
        Create embedder instance based on vectorization_config.

        Returns:
            Embedder instance or None if creation failed
        """
        try:
            provider = self.vectorization_config.get("provider", "openai")
            model = self.vectorization_config.get("model", "text-embedding-3-small")
            dimensions = self.vectorization_config.get("dimensions", 1536)
            api_key_secret_id = self.vectorization_config.get("api_key_secret_id")

            # Resolve API key from environment or secrets manager
            api_key = self._resolve_api_key(provider, api_key_secret_id)
            if not api_key:
                print(f"[Vectorization] No API key found for provider '{provider}'")
                return None

            # Create embedder based on provider
            if provider == "openai":
                from agno.embedder.openai import OpenAIEmbedder
                return OpenAIEmbedder(
                    id=model,
                    dimensions=dimensions,
                    api_key=api_key
                )
            elif provider == "mistral":
                from agno.embedder.mistral import MistralEmbedder
                return MistralEmbedder(
                    id=model,
                    dimensions=dimensions,
                    api_key=api_key
                )
            else:
                print(f"[Vectorization] Unsupported provider: {provider}")
                return None

        except Exception as e:
            print(f"[Vectorization] Error creating embedder: {e}")
            return None

    def _resolve_api_key(self, provider: str, api_key_secret_id: Optional[str]) -> Optional[str]:
        """
        Resolve API key from environment variable or secret ID.

        Args:
            provider: Provider name (openai, mistral, etc.)
            api_key_secret_id: Optional secret ID to resolve

        Returns:
            API key string or None
        """
        # First try environment variable
        env_var_name = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var_name)
        if api_key:
            return api_key

        # If secret_id provided, try to resolve it
        # For now, we'll skip DynamoDB resolution in nodes and rely on env vars
        # TODO: Add secrets manager integration if needed
        if api_key_secret_id:
            print(f"[Vectorization] Secret ID provided but secrets resolution not implemented in nodes - use environment variables")

        return None

    def _sync_to_vector_db(self, record: dict):
        """
        Sync a record to the vector database for semantic search.

        Args:
            record: The full record dict with all fields
        """
        if not self.vector_db:
            return  # Vectorization not enabled or failed to initialize

        try:
            # Get source fields to combine into embedding content
            source_fields = self.vectorization_config.get("source_fields", [])
            if not source_fields:
                print(f"[Vectorization] No source_fields configured - skipping vectorization")
                return

            # Combine content from source fields
            content_parts = []
            for field_name in source_fields:
                value = record.get(field_name)
                if value:
                    # Convert to string, handle lists/dicts
                    if isinstance(value, (list, dict)):
                        value = json.dumps(value)
                    content_parts.append(str(value))

            combined_content = ' '.join(content_parts)
            if not combined_content.strip():
                print(f"[Vectorization] No content found in source fields - skipping")
                return

            # Get metadata fields
            metadata_fields = self.vectorization_config.get("metadata_fields", [])
            meta_data = {}
            for field_name in metadata_fields:
                if field_name in record:
                    meta_data[field_name] = record[field_name]

            # Get record ID and optional name
            record_id = str(record.get('id'))
            title_field = self.vectorization_config.get("title_field")  # Optional
            name = str(record.get(title_field)) if title_field and record.get(title_field) else record_id

            # Sync to vector DB
            self.vector_db.sync_from_section_record(
                record_id=record_id,
                content=combined_content,
                meta_data=meta_data,
                name=name
            )

            print(f"[Vectorization] Synced record {record_id} to vector DB")

        except Exception as e:
            # Don't fail the entire operation if vectorization fails
            print(f"[Vectorization] Error syncing record to vector DB: {e}")

    def _delete_from_vector_db(self, record_id: UUID):
        """
        Delete a record's embeddings from the vector database.

        Args:
            record_id: UUID of the record to delete
        """
        if not self.vector_db:
            return

        try:
            success = self.vector_db.delete_by_record_id(str(record_id))
            if success:
                print(f"[Vectorization] Deleted record {record_id} from vector DB")
        except Exception as e:
            print(f"[Vectorization] Error deleting from vector DB: {e}")
