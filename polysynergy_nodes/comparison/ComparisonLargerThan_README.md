# Comparison Larger Than

Compares two values and returns true if the first value is larger than the second.

## Inputs

- **Value A** (required): First value to compare
- **Value B** (required): Second value to compare

## Outputs

- **Result**: Boolean value indicating whether Value A is larger than Value B

## Behavior

- Attempts to convert values to numbers for comparison
- Supports string-to-number conversion (e.g., "10" > "5")
- Falls back to string comparison if numeric conversion fails
- Returns false if comparison cannot be performed

## Example Usage

```
Value A: 10
Value B: 5
Result: true
```

```
Value A: "100"
Value B: "20"
Result: true (numeric comparison)
```

```
Value A: "b"
Value B: "a"
Result: true (alphabetical comparison)
```