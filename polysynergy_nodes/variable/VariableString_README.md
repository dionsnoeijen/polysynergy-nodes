
# 📝 Variable String Node

The `Variable String` node is part of the **variable** category and is used to replace placeholders in a string with corresponding values. The placeholders are replaced using a set of defined variables or values, and the result is outputted as the final string. If the replacement fails, an error is returned.

---

## ✅ Functionality

This node takes a string with placeholders (e.g., `{name}`) and replaces them with corresponding values from a given dictionary. The dictionary can contain values like `"name": "John"`, and the node will replace the placeholder `{name}` with `"John"` in the string.

---

## 🔌 Inputs

| Name     | Type       | Required | Description                              |
|----------|------------|----------|------------------------------------------|
| value    | string     | Yes      | The string with placeholders to replace. |
| values   | dictionary | Yes      | A dictionary of values to replace in the string. |

---

## 🔀 Outputs

| Name        | Type      | Description                               |
|-------------|-----------|-------------------------------------------|
| true_path   | string    | The string with placeholders replaced.    |
| false_path  | dictionary| Error message if placeholder replacement fails. |

---

## 💡 Example

### Input:
```json
{
  "value": "Hello, {name}! You have {count} new messages.",
  "values": {
    "name": "John",
    "count": "5"
  }
}
```

### Output via `true_path`:
```json
"Hello, John! You have 5 new messages."
```

### Output via `false_path` (in case of an error):
```json
{
  "error": "Missing placeholder: {count}"
}
```

---

## ⚠️ Notes

- Placeholders must be wrapped in curly braces (`{}`), e.g., `{name}`.
- If a placeholder is missing in the `values` dictionary, an error will be raised and stored in `false_path`.
- This node can handle nested placeholders like `{node.something}` and even external references like `{a.b.c}`.
- The input string can be JSON-formatted, in which case nested objects will also have their placeholders replaced.
- The node supports replacing values from a variety of sources: internal node values (`node.something`), external state values, and the provided `values` dictionary.

---

## 🔧 Dependencies

- **replace_placeholders**: A function that handles the actual replacement of placeholders in the input string or JSON structure.
