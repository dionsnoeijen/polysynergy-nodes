import asyncio
import json
from uuid import UUID

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.section.repositories.db_session import get_main_db_session
from polysynergy_nodes.section.repositories.node_section_repository import NodeSectionRepository
from polysynergy_nodes.section.repositories.node_content_repository import NodeContentRepository


@node(
    name="Section Read",
    category="section",
    icon='database.svg',
    version=1.0,
)
class SectionRead(Node):
    """
    Read a single record from a section by ID.

    Calls the Content API to fetch a specific record from a section's table.
    Returns the complete record with all field values.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to read from. Frontend will populate this dropdown with available sections from the portal store."
    )

    # Paths
    true_path: bool | dict = PathSettings(label="Found")
    false_path: bool | dict = PathSettings(label="Not Found / Error")

    async def execute(self):
        """Read a record from the section"""
        try:
            print(f"\n[Section Read] ========== Reading Record ==========")
            print(f"[Section Read] Section ID: {self.section_id}")
            print(f"[Section Read] Record ID: {self.record_id}")

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
            def _sync_read():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Read] Section: {section_info['label']}")
                print(f"[Section Read] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Read record from content table
                content_repo = NodeContentRepository(section_info)
                record_data = content_repo.get_by_id(record_uuid)

                return record_data

            # Run in thread pool to avoid blocking
            record_data = await asyncio.to_thread(_sync_read)

            if record_data:
                print(f"[Section Read] ✓ Record found")
                print(f"[Section Read] Record: {json.dumps(record_data, indent=2, default=str)[:200]}...")

                # Take success path
                self.true_path = record_data
            else:
                # Record not found
                print(f"[Section Read] ✗ Record not found")
                self.false_path = {"error": "Record not found"}

        except Exception as e:
            print(f"[Section Read] ✗ Error: {str(e)}")
            self.false_path = NodeError.format(e)
