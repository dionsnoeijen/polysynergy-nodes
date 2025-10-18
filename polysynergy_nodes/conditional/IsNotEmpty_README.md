# Is Not Empty

Checks if a value is not empty, similar to PHP's `!empty()` function.

## Inputs

- **Value** (required): The value to check for emptiness (any type)

## Flow Control

- **True Path (Value)**: Triggered when the value is **not empty**. Passes through the original value.
- **False Path (Is Empty)**: Triggered when the value **is empty**. Contains the message "Value is empty".

## Behavior

A value is considered **empty** if it is:
- `null` / `None`
- `false`
- `0` (number zero)
- `"0"` (string zero)
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dictionary)

All other values are considered **not empty**.

## Example Usage

### Example 1: Non-empty string
```
Value: "hello"
Result: True Path triggered with "hello"
```

### Example 2: Empty string
```
Value: ""
Result: False Path triggered with "Value is empty"
```

### Example 3: Number zero
```
Value: 0
Result: False Path triggered with "Value is empty"
```

### Example 4: Non-empty list
```
Value: [1, 2, 3]
Result: True Path triggered with [1, 2, 3]
```

### Example 5: Empty list
```
Value: []
Result: False Path triggered with "Value is empty"
```

### Example 6: Null/None
```
Value: null
Result: False Path triggered with "Value is empty"
```

## Use Cases

- **Data validation**: Check if required fields have values before processing
- **Conditional flows**: Only proceed if data exists
- **API response validation**: Verify that responses contain data
- **Form input validation**: Ensure users provided input
- **Database query results**: Check if queries returned data

## Pattern: Exit on Empty

Common pattern to stop flow execution when data is missing:

```
[Data Source] → [Is Not Empty] --false_path--> [Exit Flow: "No data found"]
                                --true_path---> [Process Data]
```
