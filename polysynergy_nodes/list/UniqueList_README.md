# 🧩 Unique List Node

The `Unique List` node is part of the `list` category and is responsible for removing duplicate elements from a list.

---

## ✅ Functionality

This node removes all duplicate values from the provided list while preserving the order of first appearance.

---

## 🔌 Inputs

| Name         | Type  | Required | Description                                          |
|--------------|-------|----------|------------------------------------------------------|
| `input_list` | list  | Yes      | The list from which duplicates should be removed.    |

---

## 🔀 Outputs

| Name         | Type  | Description                                |
|--------------|-------|--------------------------------------------|
| `true_path`  | list  | The list containing only unique elements.   |
| `false_path` | dict  | Contains an error message if something fails. |

---

## 📌 Example

### Input:
```json
["apple", "banana", "apple", "orange", "banana"]
```

### Output via `true_path`:
```json
["apple", "banana", "orange"]
```

---

## ⚠️ Note

- The order of items is preserved: only the first occurrence of an item is kept.
- Supports any type in the list (strings, numbers, dicts, etc.), but be aware that unhashable items may cause issues if you use sets in your own modifications.

---

## 🧪 Test

A unittest is available in `test_unique_list.py` which verifies that duplicates are properly filtered.