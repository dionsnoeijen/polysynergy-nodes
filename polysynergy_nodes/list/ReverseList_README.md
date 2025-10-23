# Reverse List Node

The **Reverse List** node reverses the order of items in a list, returning a new list with items in reverse order.

---

## 🔧 Node Configuration

### Inputs

- **input_list** (`list`, required):
  The list to reverse.

---

### Outputs

- **reversed_list** (`list`):
  The list with items in reverse order.

- **true_path** (path):
  Triggered on success. Returns the reversed list.

- **false_path** (path):
  Triggered if the operation fails. Returns error info.

---

## 🧠 Example Use

### Input:
```json
{
  "input_list": [1, 2, 3, 4, 5]
}
```

### Output (`true_path`):
```json
[5, 4, 3, 2, 1]
```

---

### With Strings:
```json
{
  "input_list": ["apple", "banana", "cherry"]
}
```

### Output (`true_path`):
```json
["cherry", "banana", "apple"]
```

---

## ⚠️ Notes

- The original list is not modified; a new reversed list is returned.
- Works with any list type: numbers, strings, objects, mixed types.

---

## 🧩 Category

- `list`
