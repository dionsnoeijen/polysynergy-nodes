# JSON Validator

This node validates JSON input against a given JSON schema and returns the validation result.

## **Category:** Validation

## **Description**
The **JSON Validator** node checks whether a JSON object conforms to a specified JSON schema. If validation succeeds, the JSON is returned in a formatted structure. If validation fails, an error message is generated.

## **Variables**

| Name                | Type  | Input | Output | Description |
|---------------------|-------|-------|--------|-------------|
| `schema`           | str   | ✅     | ❌      | The JSON schema used for validation. |
| `input_json`       | str   | ✅     | ❌      | The JSON input to be validated. |
| `validation_result` | str   | ❌     | ✅      | The validation result ("Valid JSON" or an error message). |
| `output_json`      | str   | ❌     | ✅      | The validated JSON formatted as a string. |
| `output_json_as_dict` | dict  | ❌     | ✅      | The validated JSON as a dictionary. |

## **Flow Control**
This node has two logical outputs:
- **`true_path`** (bool) – triggered if the JSON is valid.
- **`false_path`** (bool) – triggered if the JSON is invalid.

## **How It Works**
1. The node receives a **JSON Schema** and a **JSON Input**.
2. Both the schema and input are parsed. If either is invalid JSON, an error message is returned.
3. A dynamic Pydantic model is generated based on the schema.
4. The JSON input is validated using the model.
5. If validation succeeds:
   - `validation_result` is set to `Valid JSON`.
   - `output_json` contains the formatted JSON string.
   - `output_json_as_dict` contains the validated JSON as a dictionary.
6. If validation fails:
   - `validation_result` contains error details about the validation failure.

## **Example**

### **JSON Schema** (input)
```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}
```

### **JSON Input** (valid)
```json
{
    "name": "John Doe",
    "age": 30
}
```

### **Result**
- **Validation successful:**
  - `validation_result` = "Valid JSON"
  - `output_json` contains the formatted JSON string.
  - `output_json_as_dict` contains the validated JSON as a dictionary.
- **Validation failed:**
  - `validation_result` contains details about the error.

## **Error Handling**
- Invalid JSON in `schema` or `input_json` will return an error message.
- If the input does not conform to the schema, a detailed validation error is displayed.

## **Usage**
This node is useful for API validation, data integration, or enforcing structured data in workflows.
