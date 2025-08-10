# Boolean XOR

Performs a logical XOR (exclusive OR) operation on two input values with intelligent type coercion.

## Inputs

- **A** (required): First boolean value or value to convert to boolean
- **B** (required): Second boolean value or value to convert to boolean

## Flow Control

- **True Path**: Triggered when exactly one of A or B is truthy (but not both). Contains boolean true.
- **False Path**: Triggered when both values have the same truthiness, or on error. Contains boolean false or error message.

## Behavior

- Performs intelligent type coercion following common conventions:
  - Strings: Empty string, "false", "0", "null", "none", "undefined" are falsy
  - Numbers: Zero is falsy, all other numbers are truthy
  - Collections: Empty collections are falsy, non-empty are truthy
  - null/None values are falsy
- Returns true only when inputs have different truth values
- Useful for detecting differences or toggles
- Compatible with all data types through automatic conversion

## Example Usage

```
A: true, B: false
Result: true (different values)
```

```
A: false, B: true
Result: true (different values)
```

```
A: true, B: true
Result: false (same values)
```

```
A: false, B: false
Result: false (same values)
```

```
A: "hello", B: 0
Result: true (truthy vs falsy)
```