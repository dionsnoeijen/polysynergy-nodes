# Slice List Node

The **Slice List** node extracts a portion of a list based on various slicing modes. It supports extracting the first N items, last N items, or custom ranges.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to slice.

- **slice_mode** (`str`, required):
  How to slice the list. One of:

  - `first_n`: Take the first N items
  - `last_n`: Take the last N items (default)
  - `range`: Take items from start_index to end_index
  - `from_index`: Take items from start_index to the end
  - `to_index`: Take items from the start to end_index

- **count** (`int`, optional):
  Number of items to take (for `first_n` and `last_n` modes). Default: `10`.

- **start_index** (`int`, optional):
  Starting index for range-based slicing (0-based). Default: `0`.

- **end_index** (`int`, optional):
  Ending index for range-based slicing (exclusive). Default: `10`.

---

### Outputs

- **sliced_list** (`list`):
  The resulting sliced portion of the list.

- **original_length** (`int`):
  Length of the input list.

- **sliced_length** (`int`):
  Length of the sliced result.

- **true_path** (path):
  Triggered on success. Returns the sliced list.

- **false_path** (path):
  Triggered if slicing fails. Returns error info.

---

## 🧠 Example Use

### Get Last 10 Items

```json
{
  "input_list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  "slice_mode": "last_n",
  "count": 10
}
```

**Output (`true_path`):**
```json
[3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```

---

### Get Items from Index 5 to 10

```json
{
  "input_list": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "slice_mode": "range",
  "start_index": 5,
  "end_index": 10
}
```

**Output (`true_path`):**
```json
[5, 6, 7, 8, 9]
```

---

## ⚠️ Notes

- All slice operations are safe and will not throw errors for out-of-bounds indices.
- Python's standard list slicing behavior applies (negative indices work in `last_n` mode).
- The `end_index` in range mode is exclusive (does not include the item at that index).

---

## 🧩 Category

- `list`
