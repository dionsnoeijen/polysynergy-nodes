import asyncio
import json
from typing import List, Dict, Any
from uuid import UUID

from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_select_values
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.section.repositories.db_session import get_main_db_session
from polysynergy_nodes.section.repositories.node_section_repository import NodeSectionRepository
from polysynergy_nodes.section.repositories.node_content_repository import NodeContentRepository


@node(
    name="Section List",
    category="section",
    icon='database.svg',
    version=1.0,
)
class SectionList(Node):
    """
    List records from a section with pagination, sorting, and search.

    Fetches multiple records from a section's table with support for
    pagination (limit/offset), sorting, and full-text search.
    Returns a list of records along with total count and pagination info.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to list records from. Frontend will populate this dropdown with available sections from the portal store."
    )

    limit: int = NodeVariableSettings(
        label="Limit",
        dock=True,
        has_in=True,
        default=100,
        info="Maximum number of records to return (1-1000)"
    )

    offset: int = NodeVariableSettings(
        label="Offset",
        dock=True,
        has_in=True,
        default=0,
        info="Number of records to skip (for pagination)"
    )

    order_by: str = NodeVariableSettings(
        label="Order By",
        dock=True,
        has_in=True,
        default="created_at",
        info="Column to order by (e.g., 'created_at', 'updated_at', or any field handle)"
    )

    order_direction: str = NodeVariableSettings(
        label="Order Direction",
        dock=dock_select_values(
            select_values={"ASC": "ASC", "DESC": "DESC"}
        ),
        has_in=True,
        default="DESC",
        info="Sort direction: ASC (ascending) or DESC (descending)"
    )

    search: str = NodeVariableSettings(
        label="Search",
        dock=True,
        has_in=True,
        default="",
        info="Search term (searches across all text fields using PostgreSQL Full Text Search)"
    )

    # Outputs
    total: int = NodeVariableSettings(
        label="Total",
        has_out=True,
        info="Total number of records in the section (not just returned records)"
    )

    has_more: bool = NodeVariableSettings(
        label="Has More",
        has_out=True,
        info="True if there are more records available (for pagination)"
    )

    count: int = NodeVariableSettings(
        label="Count",
        has_out=True,
        info="Number of records returned in this response"
    )

    # Paths
    true_path: bool | list = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        """List records from the section"""
        try:
            print(f"\n[Section List] ========== Listing Records ==========")
            print(f"[Section List] Section ID: {self.section_id}")
            print(f"[Section List] Limit: {self.limit}, Offset: {self.offset}")
            print(f"[Section List] Order: {self.order_by} {self.order_direction}")
            if self.search:
                print(f"[Section List] Search: '{self.search}'")

            # Validate inputs
            if not self.section_id:
                raise ValueError("Section ID is required")

            # Convert section_id to UUID
            try:
                section_uuid = UUID(self.section_id)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid section ID format: {self.section_id}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_list():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section List] Section: {section_info['label']}")
                print(f"[Section List] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Get records from content table
                content_repo = NodeContentRepository(section_info)
                records_list = content_repo.get_all(
                    limit=self.limit,
                    offset=self.offset,
                    order_by=self.order_by,
                    order_direction=self.order_direction,
                    search=self.search if self.search else None
                )

                # Get total count
                total_count = content_repo.count(search=self.search if self.search else None)

                return records_list, total_count

            # Run in thread pool to avoid blocking
            records_list, total_count = await asyncio.to_thread(_sync_list)

            has_more_flag = (self.offset + len(records_list)) < total_count

            print(f"[Section List] ✓ Found {len(records_list)} records (total: {total_count})")
            print(f"[Section List] Has more: {has_more_flag}")

            self.total = total_count
            self.has_more = has_more_flag
            self.count = len(records_list)

            # Take success path
            self.true_path = records_list

        except Exception as e:
            print(f"[Section List] ✗ Error: {str(e)}")
            self.total = 0
            self.has_more = False
            self.count = 0
            self.false_path = NodeError.format(e)
