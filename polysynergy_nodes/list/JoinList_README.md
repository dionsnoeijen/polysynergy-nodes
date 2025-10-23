# Join List to String Node

The **Join List to String** node concatenates list items into a single string with a configurable separator. It can extract fields from dictionaries before joining.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to join into a string.

- **separator** (`str`, optional):
  String to insert between items. Default: `", "`.

  Examples: `", "`, `"\n"`, `";"`, `" | "`

- **field** (`str`, optional):
  If the list contains dictionaries, extract this field before joining. Leave empty to join items directly.

---

### Outputs

- **joined_string** (`str`):
  The resulting concatenated string.

- **item_count** (`int`):
  Number of items that were joined.

- **true_path** (path):
  Triggered on success. Returns the joined string.

- **false_path** (path):
  Triggered if the operation fails. Returns error info.

---

## 🧠 Example Use

### Join Simple List

```json
{
  "input_list": ["apple", "banana", "cherry"],
  "separator": ", "
}
```

**Output (`true_path`):**
```
"apple, banana, cherry"
```

---

### Join with Newlines

```json
{
  "input_list": ["Line 1", "Line 2", "Line 3"],
  "separator": "\n"
}
```

**Output (`true_path`):**
```
"Line 1
Line 2
Line 3"
```

---

### Join Dict Field

```json
{
  "input_list": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
  ],
  "field": "name",
  "separator": ", "
}
```

**Output (`true_path`):**
```
"Alice, Bob, Charlie"
```

---

## ⚠️ Notes

- All items are converted to strings before joining.
- `None` values are converted to empty strings.
- If a dict is missing the specified field, an empty string is used for that item.

---

## 🧩 Category

- `list`
