# Variable Dict

Stores and processes dictionary values with JSON serialization and placeholder replacement support.

## Inputs

- **Value** (required): Dictionary object to store and process

## Outputs

- **Value as Json String**: Dictionary serialized as JSON string

## Flow Control

- **True Path**: Triggered on successful processing. Contains the processed dictionary.
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Stores dictionary values and converts them to JSON strings
- Supports placeholder replacement using Jinja2 syntax ({{ variable }})
- Handles nested dictionaries and various data types
- Returns both the dictionary object and its JSON string representation
- Provides detailed error information for debugging

## Example Usage

```
Value: {"name": "John", "age": 30}
Result: {"name": "John", "age": 30}
JSON String: '{"name": "John", "age": 30}'
```

```
Value: {"message": "Hello {{ name }}", "count": 5}
Placeholders: {"name": "World"}
Result: {"message": "Hello World", "count": 5}
```

```
Value: {"nested": {"items": [1, 2, 3]}}
Result: {"nested": {"items": [1, 2, 3]}}
```