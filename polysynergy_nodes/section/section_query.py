import asyncio
from uuid import UUID

from polysynergy_node_runner.execution_context.replace_placeholders import replace_placeholders
from polysynergy_node_runner.setup_context.dock_property import dock_property, dock_text_area
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_error import NodeError
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings

from polysynergy_nodes.section.repositories.db_session import get_main_db_session
from polysynergy_nodes.section.repositories.node_section_repository import NodeSectionRepository
from polysynergy_nodes.section.repositories.node_content_repository import NodeContentRepository


@node(
    name="Section Query",
    category="section",
    icon='database.svg',
    version=1.0,
    stateful=False,  # Must be non-stateful to work correctly in loops
)
class SectionQuery(Node):
    """
    Query section records with custom WHERE conditions.

    This is like Section List, but you can specify custom SQL WHERE conditions
    instead of just using the search parameter.

    The node automatically builds: SELECT * FROM "schema"."table" WHERE {your_condition}

    Example WHERE conditions:
    - created_at > '2024-01-01'
    - status = 'active' AND price > 100
    - email LIKE '%@gmail.com'

    For simple listing/searching, use Section List instead.
    For complex JOINs or aggregations, use database nodes directly.

    WARNING: This node allows arbitrary WHERE clauses. Ensure input is trusted
    or properly validated to prevent SQL injection.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to query records from"
    )

    where_clause: str = NodeVariableSettings(
        label="WHERE Condition",
        dock=dock_text_area(),
        has_in=True,
        default="",
        info="SQL WHERE condition (without 'WHERE' keyword). Example: created_at > '2024-01-01' AND status = 'active'. Supports placeholders like {{variable_name}}"
    )

    values: dict[str, str] = NodeVariableSettings(
        label="Values",
        dock=True,
        has_in=True,
        default={},
        info="Dictionary of values for placeholder replacement in WHERE condition"
    )

    limit: int = NodeVariableSettings(
        label="Limit",
        dock=True,
        has_in=True,
        default=100,
        info="Maximum number of records to return"
    )

    offset: int = NodeVariableSettings(
        label="Offset",
        dock=True,
        has_in=True,
        default=0,
        info="Number of records to skip (for pagination)"
    )

    select: dict = NodeVariableSettings(
        label="Select Columns",
        dock=True,
        has_in=True,
        has_out=True,
        default={},
        info="Dict with column names as keys to select specific columns. Empty = all columns. After execute, contains values from first record."
    )

    count: int = NodeVariableSettings(
        label="Count",
        has_out=True,
        info="Number of records returned"
    )

    # Paths
    true_path: bool | list = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        try:
            print(f"\n[Section Query] ========== Executing Query with WHERE ==========")
            print(f"[Section Query] Instance ID: {id(self)} ({self.handle})")
            print(f"[Section Query] Section ID: {self.section_id}")
            print(f"[Section Query] WHERE: {self.where_clause}")
            print(f"[Section Query] Limit: {self.limit}, Offset: {self.offset}")

            # Validate inputs
            if not self.section_id:
                raise ValueError("Section ID is required")

            # Ensure values is a dict
            if not isinstance(self.values, dict):
                self.values = {}

            # Ensure select is a dict
            if not isinstance(self.select, dict):
                self.select = {}

            # Get select columns from select dict keys
            select_columns = list(self.select.keys()) if self.select else None
            if select_columns:
                print(f"[Section Query] SELECT columns: {select_columns}")

            # Replace placeholders in WHERE clause (use local variable to preserve original)
            where_clause_resolved = self.where_clause
            if where_clause_resolved:
                # First replace placeholders in values dict itself
                replaced_values = replace_placeholders(
                    data=self.values,
                    values=self.values,
                    state=self.state,
                    current_node=self
                )

                # Then replace placeholders in WHERE clause
                where_clause_resolved = replace_placeholders(
                    data=where_clause_resolved,
                    values=replaced_values,
                    state=self.state,
                    current_node=self
                )

                print(f"[Section Query] WHERE after placeholder replacement: {where_clause_resolved}")

            # Convert section_id to UUID
            try:
                section_uuid = UUID(self.section_id)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid section ID format: {self.section_id}")

            # Execute in thread (repositories use sync SQLAlchemy)
            def _sync_query():
                # Get section information
                with get_main_db_session() as db:
                    section_repo = NodeSectionRepository(db)
                    section_info = section_repo.get_by_id(section_uuid)

                print(f"[Section Query] Section: {section_info['label']}")
                print(f"[Section Query] Table: {section_info['schema_name']}.{section_info['table_name']}")

                # Execute custom query
                content_repo = NodeContentRepository(section_info)

                if where_clause_resolved:
                    # Execute with custom WHERE clause
                    records_list = content_repo.query_with_where(
                        where_clause=where_clause_resolved,
                        limit=self.limit,
                        offset=self.offset,
                        select_columns=select_columns
                    )
                else:
                    # No WHERE clause - just list all records
                    print(f"[Section Query] No WHERE clause - listing all records")
                    records_list = content_repo.get_all(
                        limit=self.limit,
                        offset=self.offset,
                        select_columns=select_columns
                    )

                return records_list

            # Run in thread pool to avoid blocking
            records_list = await asyncio.to_thread(_sync_query)

            print(f"[Section Query] ✓ Query executed successfully")
            print(f"[Section Query] Returned {len(records_list)} records")

            self.count = len(records_list)

            # Check if we have results
            if len(records_list) > 0:
                # Take success path with results
                self.true_path = records_list
                self.false_path = False

                # Populate select dict with values from first record
                if select_columns:
                    first_record = records_list[0]
                    for col in select_columns:
                        if col in first_record:
                            self.select[col] = first_record[col]
                    print(f"[Section Query] Select output: {self.select}")
            else:
                # No results found - take false path
                print(f"[Section Query] ⚠ No records found matching query")
                self.false_path = {
                    "error": "No records found",
                    "message": "The query executed successfully but returned no results",
                    "query": where_clause_resolved if where_clause_resolved else "No WHERE clause"
                }
                self.true_path = False

        except Exception as e:
            print(f"[Section Query] ✗ Error: {str(e)}")
            self.count = 0
            self.false_path = NodeError.format(e)
            self.true_path = False
