# Comparison Smaller Than

Compares two values and returns true if the first value is smaller than the second.

## Inputs

- **Value A** (required): First value to compare
- **Value B** (required): Second value to compare

## Flow Control

- **True Path**: Triggered when Value A is smaller than Value B. Contains the original value from input A.
- **False Path**: Triggered when Value A is not smaller than Value B. Contains the original value from input B.

## Behavior

- Attempts to convert values to numbers for comparison
- Supports string-to-number conversion (e.g., "5" < "10")
- Falls back to string comparison if numeric conversion fails
- Returns false if comparison cannot be performed

## Example Usage

```
Value A: 5
Value B: 10
Result: true
```

```
Value A: "20"
Value B: "100"
Result: true (numeric comparison)
```

```
Value A: "a"
Value B: "b"
Result: true (alphabetical comparison)
```