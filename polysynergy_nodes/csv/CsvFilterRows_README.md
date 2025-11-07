# CSV Filter Rows Node

The **CSV Filter Rows** node filters rows from CSV data based on column values and comparison operators. It supports various comparison types including equality, containment, and numeric comparisons.

---

## 🔧 Node Configuration

### Inputs

- **data** (`list`, required):
  List of dictionaries representing CSV data with headers. Use **CSV to List** node with `has_headers=True` to prepare data.

- **column** (`str`, required):
  The column name to filter on. Must exist in the data.

- **operator** (`str`, required):
  The comparison operator to apply. One of:
  - `"equals"`: Exact match (==)
  - `"not_equals"`: Not equal (!=)
  - `"contains"`: Substring or containment check
  - `"not_contains"`: Does not contain
  - `"starts_with"`: String starts with value
  - `"ends_with"`: String ends with value
  - `"greater_than"`: Numeric comparison (>)
  - `"less_than"`: Numeric comparison (<)
  - `"greater_equal"`: Numeric comparison (>=)
  - `"less_equal"`: Numeric comparison (<=)

- **value** (`any`, required):
  The value to compare against. Type depends on operator (string for text comparisons, number for numeric comparisons).

---

### Outputs

- **filtered_data** (`list`):
  The list of rows that matched the filter condition.

- **match_count** (`int`):
  Number of rows that matched the filter.

- **true_path** (path):
  Triggered on success. Returns the filtered data.

- **false_path** (path):
  Triggered if filtering fails. Returns error info.

---

## 🧠 Example Use

### Filter by Exact Match

```json
{
  "data": [
    {"name": "Alice", "city": "New York", "age": "30"},
    {"name": "Bob", "city": "London", "age": "25"},
    {"name": "Charlie", "city": "New York", "age": "35"}
  ],
  "column": "city",
  "operator": "equals",
  "value": "New York"
}
```

**Output (`filtered_data`):**
```json
[
  {"name": "Alice", "city": "New York", "age": "30"},
  {"name": "Charlie", "city": "New York", "age": "35"}
]
```

**Output (`match_count`):** `2`

---

### Filter by Numeric Comparison

```json
{
  "data": [
    {"name": "Alice", "age": "30"},
    {"name": "Bob", "age": "25"},
    {"name": "Charlie", "age": "35"}
  ],
  "column": "age",
  "operator": "greater_than",
  "value": 30
}
```

**Output (`filtered_data`):**
```json
[
  {"name": "Charlie", "age": "35"}
]
```

---

### Filter by Substring

```json
{
  "data": [
    {"email": "alice@example.com"},
    {"email": "bob@test.org"},
    {"email": "charlie@example.com"}
  ],
  "column": "email",
  "operator": "contains",
  "value": "example"
}
```

**Output (`filtered_data`):**
```json
[
  {"email": "alice@example.com"},
  {"email": "charlie@example.com"}
]
```

---

### Filter by Starts With

```json
{
  "data": [
    {"product": "iPhone 14"},
    {"product": "Samsung Galaxy"},
    {"product": "iPad Pro"}
  ],
  "column": "product",
  "operator": "starts_with",
  "value": "i"
}
```

**Output (`filtered_data`):**
```json
[
  {"product": "iPhone 14"},
  {"product": "iPad Pro"}
]
```

---

## ⚠️ Notes

- Data must be a list of dictionaries (use CSV to List with headers enabled).
- The specified column must exist in all rows, or an error will be triggered.
- String comparisons are case-sensitive.
- Numeric operators (`greater_than`, `less_than`, etc.) automatically convert values to floats. Non-numeric values are treated as non-matches.
- Empty data returns an empty list (not an error).
- For multiple filter conditions, chain multiple Filter Rows nodes together.

---

## 🧩 Category

- `csv`
