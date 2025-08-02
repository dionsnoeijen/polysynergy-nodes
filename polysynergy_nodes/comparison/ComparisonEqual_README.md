# Comparison Equal

Compares two values for equality and returns true if they are equal, false otherwise.

## Inputs

- **Value A** (required): First value to compare
- **Value B** (required): Second value to compare

## Outputs

- **Result**: Boolean value indicating whether the values are equal

## Behavior

- Performs intelligent type coercion (e.g., "5" equals 5)
- Handles various data types: strings, numbers, booleans, lists, dictionaries
- Returns false if values cannot be compared

## Example Usage

```
Value A: "hello"
Value B: "hello"
Result: true
```

```
Value A: 5
Value B: "5"
Result: true
```

```
Value A: [1, 2, 3]
Value B: [1, 2, 3]
Result: true
```