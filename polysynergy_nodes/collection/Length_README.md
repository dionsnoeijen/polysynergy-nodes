# Length

Gets the length/count of items in any collection or string.

## Inputs

- **Value** (required): Collection or string to measure (list, dict, string, tuple, set, etc.)

## Outputs

- **Length**: The number of items/characters in the collection

## Flow Control

- **True Path**: Triggered on successful measurement. Contains the length value.
- **False Path**: Triggered when value doesn't have a measurable length. Contains error information.

## Behavior

- Supports various collection types:
  - Lists/Arrays: Number of elements
  - Strings: Number of characters
  - Dictionaries: Number of key-value pairs
  - Tuples: Number of elements
  - Sets: Number of unique elements
- Returns 0 for null/None values
- Works with empty collections (returns 0)
- Returns error for non-iterable types that don't have length
- Universal length measurement across data types

## Example Usage

```
Value: [1, 2, 3, 4, 5]
Length: 5
```

```
Value: "Hello World"
Length: 11
```

```
Value: {"a": 1, "b": 2, "c": 3}
Length: 3
```

```
Value: []
Length: 0
```

```
Value: null
Length: 0
```

```
Value: 42
Result: Error - Cannot get length of integer
```