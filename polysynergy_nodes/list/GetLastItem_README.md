# Get Last Item Node

The **Get Last Item** node retrieves the last element from a list. It's a convenient shortcut for accessing the last item without needing to specify a negative index.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to get the last item from.

- **default_value** (`any`, optional):
  Value to return if the list is empty. Default: `None`.

---

### Outputs

- **item** (`any`):
  The last item in the list.

- **list_length** (`int`):
  Total length of the list.

- **true_path** (path):
  Triggered when item is found. Returns the last item.

- **false_path** (path):
  Triggered if the list is empty. Returns error info with default value.

---

## 🧠 Example Use

### Get Last Item from List

```json
{
  "input_list": ["apple", "banana", "cherry"]
}
```

**Output (`item`):** `"cherry"`
**Output (`list_length`):** `3`
**Output (`true_path`):** `"cherry"`

---

### Empty List with Default Value

```json
{
  "input_list": [],
  "default_value": "no items"
}
```

**Output (`item`):** `"no items"`
**Output (`list_length`):** `0`
**Output (`false_path`):**
```json
{
  "error": "List is empty",
  "default_value": "no items"
}
```

---

### Get Last Dict from List

```json
{
  "input_list": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
  ]
}
```

**Output (`item`):**
```json
{"name": "Bob", "age": 25}
```

---

## ⚠️ Notes

- This is a convenience node equivalent to accessing `list[-1]` in Python.
- If the list is empty and no default value is provided, `None` is returned.
- The `false_path` is triggered for empty lists, making it easy to handle edge cases.
- For accessing items at specific positions, use the **Get Item by Index** node instead.

---

## 🧩 Category

- `list`
