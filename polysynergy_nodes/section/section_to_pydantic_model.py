import asyncio
from uuid import UUID
from typing import Optional, Any
from pydantic import BaseModel, create_model, Field

from polysynergy_node_runner.setup_context.dock_property import dock_property
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.service_node import ServiceNode

from polysynergy_nodes.section.repositories.db_session import get_main_db_session
from polysynergy_nodes.section.repositories.node_section_repository import NodeSectionRepository


# Field type mapping from section field types to Python types
FIELD_TYPE_MAP = {
    'text': str,
    'email': str,
    'url': str,
    'textarea': str,
    'number': float,  # Can handle both int and float
    'boolean': bool,
    'json': dict,  # OpenAI doesn't support plain dict - will be converted to Any
    'date': str,  # ISO 8601 format
    'datetime': str,  # ISO 8601 format
    'select': str,
    'multiselect': list,  # OpenAI doesn't support plain list - will be converted to list[Any]
}


@node(
    name="Section to Pydantic Model",
    category="section",
    icon='database.svg',
    version=1.0,
    has_enabled_switch=False,
)
class SectionToPydanticModel(ServiceNode):
    """
    Generates a Pydantic model from a Section definition.

    This node reads a section's field configuration and automatically
    creates a Pydantic BaseModel that matches the section structure.

    Perfect for:
    - Providing structured output schemas to AI agents
    - Validating data before inserting into sections
    - Generating type-safe interfaces for section data

    The generated model can be used directly with Agno agents as response_model.
    """

    section_id: str = NodeVariableSettings(
        label="Section",
        dock=dock_property(
            metadata={"source": "portal_sections"},
            placeholder="Select a section"
        ),
        has_in=True,
        info="The section to generate a Pydantic model for"
    )

    model_name: str = NodeVariableSettings(
        label="Model Name",
        dock=True,
        has_in=True,
        default="",
        info="Optional custom model name. If empty, uses section handle in PascalCase (e.g., 'CompanyResearch')"
    )

    make_optional: bool = NodeVariableSettings(
        label="Make All Fields Optional",
        dock=True,
        has_in=True,
        default=False,
        info="If True, all fields will be optional (can be None). If False, fields are required."
    )

    model: BaseModel | None = NodeVariableSettings(
        label="Model",
        has_out=True,
        info="The generated Pydantic BaseModel - use this as response_model for Agno agents"
    )

    def _to_pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase (e.g., 'company_research' -> 'CompanyResearch')"""
        return ''.join(word.capitalize() for word in snake_str.split('_'))

    def _get_python_type(self, field_type: str, field_settings: dict) -> tuple:
        """
        Map a section field type to a Python type for Pydantic.

        Args:
            field_type: The field type handle (e.g., 'text', 'number', 'json')
            field_settings: Additional settings for the field

        Returns:
            tuple: (type, Field(...)) for use with create_model
        """
        # Get base Python type
        python_type = FIELD_TYPE_MAP.get(field_type, str)  # Default to str if unknown

        # IMPORTANT: OpenAI structured outputs doesn't accept dict, list, or Any
        # For JSON fields, use str and let the agent return JSON as a string
        # The section repository will handle JSON parsing when storing
        if python_type == dict:
            python_type = str  # JSON objects as strings
        elif python_type == list:
            python_type = str  # JSON arrays as strings

        # For OpenAI structured outputs, we need all fields to be required OR all optional
        # Using Field(...) makes it required, Field(default=None) makes it optional
        if self.make_optional:
            # Make optional with None default
            return (Optional[python_type], Field(default=None))
        else:
            # Make required (no default)
            return (python_type, Field(...))

    def _create_model_from_section(self, section_info: dict) -> type[BaseModel]:
        """
        Create a Pydantic model from section field assignments.

        Args:
            section_info: Dictionary with section information including field_assignments

        Returns:
            A Pydantic BaseModel class
        """
        fields = {}
        field_assignments = section_info.get("field_assignments", [])

        print(f"\n[Section to Pydantic] ========== Generating Model ==========")
        print(f"[Section to Pydantic] Section: {section_info.get('label')}")
        print(f"[Section to Pydantic] Fields: {len(field_assignments)}")

        for assignment in field_assignments:
            field_handle = assignment["handle"]
            field_type = assignment["field_type_handle"]
            field_settings = assignment.get("field_settings", {})

            # Get Python type for this field
            python_type_info = self._get_python_type(field_type, field_settings)
            fields[field_handle] = python_type_info

            print(f"[Section to Pydantic]   - {field_handle}: {field_type} -> {python_type_info[0].__name__}")

        # Generate model name
        if self.model_name:
            model_name = self.model_name
        else:
            # Use section handle converted to PascalCase
            model_name = self._to_pascal_case(section_info.get("handle", "DynamicModel"))

        print(f"[Section to Pydantic] Model name: {model_name}")

        # Create the Pydantic model
        generated_model = create_model(
            model_name,
            __module__=__name__,
            **fields
        )

        print(f"[Section to Pydantic] ✓ Model generated successfully")

        # DEBUG: Print the JSON schema that will be sent to OpenAI
        try:
            schema = generated_model.model_json_schema()
            print(f"[Section to Pydantic] Generated JSON Schema:")
            print(f"  Properties: {list(schema.get('properties', {}).keys())}")
            print(f"  Required: {schema.get('required', [])}")
        except Exception as e:
            print(f"[Section to Pydantic] Warning: Could not print schema: {e}")

        return generated_model

    async def provide_instance(self) -> type[BaseModel]:
        """
        Generate a Pydantic model from the section definition.

        Returns:
            The generated Pydantic BaseModel class
        """
        print(f"\n[Section to Pydantic] ========== Starting ==========")
        print(f"[Section to Pydantic] Section ID: {self.section_id}")

        # Validate input
        if not self.section_id:
            raise ValueError("Section ID is required")

        # Convert to UUID
        try:
            section_uuid = UUID(self.section_id)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid section ID format: {str(e)}")

        # Execute in thread (repository uses sync SQLAlchemy)
        def _sync_get_section():
            with get_main_db_session() as db:
                section_repo = NodeSectionRepository(db)
                return section_repo.get_by_id(section_uuid)

        # Get section info
        section_info = await asyncio.to_thread(_sync_get_section)

        # Generate Pydantic model
        generated_model = self._create_model_from_section(section_info)

        # Store for output
        self.model = generated_model

        print(f"[Section to Pydantic] ✓ Generated model: {generated_model.__name__}")
        print(f"[Section to Pydantic] ✓ Field count: {len(section_info.get('field_assignments', []))}")

        return generated_model
