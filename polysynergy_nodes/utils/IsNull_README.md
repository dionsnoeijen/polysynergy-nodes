# Is Null

Checks if a value is null, empty, or undefined using comprehensive null-checking logic.

## Inputs

- **Value** (required): Value to check for null/empty status

## Outputs

- **Is Null**: Boolean indicating if the value is considered null/empty

## Flow Control

- **True Path**: Always triggered. Contains boolean result of null check.
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Comprehensive null/empty checking:
  - None/null values: Considered null
  - Empty strings: "" or whitespace-only strings
  - Empty collections: [], {}, (), set()
  - String literals: "null", "none", "undefined" (case-insensitive)
- Returns false for:
  - Non-empty strings, lists, dictionaries
  - Number 0 (zero is a valid value, not null)
  - Boolean false (false is a valid value, not null)
- Useful for validation and conditional logic
- Provides consistent null-checking across all data types

## Example Usage

```
Value: null
Result: true
```

```
Value: ""
Result: true
```

```
Value: []
Result: true
```

```
Value: "null"
Result: true
```

```
Value: 0
Result: false (zero is not null)
```

```
Value: false
Result: false (false is not null)
```

```
Value: "hello"
Result: false
```