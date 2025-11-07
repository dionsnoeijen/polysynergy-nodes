# CSV Select Columns Node

The **CSV Select Columns** node extracts specific columns from CSV data, removing all other columns. It's useful for reducing data size, selecting relevant fields, or preparing data for downstream processing.

---

## 🔧 Node Configuration

### Inputs

- **data** (`list`, required):
  List of dictionaries representing CSV data with headers. Use **CSV to List** node with `has_headers=True` to prepare data.

- **columns** (`list`, required):
  List of column names to select. Example: `["name", "email"]`.

- **ignore_missing** (`bool`, optional):
  How to handle columns that don't exist in the data. Default: `True`.
  - If `True`: Skip columns that don't exist (no error)
  - If `False`: Raise error if any column is missing

---

### Outputs

- **selected_data** (`list`):
  The data with only the selected columns retained.

- **selected_columns** (`list`):
  List of columns that were actually selected (excludes missing columns if `ignore_missing=True`).

- **row_count** (`int`):
  Number of rows in the result.

- **true_path** (path):
  Triggered on success. Returns the data with selected columns.

- **false_path** (path):
  Triggered if selection fails. Returns error info.

---

## 🧠 Example Use

### Select Specific Columns

```json
{
  "data": [
    {"name": "Alice", "age": "30", "city": "New York", "email": "alice@example.com"},
    {"name": "Bob", "age": "25", "city": "London", "email": "bob@example.com"}
  ],
  "columns": ["name", "email"]
}
```

**Output (`selected_data`):**
```json
[
  {"name": "Alice", "email": "alice@example.com"},
  {"name": "Bob", "email": "bob@example.com"}
]
```

**Output (`selected_columns`):**
```json
["name", "email"]
```

---

### Reorder Columns

The output will have columns in the order specified:

```json
{
  "data": [
    {"age": "30", "name": "Alice", "city": "New York"}
  ],
  "columns": ["city", "name", "age"]
}
```

**Output (`selected_data`):**
```json
[
  {"city": "New York", "name": "Alice", "age": "30"}
]
```

---

### Handle Missing Columns (Ignore)

```json
{
  "data": [
    {"name": "Alice", "age": "30"}
  ],
  "columns": ["name", "email", "age"],
  "ignore_missing": true
}
```

**Output (`selected_data`):**
```json
[
  {"name": "Alice", "age": "30"}
]
```

**Output (`selected_columns`):**
```json
["name", "age"]
```

*Note: "email" was skipped because it doesn't exist.*

---

### Handle Missing Columns (Error)

```json
{
  "data": [
    {"name": "Alice", "age": "30"}
  ],
  "columns": ["name", "email"],
  "ignore_missing": false
}
```

**Output (`false_path`):**
```json
{
  "error": "Column 'email' not found in data. Available columns: name, age"
}
```

---

## ⚠️ Notes

- Data must be a list of dictionaries (use CSV to List with headers enabled).
- The `columns` parameter must be a non-empty list.
- Column order in the output matches the order in the `columns` parameter.
- Missing columns are filled with empty strings if `ignore_missing=True`.
- Empty data returns an empty list (not an error).
- This node is ideal for preparing data before converting back to CSV with **List to CSV** node.

---

## 🧩 Category

- `csv`
