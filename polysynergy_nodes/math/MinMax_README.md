# Min Max

Finds the minimum and maximum values from a collection of numbers.

## Inputs

- **Values** (required): List of numbers or comma-separated string of numbers

## Outputs

- **Min Value**: The smallest number in the collection
- **Max Value**: The largest number in the collection

## Flow Control

- **True Path**: Triggered on successful calculation. Contains boolean true.
- **False Path**: Triggered when no valid numbers are found. Contains error information.

## Behavior

- Accepts input as list of numbers or comma-separated string
- Automatically converts string numbers to integers or floats
- Ignores non-numeric values in the collection
- Supports both integers and floating-point numbers
- Returns error if no valid numbers are provided
- Handles mixed integer and float values correctly

## Example Usage

```
Values: [1, 5, 3, 9, 2]
Min Value: 1, Max Value: 9
```

```
Values: "1.5, 3.2, 0.8, 4.7"
Min Value: 0.8, Max Value: 4.7
```

```
Values: [10, -5, 0, 15]
Min Value: -5, Max Value: 15
```

```
Values: "1, hello, 5, world, 3"
Min Value: 1, Max Value: 5 (ignores non-numeric values)
```