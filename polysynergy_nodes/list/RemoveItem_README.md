# Remove Item Node

The **Remove Item** node removes items from a list either by value (first or all occurrences) or by index position.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to remove items from.

- **mode** (`str`, required):
  How to identify items to remove. One of:

  - `"by_value"`: Remove first occurrence of the value (default)
  - `"by_value_all"`: Remove all occurrences of the value
  - `"by_index"`: Remove by index position

- **value** (`any`, optional):
  The value to remove (for `by_value` modes).

- **index** (`int`, optional):
  Position to remove from (for `by_index` mode, 0-based). Default: `0`.

---

### Outputs

- **modified_list** (`list`):
  The list with item(s) removed.

- **removed_count** (`int`):
  Number of items removed.

- **original_length** (`int`):
  Length of the original list.

- **new_length** (`int`):
  Length of the modified list.

- **true_path** (path):
  Triggered on success. Returns the modified list.

- **false_path** (path):
  Triggered if removal fails. Returns error info.

---

## 🧠 Example Use

### Remove First Occurrence by Value

```json
{
  "input_list": [1, 2, 3, 2, 4],
  "mode": "by_value",
  "value": 2
}
```

**Output (`true_path`):**
```json
[1, 3, 2, 4]
```
(Only the first `2` is removed)

---

### Remove All Occurrences by Value

```json
{
  "input_list": ["a", "b", "a", "c", "a"],
  "mode": "by_value_all",
  "value": "a"
}
```

**Output (`true_path`):**
```json
["b", "c"]
```
(All `"a"` values are removed)

---

### Remove by Index

```json
{
  "input_list": [10, 20, 30, 40, 50],
  "mode": "by_index",
  "index": 2
}
```

**Output (`true_path`):**
```json
[10, 20, 40, 50]
```
(Item at index 2, which is `30`, is removed)

---

## ⚠️ Notes

- The original list is not modified; a new list is returned.
- If a value is not found in `by_value` mode, no error is raised — the list is returned unchanged with `removed_count = 0`.
- For `by_index` mode, out-of-bounds indices trigger the `false_path`.
- Negative indices work for `by_index` mode (`-1` removes last item).

---

## 🧩 Category

- `list`
