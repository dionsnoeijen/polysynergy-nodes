import asyncio
import json
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
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
    name="Section Upsert",
    category="section",
    icon='database.svg',
    version=1.0,
)
class SectionUpsert(Node):
    """
    Upsert (Insert or Update) a record in a section.

    If a record with the given record_id exists, it will be updated.
    If not, a new record will be created with that ID.

    This is perfect for idempotent operations where you want to ensure
    a record exists with specific values, regardless of whether it
    already exists or not.

    Use case: Agent generates leads with deterministic IDs from company names.
    Each run should update the existing record, not create duplicates.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to upsert the record in"
    )

    record_id: str = NodeVariableSettings(
        label="Record ID",
        dock=True,
        has_in=True,
        info="UUID of the record (will create with this ID if not exists, or update if exists)"
    )

    field_data: dict = NodeVariableSettings(
        label="Field Data",
        dock=dock_json(),
        has_in=True,
        default={},
        info="JSON object with field values. Example: {\"first_name\": \"John\", \"last_name\": \"Doe\"}"
    )

    # Outputs
    record_id_out: str = NodeVariableSettings(
        label="Record ID",
        has_out=True,
        info="The UUID of the record"
    )

    was_created: bool = NodeVariableSettings(
        label="Was Created",
        has_out=True,
        info="True if record was created (didn't exist), False if it was updated (already existed)"
    )

    # Paths
    true_path: bool | dict = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        """Upsert a record in the section"""
        try:
            print(f"\n[Section Upsert] ========== Upserting Record ==========")

            # Resolve placeholders into local vars (don't mutate self)
            section_id = replace_placeholders(
                data=self.section_id, values=self.__dict__, state=self.state, current_node=self
            )
            record_id = replace_placeholders(
                data=self.record_id, values=self.__dict__, state=self.state, current_node=self
            )
            field_data = replace_placeholders(
                data=self.field_data, values=self.__dict__, state=self.state, current_node=self
            )

            # Validate inputs
            if not section_id:
                raise ValueError("Section ID is required")

            if not record_id:
                raise ValueError("Record ID is required")

            if not isinstance(field_data, dict):
                raise ValueError("Field data must be a JSON object (dict)")

            # Remove system fields (managed automatically by the repository)
            system_fields = {'id', 'created_at', 'updated_at'}
            field_data = {k: v for k, v in field_data.items() if k not in system_fields}

            # Sanitize field_data: convert non-serializable types to strings
            sanitized_data = {}
            for k, v in field_data.items():
                if isinstance(v, (datetime, date)):
                    sanitized_data[k] = v.isoformat()
                elif isinstance(v, Decimal):
                    sanitized_data[k] = float(v)
                elif isinstance(v, UUID):
                    sanitized_data[k] = str(v)
                else:
                    sanitized_data[k] = v
            field_data = sanitized_data

            # Convert IDs to UUIDs
            try:
                section_uuid = UUID(section_id)
                record_uuid = UUID(record_id)
            except (ValueError, AttributeError) as e:
                raise ValueError(f"Invalid UUID format: {str(e)}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_upsert():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Upsert] Section: {section_info['label']}")
                print(f"[Section Upsert] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Create content repository
                content_repo = NodeContentRepository(section_info)

                # Check if record exists
                existing_record = content_repo.get_by_id(record_uuid)

                if existing_record:
                    # Record exists - UPDATE
                    print(f"[Section Upsert] Record exists - updating")
                    updated_record = content_repo.update(record_uuid, {**field_data})
                    return updated_record, False  # False = was not created (was updated)
                else:
                    # Record doesn't exist - CREATE with explicit ID
                    print(f"[Section Upsert] Record doesn't exist - creating with ID {record_uuid}")

                    # Add ID to field_data
                    create_data = {**field_data, "id": str(record_uuid)}
                    created_record = content_repo.create(create_data)
                    return created_record, True  # True = was created

            # Run in thread pool to avoid blocking
            result_record, was_created = await asyncio.to_thread(_sync_upsert)

            action = "created" if was_created else "updated"
            print(f"[Section Upsert] ✓ Record {action} successfully")
            print(f"[Section Upsert] Record ID: {result_record.get('id')}")

            self.record_id_out = str(result_record.get('id'))
            self.was_created = was_created

            # Take success path
            self.true_path = result_record

        except Exception as e:
            print(f"[Section Upsert] ✗ Error: {str(e)}")
            self.record_id_out = None
            self.was_created = False
            self.false_path = NodeError.format(e)
