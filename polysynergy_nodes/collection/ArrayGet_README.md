# Array Get

Retrieves an item from an array/list by its index position.

## Inputs

- **Array** (required): List/array to get item from
- **Index** (required): Zero-based index of the item to retrieve

## Outputs

- **Item**: The item at the specified index

## Flow Control

- **True Path**: Triggered when item is successfully retrieved. Contains the item value.
- **False Path**: Triggered when index is out of bounds or input is invalid. Contains error information.

## Behavior

- Uses zero-based indexing (first item is index 0)
- Supports negative indexing (-1 is last item, -2 is second-to-last, etc.)
- Automatically converts string indices to integers when possible
- Returns error for out-of-bounds access
- Validates that input is actually a list/array
- Preserves original data types of retrieved items
- Works with arrays containing any data types

## Example Usage

```
Array: ['a', 'b', 'c'], Index: 1
Result: 'b'
```

```
Array: [10, 20, 30], Index: -1
Result: 30 (last item)
```

```
Array: [1, "hello", {"key": "value"}], Index: 2
Result: {"key": "value"}
```

```
Array: [1, 2, 3], Index: 5
Result: Error - Index out of range
```