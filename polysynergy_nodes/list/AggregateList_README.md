# Aggregate List Node

The **Aggregate List** node calculates statistical aggregations (min, max, sum, average, count) for numeric lists. It can work with simple numeric lists or extract numeric fields from dictionaries.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  List of numbers or dictionaries with numeric fields.

- **field** (`str`, optional):
  If the list contains dictionaries, aggregate this numeric field. Leave empty to aggregate direct numeric values.

---

### Outputs

- **min_value** (`float`):
  Minimum value in the list.

- **max_value** (`float`):
  Maximum value in the list.

- **sum_value** (`float`):
  Sum of all values.

- **average_value** (`float`):
  Average (mean) of all values.

- **count** (`int`):
  Number of values aggregated.

- **true_path** (path):
  Triggered on success. Returns a dictionary with all aggregation results:
  ```json
  {
    "min": 1.0,
    "max": 10.0,
    "sum": 55.0,
    "average": 5.5,
    "count": 10
  }
  ```

- **false_path** (path):
  Triggered if aggregation fails. Returns error info.

---

## 🧠 Example Use

### Aggregate Simple Numeric List

```json
{
  "input_list": [1, 5, 3, 9, 2, 7]
}
```

**Output (`true_path`):**
```json
{
  "min": 1,
  "max": 9,
  "sum": 27,
  "average": 4.5,
  "count": 6
}
```

---

### Aggregate Dict Field

```json
{
  "input_list": [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
  ],
  "field": "score"
}
```

**Output (`true_path`):**
```json
{
  "min": 78,
  "max": 92,
  "sum": 255,
  "average": 85.0,
  "count": 3
}
```

---

## ⚠️ Notes

- Non-numeric values are automatically skipped (no error thrown).
- Empty lists or lists with no numeric values will trigger the `false_path`.
- Values are converted to float for aggregation.

---

## 🧩 Category

- `list`
