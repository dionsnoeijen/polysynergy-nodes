# List to CSV Node

The **List to CSV** node converts structured list data into CSV (Comma-Separated Values) format. It supports converting both lists of dictionaries and lists of lists into CSV strings.

---

## 🔧 Node Configuration

### Inputs

- **data** (`list`, required):
  The data to convert to CSV. Can be:
  - List of dictionaries: `[{"name": "Alice", "age": 30}, ...]`
  - List of lists: `[["Alice", 30], ["Bob", 25], ...]`

- **delimiter** (`str`, optional):
  The delimiter character to separate values. Default: `","` (comma). Common alternatives: `";"`, `"\t"` (tab), `"|"`.

- **include_headers** (`bool`, optional):
  Whether to include column headers in the output. Default: `True`.
  - For dict lists: Uses dictionary keys as headers
  - For list of lists: Uses `headers` parameter if provided

- **headers** (`list`, optional):
  Custom headers for list of lists. If not provided, dict keys are used automatically for dict lists. Default: `None`.

---

### Outputs

- **csv_string** (`str`):
  The resulting CSV data as a string, with rows separated by newlines.

- **row_count** (`int`):
  Number of data rows written (excluding header row).

- **true_path** (path):
  Triggered on success. Returns the CSV string.

- **false_path** (path):
  Triggered if conversion fails. Returns error info.

---

## 🧠 Example Use

### List of Dictionaries (Default)

```json
{
  "data": [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "London"}
  ],
  "delimiter": ",",
  "include_headers": true
}
```

**Output (`csv_string`):**
```
name,age,city
Alice,30,New York
Bob,25,London
```

---

### List of Dictionaries Without Headers

```json
{
  "data": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
  ],
  "include_headers": false
}
```

**Output (`csv_string`):**
```
Alice,30
Bob,25
```

---

### List of Lists with Custom Headers

```json
{
  "data": [
    ["Alice", 30, "New York"],
    ["Bob", 25, "London"]
  ],
  "headers": ["name", "age", "city"],
  "include_headers": true
}
```

**Output (`csv_string`):**
```
name,age,city
Alice,30,New York
Bob,25,London
```

---

### Custom Delimiter (Semicolon)

```json
{
  "data": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
  ],
  "delimiter": ";"
}
```

**Output (`csv_string`):**
```
name;age
Alice;30
Bob;25
```

---

## ⚠️ Notes

- Empty data lists will trigger the `false_path` with an error.
- For lists of dictionaries, headers are automatically extracted from the first dictionary's keys.
- For lists of lists, headers must be explicitly provided if `include_headers` is `True`.
- Values are automatically quoted if they contain the delimiter or special characters.
- Uses Python's built-in `csv` module for RFC 4180 compliance.

---

## 🧩 Category

- `csv`
