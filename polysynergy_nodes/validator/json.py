import json
from pydantic import ValidationError

from polysynergy_node_runner.setup_context.dock_property import dock_json
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.validator.utils.generate_pydantic_model import generate_pydantic_model


@node(
    name="JSON Validator",
    category="validation"
)
class Json(Node):
    schema: str = NodeVariableSettings(label="JSON Schema", dock=dock_json(), has_in=True, required=True)
    input_json: str = NodeVariableSettings(label="JSON Input", dock=dock_json(), has_in=True)
    input_json_as_bytes: bytes = NodeVariableSettings(label="Input JSON as Bytes", has_in=True)
    validation_result: str = NodeVariableSettings(label="Validation Result", dock=True, has_out=True)
    output_json: str = NodeVariableSettings(label="Output JSON", has_out=True)
    output_json_as_dict: dict = NodeVariableSettings(label="Output JSON as Dict", has_out=True)

    true_path: bool = False
    false_path: bool = False

    def execute(self):
        try:
            try:
                if not self.schema or not self.schema.strip():
                    raise ValueError("Schema is empty")
                schema_dict = json.loads(self.schema)
            except (json.JSONDecodeError, ValueError) as e:
                self.validation_result = f"Schema is invalid JSON: {str(e)}"
                self.false_path = True
                return

            try:
                if isinstance(self.input_json_as_bytes, bytes):
                    input_str = self.input_json_as_bytes.decode("utf-8").strip()
                elif isinstance(self.input_json_as_bytes, str):
                    input_str = self.input_json_as_bytes.strip()
                elif self.input_json:
                    input_str = self.input_json.strip()
                else:
                    input_str = ""

                if not input_str:
                    raise ValueError("Input is empty")

                input_data = json.loads(input_str)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as e:
                self.validation_result = f"Input is invalid JSON: {str(e)}"
                self.false_path = True
                return

            dynamic_model = generate_pydantic_model(schema_dict)
            validated_data = dynamic_model(**input_data)

            self.validation_result = "Valid JSON"
            self.output_json = validated_data.model_dump_json(indent=2)
            self.output_json_as_dict = validated_data.model_dump()
            self.true_path = True

        except ValidationError as e:
            self.validation_result = f"Validation Error: {str(e)}"
            self.false_path = True
        except Exception as e:
            self.validation_result = f"Error: {str(e)}"
            self.false_path = True