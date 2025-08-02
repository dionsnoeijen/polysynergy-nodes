# Comparison Not Equal

Compares two values for inequality and returns true if they are different, false if they are equal.

## Inputs

- **Value A** (required): First value to compare
- **Value B** (required): Second value to compare

## Outputs

- **Result**: Boolean value indicating whether the values are not equal

## Behavior

- Performs intelligent type coercion (e.g., "5" equals 5, so they are not "not equal")
- Handles various data types: strings, numbers, booleans, lists, dictionaries
- Returns true if values cannot be compared or are different

## Example Usage

```
Value A: "hello"
Value B: "world"
Result: true
```

```
Value A: 5
Value B: "5"
Result: false (they are equal after type coercion)
```

```
Value A: [1, 2, 3]
Value B: [1, 2, 4]
Result: true
```