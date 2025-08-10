# Boolean NOT

Performs a logical NOT operation on an input value with intelligent type coercion.

## Inputs

- **A** (required): Boolean value or value to convert to boolean and negate

## Flow Control

- **True Path**: Triggered when A is falsy. Contains boolean true.
- **False Path**: Triggered when A is truthy, or on error. Contains boolean false or error message.

## Behavior

- Performs intelligent type coercion following common conventions:
  - Strings: Empty string, "false", "0", "null", "none", "undefined" are falsy
  - Numbers: Zero is falsy, all other numbers are truthy
  - Collections: Empty collections are falsy, non-empty are truthy
  - null/None values are falsy
- Returns the logical opposite of the input value
- Compatible with all data types through automatic conversion

## Example Usage

```
A: true
Result: false
```

```
A: false
Result: true
```

```
A: ""
Result: true (empty string is falsy, so NOT gives true)
```

```
A: "hello"
Result: false (non-empty string is truthy, so NOT gives false)
```

```
A: 0
Result: true (zero is falsy)
```