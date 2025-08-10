# Variable Float

Stores and outputs floating-point values.

## Inputs

- **Value** (required): Float value to store

## Outputs

- **Value**: The stored float value

## Behavior

- Simple passthrough node for floating-point values
- Stores any float value (positive, negative, or zero)
- Preserves precision of decimal values
- Returns the exact value provided
- Suitable for mathematical operations and decimal calculations

## Example Usage

```
Value: 3.14159
Result: 3.14159
```

```
Value: -2.5
Result: -2.5
```

```
Value: 0.0
Result: 0.0
```

```
Value: 123456.789
Result: 123456.789
```