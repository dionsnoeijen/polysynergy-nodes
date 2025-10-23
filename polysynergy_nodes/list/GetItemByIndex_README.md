# Get Item by Index Node

The **Get Item by Index** node extracts a single item from a list by its position (index). It supports negative indices and has a safe mode for handling out-of-bounds access.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to get an item from.

- **index** (`int`, required):
  Position of the item to get (0-based). Negative indices count from the end (-1 is last item). Default: `0`.

- **use_safe_mode** (`bool`, optional):
  If `True`, returns `false_path` for out-of-bounds instead of raising an exception. Default: `True`.

- **default_value** (`any`, optional):
  Value to return if index is out of bounds (only used in safe mode). Default: `None`.

---

### Outputs

- **item** (`any`):
  The item at the specified index.

- **list_length** (`int`):
  Total length of the list.

- **true_path** (path):
  Triggered when item is found. Returns the item.

- **false_path** (path):
  Triggered if index is out of bounds (in safe mode) or operation fails. Returns error info and default value.

---

## 🧠 Example Use

### Get First Item

```json
{
  "input_list": ["a", "b", "c", "d"],
  "index": 0
}
```

**Output (`true_path`):**
```
"a"
```

---

### Get Last Item (Negative Index)

```json
{
  "input_list": [10, 20, 30, 40],
  "index": -1
}
```

**Output (`true_path`):**
```
40
```

---

### Safe Mode with Default

```json
{
  "input_list": [1, 2, 3],
  "index": 10,
  "use_safe_mode": true,
  "default_value": "Not found"
}
```

**Output (`true_path`):**
```
"Not found"
```

**And `false_path` contains:**
```json
{
  "error": "Index 10 out of range for list of length 3",
  "default_value": "Not found"
}
```

---

## ⚠️ Notes

- Negative indices work: `-1` is the last item, `-2` is second-to-last, etc.
- In safe mode, out-of-bounds returns `default_value` via `true_path` and error info via `false_path`.
- With safe mode off, out-of-bounds raises an exception.

---

## 🧩 Category

- `list`
