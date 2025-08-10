# Variable List

Stores and manages list/array values with append functionality.

## Inputs

- **Value** (required): List/array to store and manage
- **Append** (optional): Item to append to the list

## Flow Control

- **True Path**: Always triggered. Contains the resulting list.

## Behavior

- Stores and manages list/array data structures
- Supports appending new items to existing lists
- Can append any data type (strings, numbers, objects, nested lists)
- If append value is provided, it gets added to the end of the list
- Returns the complete list including any appended items
- Handles empty lists and null append values gracefully

## Example Usage

```
Value: [1, 2, 3]
Append: 4
Result: [1, 2, 3, 4]
```

```
Value: ["apple", "banana"]
Append: "cherry"
Result: ["apple", "banana", "cherry"]
```

```
Value: [1, 2, 3]
Append: [4, 5]
Result: [1, 2, 3, [4, 5]]
```

```
Value: []
Append: "first item"
Result: ["first item"]
```

```
Value: [1, 2, 3]
Append: null
Result: [1, 2, 3]
```