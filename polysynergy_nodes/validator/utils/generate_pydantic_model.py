from typing import Any, Dict, List, Type, Optional
from pydantic import BaseModel, Field, create_model

def generate_pydantic_model(schema_json: Dict[str, Any]) -> Type[BaseModel]:
    def parse_fields(fields_data: Dict[str, Any]) -> Dict[str, Any]:
        parsed_fields = {}

        for field_name, field_props in fields_data.items():
            field_type = field_props["type"]

            type_mapping = {"int": int, "str": str, "list": List[Any], "dict": Dict[str, Any]}
            python_type = type_mapping.get(field_type, str)

            field_args = {}
            if "min" in field_props:
                field_args["gt"] = field_props["min"]
            if "min_length" in field_props:
                field_args["min_length"] = field_props["min_length"]
            if "max_length" in field_props:
                field_args["max_length"] = field_props["max_length"]
            if "regex" in field_props:
                field_args["regex"] = field_props["regex"]
            if "choices" in field_props:
                field_args["description"] = f"Allowed values: {', '.join(field_props['choices'])}"

            default_value = field_props.get("default", ...)
            required = field_props.get("required", False)

            if "fields" in field_props:
                sub_model = create_model(f"{field_name.capitalize()}Model", **parse_fields(field_props["fields"]))
                parsed_fields[field_name] = (Optional[sub_model] if not required else sub_model, Field(default_value))
            else:
                parsed_fields[field_name] = (Optional[python_type] if not required else python_type, Field(default_value, **field_args))

        return parsed_fields

    return create_model("DynamicSchema", **parse_fields(schema_json["fields"]))