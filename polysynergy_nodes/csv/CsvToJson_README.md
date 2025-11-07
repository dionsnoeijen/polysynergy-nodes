# CSV to JSON Node

The **CSV to JSON** node converts CSV data (already parsed into a list format) into JSON string format. It's useful for API integrations, data exports, or any scenario where JSON output is required.

---

## 🔧 Node Configuration

### Inputs

- **data** (`list`, required):
  List of dictionaries or lists representing CSV data. Typically output from **CSV to List** node.

- **indent** (`int`, optional):
  Number of spaces for JSON indentation. Default: `2`.
  - Set to `0` for compact JSON (no formatting)
  - Set to `2` or `4` for readable, indented JSON

---

### Outputs

- **json_string** (`str`):
  The resulting JSON data as a formatted string.

- **json_object** (`list`):
  The data as a Python object (same as input). Useful for further processing without re-parsing.

- **row_count** (`int`):
  Number of rows converted.

- **true_path** (path):
  Triggered on success. Returns the JSON string.

- **false_path** (path):
  Triggered if conversion fails. Returns error info.

---

## 🧠 Example Use

### Default (Indented JSON)

```json
{
  "data": [
    {"name": "Alice", "age": "30", "city": "New York"},
    {"name": "Bob", "age": "25", "city": "London"}
  ],
  "indent": 2
}
```

**Output (`json_string`):**
```json
[
  {
    "name": "Alice",
    "age": "30",
    "city": "New York"
  },
  {
    "name": "Bob",
    "age": "25",
    "city": "London"
  }
]
```

---

### Compact JSON (No Indentation)

```json
{
  "data": [
    {"name": "Alice", "age": "30"},
    {"name": "Bob", "age": "25"}
  ],
  "indent": 0
}
```

**Output (`json_string`):**
```json
[{"name":"Alice","age":"30"},{"name":"Bob","age":"25"}]
```

---

### Empty Data

```json
{
  "data": []
}
```

**Output (`json_string`):**
```json
[]
```

---

## 🧠 Common Workflow

This node is typically used in a pipeline:

1. **CSV to List** - Parse CSV string into list of dicts
2. **CSV Filter Rows** (optional) - Filter data
3. **CSV Select Columns** (optional) - Select specific columns
4. **CSV to JSON** - Convert to JSON for output

Example:
```
CSV String → CSV to List → CSV Filter Rows → CSV Select Columns → CSV to JSON → HTTP Request
```

---

## ⚠️ Notes

- Input data must be a non-empty list.
- The `ensure_ascii=False` flag is used to preserve Unicode characters in the output.
- Empty data returns `"[]"` (not an error).
- The `json_object` output is identical to the input `data`, provided for convenience in workflows where both JSON string and object are needed.
- For very large datasets, consider using compact JSON (`indent=0`) to reduce output size.

---

## 🧩 Category

- `csv`
