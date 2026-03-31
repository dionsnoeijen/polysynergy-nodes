import asyncio
import json
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
    name="Section Create Many",
    category="section",
    icon="database.svg",
    version=1.0,
)
class SectionCreateMany(Node):
    """
    Create multiple records in a section at once.

    Accepts a list of objects and creates each as a record in the specified
    section's table. Returns all created records with ids and timestamps.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to create records in."
    )

    records: list = NodeVariableSettings(
        label="Records",
        dock=dock_json(),
        has_in=True,
        default=[],
        info="JSON array of objects. Each object becomes a record. Example: [{\"name\": \"Alice\"}, {\"name\": \"Bob\"}]"
    )

    count: int = NodeVariableSettings(
        label="Count",
        has_out=True,
        info="Number of records successfully created"
    )

    # Paths
    true_path: bool | list = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        """Create multiple records in the section"""
        try:
            print(f"\n[Section Create Many] ========== Creating Records ==========")

            # Resolve placeholders into local vars (don't mutate self)
            section_id = replace_placeholders(
                data=self.section_id, values=self.__dict__, state=self.state, current_node=self
            )
            records = replace_placeholders(
                data=self.records, values=self.__dict__, state=self.state, current_node=self
            )

            # Validate inputs
            if not section_id:
                raise ValueError("Section ID is required")

            records_data = records
            if isinstance(records_data, str):
                records_data = json.loads(records_data)

            if not isinstance(records_data, list):
                raise ValueError("Records must be a JSON array (list)")

            if not records_data:
                raise ValueError("Records list is empty")

            print(f"[Section Create Many] Records to create: {len(records_data)}")

            # Convert section_id string to UUID
            try:
                section_uuid = UUID(section_id)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid section ID format: {section_id}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_create_many():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Create Many] Section: {section_info['label']}")
                print(f"[Section Create Many] Table: {section_info['schema_name']}.{section_info['table_name']}")

                content_repo = NodeContentRepository(section_info)

                created_records = []
                errors = []
                for i, record_data in enumerate(records_data):
                    if not isinstance(record_data, dict):
                        errors.append(f"Record [{i}] is not a JSON object, skipping")
                        continue
                    try:
                        created = content_repo.create(record_data)
                        created_records.append(created)
                    except Exception as e:
                        errors.append(f"Record [{i}]: {str(e)}")

                if errors:
                    for err in errors:
                        print(f"[Section Create Many] Warning: {err}")

                return created_records

            # Run in thread pool to avoid blocking
            created_records = await asyncio.to_thread(_sync_create_many)

            print(f"[Section Create Many] Created {len(created_records)}/{len(records_data)} records")

            self.count = len(created_records)
            self.true_path = created_records

        except Exception as e:
            print(f"[Section Create Many] Error: {str(e)}")
            self.count = 0
            self.false_path = NodeError.format(e)
