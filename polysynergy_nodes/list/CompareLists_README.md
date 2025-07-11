# Compare Lists

Compares two lists and provides a selectable output:

## Node Details

- **Name:** Compare Lists
- **Category:** list
- **Type:** util

## Inputs

- `list_a` (List): The first list to compare.
- `list_b` (List): The second list to compare.
- `mode` (String): The comparison mode to apply.
  - Options:
    - `only_in_a`: Elements only in list A
    - `only_in_b`: Elements only in list B
    - `intersection`: Elements in both A and B
    - `symmetric_difference`: Elements in A or B but not both

## Outputs

- `true_path` (List): The result of the comparison, depending on selected mode.

## Path Behavior

- `true_path`: Triggered with the resulting list as output.
- `false_path`: Triggered when comparison fails due to missing or invalid input.

## Example

```python
list_a = ["apple", "banana", "cherry"]
list_b = ["banana", "dragonfruit"]

mode = "only_in_a"
# Output: ["apple", "cherry"]
```

## Notes

This node performs a basic set comparison. Elements are compared using Python’s native equality logic. Nested or complex structures may not behave as expected without normalization.

## Status

✅ Stable and ready for use.
