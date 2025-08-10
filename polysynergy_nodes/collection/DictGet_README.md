# Dict Get

Retrieves a value from a dictionary/object by its key, with optional default value.

## Inputs

- **Dictionary** (required): Dictionary/object to get value from
- **Key** (required): Key to look up in the dictionary
- **Default** (optional): Default value to return if key is not found

## Outputs

- **Value**: The value for the specified key, or default if key not found

## Flow Control

- **True Path**: Triggered when lookup is successful. Contains the retrieved value (or default).
- **False Path**: Triggered when input is not a dictionary. Contains error information.

## Behavior

- Looks up values in dictionary using exact key matching
- Returns the default value if key is not found (graceful fallback)
- Automatically converts non-string keys to strings when needed
- Validates that input is actually a dictionary
- Preserves original data types of retrieved values
- Handles null/None values in dictionary correctly
- Returns null/None as valid values (not defaults)

## Example Usage

```
Dictionary: {"name": "John", "age": 30}, Key: "name", Default: "Unknown"
Result: "John"
```

```
Dictionary: {"a": 1, "b": 2}, Key: "c", Default: "Not Found"
Result: "Not Found"
```

```
Dictionary: {"value": null}, Key: "value", Default: "Default"
Result: null (returns actual null value, not default)
```

```
Dictionary: {}, Key: "anything", Default: "Empty"
Result: "Empty"
```