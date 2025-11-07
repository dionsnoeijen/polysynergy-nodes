# CSV to List Node

The **CSV to List** node parses CSV (Comma-Separated Values) data from a string into a structured list format. It supports both header-based parsing (returning a list of dictionaries) and headerless parsing (returning a list of lists).

---

## 🔧 Node Configuration

### Inputs

- **csv_string** (`str`, required):
  The CSV data as a string. Can contain multiple rows separated by newlines.

- **delimiter** (`str`, optional):
  The delimiter character used to separate values. Default: `","` (comma). Common alternatives: `";"`, `"\t"` (tab), `"|"`.

- **has_headers** (`bool`, optional):
  Whether the first row contains column headers. Default: `True`.
  - If `True`: Returns list of dictionaries with header keys
  - If `False`: Returns list of lists

---

### Outputs

- **data** (`list`):
  Parsed CSV data. Format depends on `has_headers`:
  - With headers: `[{"col1": "val1", "col2": "val2"}, ...]`
  - Without headers: `[["val1", "val2"], ...]`

- **headers** (`list`):
  Column headers extracted from the first row. Empty list if `has_headers` is `False`.

- **row_count** (`int`):
  Number of data rows parsed (excluding header row).

- **true_path** (path):
  Triggered on success. Returns the parsed data.

- **false_path** (path):
  Triggered if parsing fails. Returns error info.

---

## 🧠 Example Use

### With Headers (Default)

```json
{
  "csv_string": "name,age,city\nAlice,30,New York\nBob,25,London",
  "delimiter": ",",
  "has_headers": true
}
```

**Output (`data`):**
```json
[
  {"name": "Alice", "age": "30", "city": "New York"},
  {"name": "Bob", "age": "25", "city": "London"}
]
```

**Output (`headers`):**
```json
["name", "age", "city"]
```

**Output (`row_count`):**
```
2
```

---

### Without Headers

```json
{
  "csv_string": "Alice,30,New York\nBob,25,London",
  "delimiter": ",",
  "has_headers": false
}
```

**Output (`data`):**
```json
[
  ["Alice", "30", "New York"],
  ["Bob", "25", "London"]
]
```

**Output (`headers`):**
```json
[]
```

---

### Custom Delimiter (Semicolon)

```json
{
  "csv_string": "name;age;city\nAlice;30;New York\nBob;25;London",
  "delimiter": ";",
  "has_headers": true
}
```

**Output (`data`):**
```json
[
  {"name": "Alice", "age": "30", "city": "New York"},
  {"name": "Bob", "age": "25", "city": "London"}
]
```

---

## ⚠️ Notes

- All values are returned as strings. Use type conversion nodes for numeric or date processing.
- Empty CSV strings will trigger the `false_path` with an error.
- The parser handles quoted fields and escaped characters according to CSV standards.
- For tab-separated values (TSV), use `"\t"` as delimiter.
- CSV parsing uses Python's built-in `csv` module for RFC 4180 compliance.

---

## 🧩 Category

- `csv`
