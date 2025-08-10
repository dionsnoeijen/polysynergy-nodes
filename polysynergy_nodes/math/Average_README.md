# Average

Calculates the average (mean), sum, and count of a collection of numbers.

## Inputs

- **Values** (required): List of numbers or comma-separated string of numbers

## Outputs

- **Average**: The mean of all numbers
- **Sum**: The total of all numbers
- **Count**: The number of valid numbers processed

## Flow Control

- **True Path**: Triggered on successful calculation. Contains the calculated average.
- **False Path**: Triggered when no valid numbers are found. Contains error information.

## Behavior

- Accepts input as list of numbers or comma-separated string
- Automatically converts string numbers to integers or floats
- Ignores non-numeric values in the collection
- Supports both integers and floating-point numbers
- Provides comprehensive statistics: average, sum, and count
- Returns error if no valid numbers are provided
- Handles mixed integer and float values correctly

## Example Usage

```
Values: [1, 2, 3, 4, 5]
Average: 3.0, Sum: 15, Count: 5
```

```
Values: "10, 20, 30"
Average: 20.0, Sum: 60, Count: 3
```

```
Values: [2.5, 3.5, 4.0]
Average: 3.33, Sum: 10.0, Count: 3
```

```
Values: "1, invalid, 3, text, 5"
Average: 3.0, Sum: 9, Count: 3 (ignores non-numeric values)
```