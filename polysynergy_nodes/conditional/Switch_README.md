# Switch

Multi-case conditional node that matches a value against multiple cases and returns corresponding results.

## Inputs

- **Value** (required): Value to match against cases
- **Case 1** (optional): First case to match against
- **Result 1** (optional): Result to return if Case 1 matches
- **Case 2** (optional): Second case to match against  
- **Result 2** (optional): Result to return if Case 2 matches
- **Case 3** (optional): Third case to match against
- **Result 3** (optional): Result to return if Case 3 matches
- **Default** (optional): Default result if no cases match

## Flow Control

- **True Path**: Always triggered. Contains the matched result or default value.
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Compares input value against cases using exact equality (==)
- Checks cases in order (Case 1, Case 2, Case 3)
- Returns the corresponding result for the first matching case
- Returns default value if no cases match
- Supports any data type for values, cases, and results
- Cases can be null/empty to skip comparison

## Example Usage

```
Value: "A", Case1: "A", Result1: "Apple", Default: "Unknown"
Result: "Apple"
```

```
Value: 2, Case1: 1, Result1: "One", Case2: 2, Result2: "Two", Default: "Other"
Result: "Two"
```

```
Value: "X", Case1: "A", Result1: "Apple", Case2: "B", Result2: "Banana", Default: "Unknown"
Result: "Unknown"
```

```
Value: true, Case1: true, Result1: "Yes", Case2: false, Result2: "No"
Result: "Yes"
```