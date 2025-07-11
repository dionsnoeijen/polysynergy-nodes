# Merge Lists Node

The **Merge Lists** node combines two lists into one.

## Inputs

- `list_a` (`list`, required): First list to merge.
- `list_b` (`list`, required): Second list to merge.

## Outputs

- `true_path` (`list`): Combined list from both inputs.
- `false_path` (`dict`): Error info if merging fails.

## Behavior

If both inputs are valid lists, the node will merge them using list concatenation (`list_a + list_b`).  
If either input is invalid, `false_path` is triggered with an error message.

## Example

### Input
```json
{
  "list_a": [1, 2, 3],
  "list_b": [4, 5]
}
```

### Output
```json
{
  "true_path": [1, 2, 3, 4, 5]
}
```

## Errors

- Input not being a list (e.g. string, dict, etc.).
- Missing required inputs.

## Category

`list`
