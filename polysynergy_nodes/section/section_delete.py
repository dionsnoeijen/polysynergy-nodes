import asyncio
from uuid import UUID

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.section.repositories.db_session import get_main_db_session
from polysynergy_nodes.section.repositories.node_section_repository import NodeSectionRepository
from polysynergy_nodes.section.repositories.node_content_repository import NodeContentRepository


@node(
    name="Section Delete",
    category="section",
    icon='database.svg',
    version=1.0,
)
class SectionDelete(Node):
    """
    Delete a record from a section.

    Permanently deletes a record from a section's table.
    This is a hard delete - the record cannot be recovered.
    Returns success status and the deleted record ID.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section containing the record to delete. Frontend will populate this dropdown with available sections from the portal store."
    )

    record_id: str = NodeVariableSettings(
        label="Record ID",
        dock=True,
        has_in=True,
        info="The UUID of the record to delete"
    )

    # Outputs
    success: bool = NodeVariableSettings(
        label="Success",
        has_out=True,
        info="True if the record was deleted, False otherwise"
    )

    deleted_id: str = NodeVariableSettings(
        label="Deleted ID",
        has_out=True,
        info="The UUID of the deleted record (for confirmation)"
    )

    # Paths
    true_path: bool = PathSettings(label="Deleted")
    false_path: bool = PathSettings(label="Not Found / Error")

    async def execute(self):
        """Delete a record from the section"""
        try:
            print(f"\n[Section Delete] ========== Deleting Record ==========")
            print(f"[Section Delete] Section ID: {self.section_id}")
            print(f"[Section Delete] Record ID: {self.record_id}")

            # Validate inputs
            if not self.section_id:
                raise ValueError("Section ID is required")

            if not self.record_id:
                raise ValueError("Record ID is required")

            # Convert IDs to UUIDs
            try:
                section_uuid = UUID(self.section_id)
                record_uuid = UUID(self.record_id)
            except (ValueError, AttributeError) as e:
                raise ValueError(f"Invalid UUID format: {str(e)}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_delete():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Delete] Section: {section_info['label']}")
                print(f"[Section Delete] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Delete record from content table
                content_repo = NodeContentRepository(section_info)
                deleted = content_repo.delete(record_uuid)

                return deleted

            # Run in thread pool to avoid blocking
            deleted = await asyncio.to_thread(_sync_delete)

            if deleted:
                print(f"[Section Delete] ✓ Record deleted successfully")

                # Set outputs
                self.success = True
                self.deleted_id = self.record_id

                # Take success path
                self.true_path = True
            else:
                # Record not found
                print(f"[Section Delete] ✗ Record not found")
                self.success = False
                self.deleted_id = None
                self.false_path = True

        except Exception as e:
            print(f"[Section Delete] ✗ Error: {str(e)}")
            self.success = False
            self.deleted_id = None
            self.false_path = True
