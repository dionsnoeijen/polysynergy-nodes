import json
from typing import Any, List
from pydantic import BaseModel, create_model

from polysynergy_node_runner.setup_context.dock_property import dock_json
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.service_node import ServiceNode


@node(
    name="JSON Example to Model",
    category="pydantic",
    has_enabled_switch=False,
)
class JsonExampleToModel(ServiceNode):
    """
    Converts a JSON example into a Pydantic BaseModel.

    This node dynamically creates a Pydantic model by inferring types from
    an example JSON structure. Supports nested objects, arrays, and all
    standard JSON types.

    Use cases:
    - Creating response models for Agno agents
    - Validating API responses
    - Normalizing data structures
    - Schema generation from examples
    """

    example_json: str | dict | list = NodeVariableSettings(
        label="Example JSON",
        dock=dock_json(),
        has_in=True,
        info="Make an example JSON object. The structure and types will be inferred to create a Pydantic model."
    )

    model_name: str = NodeVariableSettings(
        label="Model Name",
        dock=True,
        has_in=True,
        default="DynamicModel",
        info="Name for the generated Pydantic model (default: DynamicModel)"
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
        info="The generated Pydantic BaseModel that can be used for validation and parsing"
    )

    def _infer_field_type(self, value: Any, field_name: str = "Item") -> tuple:
        """
        Recursively infer types from a value, including nested structures.

        Returns:
            tuple: (type, default_value) for use with create_model
        """
        required_marker = ... if not self.make_optional else None

        if value is None:
            return (Any, None)

        elif isinstance(value, bool):
            return (bool, required_marker)

        elif isinstance(value, int):
            return (int, required_marker)

        elif isinstance(value, float):
            return (float, required_marker)

        elif isinstance(value, str):
            return (str, required_marker)

        elif isinstance(value, list):
            if not value:
                # Empty list - create a minimal placeholder model for OpenAI compatibility
                # This ensures the schema has proper type information even for empty arrays
                placeholder_model = create_model(
                    f"{field_name}Item",
                    __module__=__name__,
                    # Empty model with no fields - will accept any object structure
                )
                return (List[placeholder_model], [] if not self.make_optional else None)

            first_item = value[0]

            if isinstance(first_item, dict):
                # Create nested model for list items
                nested_model = self._json_to_model(
                    first_item,
                    model_name=f"{field_name}Item"
                )
                return (List[nested_model], required_marker)
            else:
                # Simple list of primitives
                item_type = type(first_item)
                return (List[item_type], required_marker)

        elif isinstance(value, dict):
            # Nested object - create sub-model
            nested_model = self._json_to_model(
                value,
                model_name=f"{field_name}Model"
            )
            return (nested_model, required_marker)

        else:
            # Fallback for unknown types
            return (Any, required_marker)

    def _json_to_model(self, data: dict, model_name: str) -> type[BaseModel]:
        """
        Convert a dictionary to a Pydantic model by inferring field types.

        Args:
            data: Dictionary with example data
            model_name: Name for the generated model

        Returns:
            A Pydantic BaseModel class
        """
        fields = {}

        for key, value in data.items():
            # Create readable name for nested models
            field_display_name = key.replace('_', ' ').title().replace(' ', '')
            fields[key] = self._infer_field_type(value, field_display_name)

        # Create model with explicit __module__ to avoid KeyError
        return create_model(
            model_name,
            __module__=__name__,  # Provide module context for Pydantic
            **fields
        )

    async def provide_instance(self) -> type[BaseModel]:
        """
        Parse the example JSON and generate a Pydantic model.

        Returns:
            The generated Pydantic BaseModel class
        """
        if not self.example_json:
            raise ValueError("example_json is required")

        # Parse JSON string to dict
        try:
            if isinstance(self.example_json, str):
                data = json.loads(self.example_json)
            else:
                data = self.example_json
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        if not isinstance(data, dict):
            raise ValueError("example_json must be a JSON object (dict), not an array or primitive")

        # Generate the model
        model_name = self.model_name or "DynamicModel"
        generated_model = self._json_to_model(data, model_name)

        # Store it for output
        self.model = generated_model

        print(f"DEBUG JsonExampleToModel: Generated model = {generated_model}")
        print(f"DEBUG JsonExampleToModel: Model name = {model_name}")
        print(f"DEBUG JsonExampleToModel: Stored in self.model = {self.model}")

        return generated_model