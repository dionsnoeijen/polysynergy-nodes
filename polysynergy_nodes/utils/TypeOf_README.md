# Type Of

Determines the data type of a value and returns a user-friendly type name.

## Inputs

- **Value** (required): Value to determine the type of

## Outputs

- **Type**: User-friendly string name of the value's type

## Flow Control

- **True Path**: Always triggered. Contains the type name as a string.
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Returns user-friendly type names:
  - `null` for None/null values
  - `string` for text values
  - `integer` for whole numbers
  - `float` for decimal numbers
  - `boolean` for true/false values
  - `array` for lists/arrays
  - `object` for dictionaries
  - `tuple` for tuple values
  - `set` for set values
- Uses consistent naming conventions across programming languages
- Useful for type validation and conditional logic
- Helps with debugging and data flow analysis

## Example Usage

```
Value: "hello world"
Type: "string"
```

```
Value: 42
Type: "integer"
```

```
Value: 3.14
Type: "float"
```

```
Value: [1, 2, 3]
Type: "array"
```

```
Value: {"key": "value"}
Type: "object"
```

```
Value: null
Type: "null"
```

```
Value: true
Type: "boolean"
```