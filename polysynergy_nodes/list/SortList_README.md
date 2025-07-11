# Sort List Node

The **Sort List** node allows sorting of a list of elements, either as primitive values (like numbers or strings) or dictionaries based on a given key.

## Inputs

- `Input List` (list, required): The list to be sorted. Can contain primitive values or dictionaries.
- `Sort Key` (str, optional): If sorting dictionaries, this is the key to sort on.
- `Sort Order` (str, required): Either `"asc"` (ascending) or `"desc"` (descending). Default is `"asc"`.

## Outputs

- `true_path` (list): The sorted list.
- `false_path` (dict): Contains error info if the operation fails.

## Behavior

- If no key is specified and the list contains primitives, it is sorted directly.
- If a key is specified, it tries to sort dictionaries based on that key.
- If a non-comparable type is encountered, it falls back to string representation for comparison.
- Raises an error if the input is not a list.

## Example

### Input:
```json
{
  "input_list": [{"name": "Charlie"}, {"name": "Alice"}, {"name": "Bob"}],
  "sort_key": "name",
  "sort_order": "asc"
}
```

### Output (`true_path`):
```json
[
  {"name": "Alice"},
  {"name": "Bob"},
  {"name": "Charlie"}
]
```

## Errors

- `Input must be a list` if the input is not of type `list`.

