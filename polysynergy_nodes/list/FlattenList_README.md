# Flatten List Node

The **Flatten List** node converts nested lists into a single flat list. You can configure how many levels deep to flatten.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The nested list to flatten.

- **depth** (`str`, required):
  How many levels deep to flatten. One of:

  - `"1"`: Flatten one level only
  - `"2"`: Flatten two levels
  - `"all"`: Fully flatten all nested levels (default)

---

### Outputs

- **flattened_list** (`list`):
  The flattened list result.

- **original_length** (`int`):
  Number of items in the original list (before flattening).

- **flattened_length** (`int`):
  Number of items in the flattened list (after flattening).

- **true_path** (path):
  Triggered on success. Returns the flattened list.

- **false_path** (path):
  Triggered if flattening fails. Returns error info.

---

## 🧠 Example Use

### Flatten All Levels

```json
{
  "input_list": [[1, 2], [3, [4, 5]], [[6]]],
  "depth": "all"
}
```

**Output (`true_path`):**
```json
[1, 2, 3, 4, 5, 6]
```

---

### Flatten One Level Only

```json
{
  "input_list": [[1, 2], [3, [4, 5]], [6]],
  "depth": "1"
}
```

**Output (`true_path`):**
```json
[1, 2, 3, [4, 5], 6]
```

---

### Flatten Two Levels

```json
{
  "input_list": [[[1, 2]], [[3, 4]]],
  "depth": "2"
}
```

**Output (`true_path`):**
```json
[1, 2, 3, 4]
```

---

## ⚠️ Notes

- Non-list items are preserved as-is during flattening.
- Empty nested lists are flattened away.
- The `"all"` mode recursively flattens to any depth.

---

## 🧩 Category

- `list`
