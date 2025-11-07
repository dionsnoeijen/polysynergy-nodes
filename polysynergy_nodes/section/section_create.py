import asyncio
import json
from typing import Dict, Any
from uuid import UUID

from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_json
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.section.repositories.db_session import get_main_db_session
from polysynergy_nodes.section.repositories.node_section_repository import NodeSectionRepository
from polysynergy_nodes.section.repositories.node_content_repository import NodeContentRepository


@node(
    name="Section Create",
    category="section",
    icon='database.svg',
    version=1.0,
)
class SectionCreate(Node):
    """
    Create a new record in a section.

    Calls the Content API to create a record in the specified section's table.
    Returns the created record with id and timestamps.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to create a record in. Frontend will populate this dropdown with available sections from the portal store."
    )

    field_data: dict = NodeVariableSettings(
        label="Field Data",
        dock=dock_json(),
        has_in=True,
        default={},
        info="JSON object with field values. Example: {\"first_name\": \"John\", \"last_name\": \"Doe\"}"
    )

    record_id: str = NodeVariableSettings(
        label="Record ID",
        has_out=True,
        info="The UUID of the created record (for easy passing to other nodes)"
    )

    # Paths
    true_path: bool | dict = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        """Create a new record in the section"""
        try:
            print(f"\n[Section Create] ========== Creating Record ==========")
            print(f"[Section Create] Section ID: {self.section_id}")
            print(f"[Section Create] Field Data: {json.dumps(self.field_data, indent=2)}")

            # Validate inputs
            if not self.section_id:
                raise ValueError("Section ID is required")

            if not isinstance(self.field_data, dict):
                raise ValueError("Field data must be a JSON object (dict)")

            # Convert section_id string to UUID
            try:
                section_uuid = UUID(self.section_id)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid section ID format: {self.section_id}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_create():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Create] Section: {section_info['label']}")
                print(f"[Section Create] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Create record in content table
                content_repo = NodeContentRepository(section_info)
                created_record = content_repo.create(self.field_data)

                return created_record

            # Run in thread pool to avoid blocking
            created_record = await asyncio.to_thread(_sync_create)

            print(f"[Section Create] ✓ Record created successfully")
            print(f"[Section Create] Record ID: {created_record.get('id')}")

            self.record_id = str(created_record.get('id'))

            # Take success path
            self.true_path = created_record

        except Exception as e:
            print(f"[Section Create] ✗ Error: {str(e)}")
            self.record_id = None
            self.false_path = NodeError.format(e)
