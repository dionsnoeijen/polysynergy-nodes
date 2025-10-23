# Append/Insert Item Node

The **Append/Insert Item** node adds a single item to a list at a specified position. It supports appending to the end, prepending to the start, or inserting at a specific index.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to add an item to.

- **item** (`any`, required):
  The item to add to the list. Can be any type: string, number, dict, list, etc.

- **mode** (`str`, required):
  Where to add the item. One of:

  - `"append"`: Add to the end of the list (default)
  - `"prepend"`: Add to the start of the list
  - `"insert"`: Insert at a specific index

- **index** (`int`, optional):
  Position to insert at (for `insert` mode only). 0-based indexing. Default: `0`.

---

### Outputs

- **modified_list** (`list`):
  The list with the item added.

- **new_length** (`int`):
  Length of the modified list.

- **true_path** (path):
  Triggered on success. Returns the modified list.

- **false_path** (path):
  Triggered if the operation fails. Returns error info.

---

## 🧠 Example Use

### Append to End

```json
{
  "input_list": [1, 2, 3],
  "item": 4,
  "mode": "append"
}
```

**Output (`true_path`):**
```json
[1, 2, 3, 4]
```

---

### Prepend to Start

```json
{
  "input_list": ["b", "c", "d"],
  "item": "a",
  "mode": "prepend"
}
```

**Output (`true_path`):**
```json
["a", "b", "c", "d"]
```

---

### Insert at Index

```json
{
  "input_list": [1, 2, 4, 5],
  "item": 3,
  "mode": "insert",
  "index": 2
}
```

**Output (`true_path`):**
```json
[1, 2, 3, 4, 5]
```

---

## ⚠️ Notes

- The original list is not modified; a new list is returned.
- For `insert` mode, index must be within valid range: `0 <= index <= len(list)`.
- Out-of-bounds indices will trigger the `false_path` with an error.

---

## 🧩 Category

- `list`
