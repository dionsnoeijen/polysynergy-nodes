# Boolean OR

Performs a logical OR operation on two input values with intelligent type coercion.

## Inputs

- **A** (required): First boolean value or value to convert to boolean
- **B** (required): Second boolean value or value to convert to boolean

## Flow Control

- **True Path**: Triggered when either A or B (or both) is truthy. Contains boolean true.
- **False Path**: Triggered when both A and B are falsy, or on error. Contains boolean false or error message.

## Behavior

- Performs intelligent type coercion following common conventions:
  - Strings: Empty string, "false", "0", "null", "none", "undefined" are falsy
  - Numbers: Zero is falsy, all other numbers are truthy
  - Collections: Empty collections are falsy, non-empty are truthy
  - null/None values are falsy
- Returns true when at least one input is truthy
- Compatible with all data types through automatic conversion

## Example Usage

```
A: true, B: false
Result: true
```

```
A: false, B: false
Result: false
```

```
A: "", B: "hello"
Result: true (second value is truthy)
```

```
A: 0, B: []
Result: false (both are falsy)
```