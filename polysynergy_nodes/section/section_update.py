import asyncio
import json
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
    name="Section Update",
    category="section",
    icon='database.svg',
    version=1.0,
)
class SectionUpdate(Node):
    """
    Update an existing record in a section.

    Updates a record in the specified section's table.
    Only the fields provided in field_data will be updated (partial update).
    Returns the updated record.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section containing the record to update. Frontend will populate this dropdown with available sections from the portal store."
    )

    record_id: str = NodeVariableSettings(
        label="Record ID",
        dock=True,
        has_in=True,
        info="The UUID of the record to update"
    )

    field_data: dict = NodeVariableSettings(
        label="Field Data",
        dock=dock_json(),
        has_in=True,
        default={},
        info="JSON object with field values to update. Only include fields you want to change. Example: {\"first_name\": \"Jane\"}"
    )

    # Paths
    true_path: bool | dict = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error / Not Found")

    async def execute(self):
        """Update a record in the section"""
        try:
            print(f"\n[Section Update] ========== Updating Record ==========")
            print(f"[Section Update] Section ID: {self.section_id}")
            print(f"[Section Update] Record ID: {self.record_id}")
            print(f"[Section Update] Field Data: {json.dumps(self.field_data, indent=2)}")

            # Validate inputs
            if not self.section_id:
                raise ValueError("Section ID is required")

            if not self.record_id:
                raise ValueError("Record ID is required")

            if not isinstance(self.field_data, dict):
                raise ValueError("Field data must be a JSON object (dict)")

            # Convert IDs to UUIDs
            try:
                section_uuid = UUID(self.section_id)
                record_uuid = UUID(self.record_id)
            except (ValueError, AttributeError) as e:
                raise ValueError(f"Invalid UUID format: {str(e)}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_update():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Update] Section: {section_info['label']}")
                print(f"[Section Update] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Update record in content table
                content_repo = NodeContentRepository(section_info)
                updated_record = content_repo.update(record_uuid, self.field_data)

                return updated_record

            # Run in thread pool to avoid blocking
            updated_record = await asyncio.to_thread(_sync_update)

            print(f"[Section Update] ✓ Record updated successfully")
            print(f"[Section Update] Updated at: {updated_record.get('updated_at')}")

            # Take success path
            self.true_path = updated_record

        except ValueError as e:
            # Record not found or validation error
            error_msg = str(e)
            print(f"[Section Update] ✗ {error_msg}")
            self.record = {"error": error_msg}
            self.false_path = NodeError.format(e)

        except Exception as e:
            print(f"[Section Update] ✗ Error: {str(e)}")
            self.record = {"error": str(e)}
            self.false_path = NodeError.format(e)
