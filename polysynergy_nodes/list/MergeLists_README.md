# 🔗 Merge Lists Node

The `Merge Lists` node combines two lists into one, with optional duplicate removal.

---

## 📂 Category

**list**

---

## ⚙️ Inputs

| Name              | Type   | Required | Description                              |
|-------------------|--------|----------|------------------------------------------|
| list_a            | list   | ✅        | First list to merge                      |
| list_b            | list   | ✅        | Second list to merge                     |
| remove_duplicates | bool   | ❌        | Remove duplicate values (default: false) |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | list      | Combined list                               |
| false_path  | dict      | Error if merging fails                      |

---

## ✅ Examples

### Basic Merge:
```json
{
  "list_a": [1, 2, 3],
  "list_b": [4, 5, 6]
}
```
**Output:** `[1, 2, 3, 4, 5, 6]`

### Merge with Duplicates:
```json
{
  "list_a": ["apple", "banana"],
  "list_b": ["banana", "cherry"],
  "remove_duplicates": false
}
```
**Output:** `["apple", "banana", "banana", "cherry"]`

### Remove Duplicates:
```json
{
  "list_a": ["apple", "banana"],
  "list_b": ["banana", "cherry"],
  "remove_duplicates": true
}
```
**Output:** `["apple", "banana", "cherry"]`

### Mixed Types:
```json
{
  "list_a": [1, "two", 3],
  "list_b": ["four", 5, 6]
}
```
**Output:** `[1, "two", 3, "four", 5, 6]`

---

## 🔄 Duplicate Detection

When `remove_duplicates` is `true`:
- Uses string representation for comparison
- Preserves first occurrence order
- Works with any data type
- Comparison: `str(item)` for uniqueness

Example:
```
Input: [1, "1", 1.0, {"a": 1}]
Output: [1, {"a": 1}]  // "1" and 1.0 considered duplicates of 1
```

---

## 💡 Use Cases

- **Combine Data Sources**: Merge results from multiple queries
- **Deduplicate**: Remove duplicates from combined lists
- **Accumulate Results**: Gather data from different processes
- **Union Operations**: Create unified lists from separate sources

---

## ⚠️ Notes

- Both inputs must be valid lists
- Order preserved: List A items first, then List B items
- Duplicate detection uses string comparison
- Empty lists are valid inputs
- Type validation triggers `false_path` on error
