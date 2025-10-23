# Group By Node

The **Group By** node groups list items by a specified field value, creating a dictionary where keys are the unique field values and values are lists of items sharing that field value.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  List of dictionaries (or objects) to group.

- **field** (`str`, required):
  The field/key to group by.

---

### Outputs

- **grouped_dict** (`dict`):
  Dictionary with field values as keys and lists of items as values.

- **group_count** (`int`):
  Number of distinct groups created.

- **original_length** (`int`):
  Total number of items in the original list.

- **true_path** (path):
  Triggered on success. Returns the grouped dictionary.

- **false_path** (path):
  Triggered if grouping fails. Returns error info.

---

## 🧠 Example Use

### Group Users by Department

```json
{
  "input_list": [
    {"name": "Alice", "department": "Engineering"},
    {"name": "Bob", "department": "Sales"},
    {"name": "Charlie", "department": "Engineering"},
    {"name": "Diana", "department": "Sales"},
    {"name": "Eve", "department": "HR"}
  ],
  "field": "department"
}
```

**Output (`true_path`):**
```json
{
  "Engineering": [
    {"name": "Alice", "department": "Engineering"},
    {"name": "Charlie", "department": "Engineering"}
  ],
  "Sales": [
    {"name": "Bob", "department": "Sales"},
    {"name": "Diana", "department": "Sales"}
  ],
  "HR": [
    {"name": "Eve", "department": "HR"}
  ]
}
```

---

### Group Products by Category

```json
{
  "input_list": [
    {"product": "Laptop", "category": "Electronics", "price": 999},
    {"product": "Desk", "category": "Furniture", "price": 299},
    {"product": "Mouse", "category": "Electronics", "price": 25},
    {"product": "Chair", "category": "Furniture", "price": 199}
  ],
  "field": "category"
}
```

**Output (`true_path`):**
```json
{
  "Electronics": [
    {"product": "Laptop", "category": "Electronics", "price": 999},
    {"product": "Mouse", "category": "Electronics", "price": 25}
  ],
  "Furniture": [
    {"product": "Desk", "category": "Furniture", "price": 299},
    {"product": "Chair", "category": "Furniture", "price": 199}
  ]
}
```

---

## ⚠️ Notes

- If an item is missing the specified field, it's grouped under the key `"None"`.
- All group keys are converted to strings for consistency.
- Works with both dictionary items and objects with attributes.

---

## 🧩 Category

- `list`
