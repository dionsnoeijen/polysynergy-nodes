# If Then Else

Simple conditional node that selects between two values based on a condition.

## Inputs

- **Condition** (required): Boolean value or value to convert to boolean for decision
- **Then Value** (required): Value to return if condition is truthy
- **Else Value** (required): Value to return if condition is falsy

## Flow Control

- **True Path**: Always triggered. Contains the selected value (Then or Else).
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Evaluates the condition using intelligent type coercion:
  - Strings: Empty string, "false", "0", "null", "none", "undefined" are falsy
  - Numbers: Zero is falsy, all other numbers are truthy
  - Collections: Empty collections are falsy, non-empty are truthy
  - null/None values are falsy
- Returns Then Value if condition is truthy
- Returns Else Value if condition is falsy
- Passes through values of any type without modification
- Simple alternative to complex conditional logic

## Example Usage

```
Condition: true, Then: "Yes", Else: "No"
Result: "Yes"
```

```
Condition: false, Then: 100, Else: 200
Result: 200
```

```
Condition: "hello", Then: [1,2,3], Else: []
Result: [1,2,3] (non-empty string is truthy)
```

```
Condition: 0, Then: "positive", Else: "zero or negative"
Result: "zero or negative" (zero is falsy)
```