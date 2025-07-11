# Filter List Node

The **Filter List** node is a utility node in the `list` category designed to filter items from a list based on specific conditions. It supports basic match types like equality, containment, and numeric comparisons, and can filter based on fields within objects (dictionaries).

---

## 🔧 Node Configuration

### Inputs

- **list_to_filter** (`list`, required):  
  The input list to apply filtering on. Can be a list of strings, numbers, or dicts.

- **match_field** (`str`, optional):  
  If the list contains dicts, this specifies which key to evaluate for the filter condition.

- **match_value** (`any`, required):  
  The value to match against. Used with the selected `match_mode`.

- **match_mode** (`str`, required):  
  The type of match to apply. One of:
  
  - `equals`: Exact match
  - `contains`: Substring or list containment
  - `greater_than`: For numeric comparisons
  - `less_than`: For numeric comparisons
  - `starts_with`: Checks if a string starts with the match value

---

### Outputs

- **filtered_list** (`list`):  
  The list of items that matched the filter.

- **true_path** (path):  
  Triggered if at least one match was found. Output is the filtered list.

- **false_path** (path):  
  Triggered if no matches were found.

---

## 🧠 Example Use

Imagine a list of dictionaries like:

```json
[
  { "name": "Alice", "age": 30 },
  { "name": "Bob", "age": 20 },
  { "name": "Charlie", "age": 40 }
]
```

To filter users where `age > 25`, set:

- `match_field`: `"age"`
- `match_value`: `25`
- `match_mode`: `"greater_than"`

---

## ⚠️ Notes

- If `match_field` is empty, the item itself is evaluated (works for flat lists).
- Matching is **case-sensitive** for strings.
- Type safety is not enforced — incorrect value types may result in a failed match or exception.

---

## 🧩 Category

- `list`
- `util`

