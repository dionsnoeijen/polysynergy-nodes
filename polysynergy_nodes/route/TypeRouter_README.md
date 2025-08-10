# Type Router

Routes values based on their data type to different output paths.

## Description

The Type Router node analyzes the input value's data type and routes it to the corresponding type-specific output connection. This enables different processing flows based on whether the input is a string, number, boolean, array, object, or null value.

## Inputs

- **Value**: The value to analyze for type routing (required)

## Outputs

The node provides predefined output connections for each supported data type:

- **string**: Routes string values
- **number**: Routes numeric values (int or float)
- **boolean**: Routes boolean values (true/false)  
- **array**: Routes list/array values
- **object**: Routes dictionary/object values
- **null**: Routes null/None values
- **default**: Fallback route for unrecognized types

## Paths

- **No Match**: Triggered when no type matches and no default connection exists

## Behavior

1. Analyzes the input value's Python type
2. Maps Python types to user-friendly type names:
   - `str` → "string"
   - `int`, `float` → "number"
   - `bool` → "boolean"
   - `list` → "array"
   - `dict` → "object"
   - `None` → "null"
3. Routes to the matching type output or "default" if no specific type match
4. Kills all non-matching output connections
5. Passes the original input value through the selected route

## Example Use Cases

- **Data validation workflows**: Route different data types to appropriate validation logic
- **Format conversion**: Send strings to text processors, numbers to calculators, objects to JSON handlers
- **Type-specific processing**: Apply different transformations based on data type
- **Error handling**: Use default route for unexpected data types

## Type Detection

The node uses Python's built-in type checking:
- Strings, integers, floats, booleans, lists, and dictionaries are detected accurately
- Custom objects fall back to using their class name in lowercase
- None values are specifically handled as "null" type