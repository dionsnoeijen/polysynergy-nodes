# Boolean AND

Performs a logical AND operation on two input values with intelligent type coercion.

## Inputs

- **A** (required): First boolean value or value to convert to boolean
- **B** (required): Second boolean value or value to convert to boolean

## Flow Control

- **True Path**: Triggered when both A and B are truthy. Contains boolean true.
- **False Path**: Triggered when either A or B is falsy, or on error. Contains boolean false or error message.

## Behavior

- Performs intelligent type coercion following common conventions:
  - Strings: Empty string, "false", "0", "null", "none", "undefined" are falsy
  - Numbers: Zero is falsy, all other numbers are truthy
  - Collections: Empty collections are falsy, non-empty are truthy
  - null/None values are falsy
- Returns true only when both inputs are truthy
- Compatible with all data types through automatic conversion

## Example Usage

```
A: true, B: true
Result: true
```

```
A: true, B: false
Result: false
```

```
A: "hello", B: 1
Result: true (both are truthy)
```

```
A: "", B: "world"
Result: false (empty string is falsy)
```