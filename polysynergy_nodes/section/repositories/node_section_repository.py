"""Section Repository for Nodes - Simplified version without project auth context"""

import os
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session


class NodeSectionRepository:
    """
    Simplified section repository for use in nodes.

    Unlike the API repository, this doesn't require project authentication context.
    It uses PROJECT_ID from environment to generate the schema_name directly,
    just like the Project model does with its schema_name property.
    """

    def __init__(self, session: Session):
        self.session = session
        self.project_id = os.getenv('PROJECT_ID')
        if not self.project_id:
            raise ValueError("PROJECT_ID environment variable is required")

        # Generate schema_name exactly like Project model does
        self.schema_name = f"project_{str(self.project_id).replace('-', '_')}"

    def get_by_id(self, section_id: UUID) -> dict:
        """
        Get section information by ID.

        Returns a dict with:
        - id: UUID
        - handle: str
        - table_name: str
        - schema_name: str (generated from PROJECT_ID)
        - database_url: str (connection string for content database)
        - field_assignments: list of field info
        """
        sql = text("""
            SELECT
                s.id,
                s.handle,
                s.table_name,
                s.label,
                s.database_connection_id,
                s.vectorization_config,
                dc.database_type,
                dc.host,
                dc.port,
                dc.database_name,
                dc.username,
                dc.password,
                dc.file_path
            FROM sections s
            LEFT JOIN database_connections dc ON s.database_connection_id = dc.id
            WHERE s.id = :section_id
            AND s.project_id = :project_id
            AND s.deleted_at IS NULL
        """)

        result = self.session.execute(sql, {
            "section_id": str(section_id),
            "project_id": str(self.project_id)
        })
        row = result.fetchone()

        if not row:
            raise ValueError(f"Section {section_id} not found in project {self.project_id}")

        # Get field assignments
        fields_sql = text("""
            SELECT
                f.handle,
                f.label,
                f.field_type_handle,
                f.field_settings
            FROM section_field_assignments sfa
            JOIN fields f ON sfa.field_id = f.id
            WHERE sfa.section_id = :section_id
            ORDER BY sfa.sort_order
        """)

        fields_result = self.session.execute(fields_sql, {
            "section_id": str(section_id)
        })
        field_assignments = [
            {
                "handle": row.handle,
                "label": row.label,
                "field_type_handle": row.field_type_handle,
                "field_settings": row.field_settings
            }
            for row in fields_result.fetchall()
        ]

        # Determine database URL
        if row.database_connection_id:
            # Build connection string from database_connection fields
            database_type = row.database_type

            if database_type == "sqlite":
                database_url = f"sqlite:///{row.file_path}"
            else:
                # PostgreSQL, MySQL, etc.
                auth = f"{row.username}:{row.password}@" if row.username and row.password else ""
                port = f":{row.port}" if row.port else ""
                database_url = f"{database_type}://{auth}{row.host}{port}/{row.database_name}"
        else:
            # Use default sections_db - import the properly built URL
            from polysynergy_nodes.section.repositories.db_session import SECTIONS_DATABASE_URL
            database_url = SECTIONS_DATABASE_URL

        return {
            "id": row.id,
            "handle": row.handle,
            "table_name": row.table_name,
            "label": row.label,
            "schema_name": self.schema_name,  # Use generated schema_name from PROJECT_ID
            "database_url": database_url,
            "vectorization_config": row.vectorization_config,
            "field_assignments": field_assignments
        }
