"""
SectionPgVector - Agno PgVector wrapper for PolySynergy sections

This class extends Agno's PgVector to provide automatic embedding sync
for section records, making section data searchable via semantic/hybrid search.
"""
from typing import Optional, Dict, Any
from agno.vectordb.pgvector import PgVector
from agno.knowledge.document import Document
from agno.vectordb.search import SearchType
from agno.vectordb.distance import Distance


class SectionPgVector(PgVector):
    """
    PgVector wrapper for PolySynergy sections.

    Automatically syncs section records to Agno-compatible embeddings table.
    Creates table: {project_schema}._section_{section_id}_embeddings
    """

    def __init__(
        self,
        section_id: str,
        project_schema: str,
        db_url: str,
        embedder=None,
        search_type: SearchType = SearchType.hybrid,
        distance: Distance = Distance.cosine,
        **kwargs
    ):
        """
        Initialize with section-specific settings.

        Args:
            section_id: UUID of the section
            project_schema: Project schema name (e.g., "project_abc123")
            db_url: Database connection URL for sections_db
            embedder: Embedder instance (OpenAI, Mistral, etc.)
            search_type: Type of search (vector, keyword, hybrid)
            distance: Distance metric (cosine, l2, max_inner_product)
            **kwargs: Additional PgVector arguments
        """
        # Generate unique but short table name for this section
        # Format: _sec_{uuid_without_dashes}_emb
        # PostgreSQL has 63 char limit for identifiers, and indexes add prefixes
        clean_section_id = section_id.replace('-', '')
        table_name = f"_sec_{clean_section_id}_emb"

        # Initialize parent PgVector with section-specific config
        super().__init__(
            table_name=table_name,
            schema=project_schema,
            db_url=db_url,
            embedder=embedder,
            search_type=search_type,
            distance=distance,
            **kwargs
        )

        self.section_id = section_id
        self.project_schema = project_schema

    def sync_from_section_record(
        self,
        record_id: str,
        content: str,
        meta_data: Dict[str, Any],
        name: Optional[str] = None
    ) -> None:
        """
        Sync a section record to embeddings table.

        Called automatically by ContentRepository on create/update.

        Args:
            record_id: UUID of the section record
            content: Combined text from source_fields
            meta_data: Metadata dictionary (from metadata_fields config)
            name: Display name for the document (optional)
        """
        # Create Document with section metadata
        doc = Document(
            id=f"section_{self.section_id}_{record_id}",
            name=name or record_id,
            content=content,
            content_id=record_id,  # Link back to original section record
            meta_data={
                **meta_data,
                "source_section_id": self.section_id,
                "source_record_id": record_id
            }
        )

        # Use Agno's upsert logic (insert or update)
        # content_hash = record_id ensures idempotency:
        # - Same record_id → same embedding (update instead of duplicate)
        # - Different content → embedding is recalculated and updated
        self.upsert(content_hash=record_id, documents=[doc])

    def delete_by_record_id(self, record_id: str) -> bool:
        """
        Delete embeddings for a specific section record.

        Args:
            record_id: UUID of the section record to delete

        Returns:
            bool: True if deletion was successful
        """
        doc_id = f"section_{self.section_id}_{record_id}"
        return self.delete_by_id(doc_id)
