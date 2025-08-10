# Count

Counts the number of items in a collection (list, string, dictionary, etc.).

## Inputs

- **Values** (required): Collection to count items in (list, string, dict, etc.)

## Outputs

- **Count**: The number of items in the collection

## Flow Control

- **True Path**: Always triggered. Contains the count of items.
- **False Path**: Triggered on errors. Contains error information.

## Behavior

- Supports counting items in various collection types:
  - Lists: Number of elements
  - Strings: Number of characters
  - Dictionaries: Number of key-value pairs
  - Tuples: Number of elements
  - Sets: Number of unique elements
- Returns 0 for null/None values
- Returns 1 for non-iterable single values
- Provides universal counting functionality across data types

## Example Usage

```
Values: [1, 2, 3, 4, 5]
Count: 5
```

```
Values: "hello"
Count: 5
```

```
Values: {"a": 1, "b": 2, "c": 3}
Count: 3
```

```
Values: null
Count: 0
```

```
Values: (1, 2, 3, 4)
Count: 4
```