# 🧩 Zip Inject Node

The `Zip Inject` node is part of the `utils` category and is designed to combine two lists by injecting values from one list into elements of another list at a specified path.

---

## ✅ Functionality

This node takes two equally long lists:
- A **source list** of dictionaries.
- A **values list** containing any values (e.g. embeddings, scores, labels).

It then injects each value from the second list into the corresponding dictionary in the source list using a dot-notated target path.

Supports both direct list input and JSON strings for maximum flexibility.

---

## 🔌 Inputs

| Name                      | Type  | Required | Description                                                                 |
|---------------------------|-------|----------|-----------------------------------------------------------------------------|
| `source_list`             | list  | No       | A list of dictionaries into which values will be injected.                 |
| `source_list_as_string`   | str   | No       | JSON string version of `source_list`, useful when using a handle or input. |
| `values_to_inject`        | list  | No       | A list of values to inject into each dictionary in the source list.        |
| `values_to_inject_as_string` | str | No       | JSON string version of `values_to_inject`.                                 |
| `target_path`             | str   | Yes      | Dot-notated path (e.g. `package.embedding`) where the value will be injected. |

> **Note**: Either `source_list` or `source_list_as_string` must be provided. Same applies to `values_to_inject` and `values_to_inject_as_string`.

---

## 🔀 Outputs

| Name         | Type  | Description                                                               |
|--------------|-------|---------------------------------------------------------------------------|
| `true_path`  | list  | The resulting list of dictionaries after values have been injected.        |
| `false_path` | dict  | Contains an error message if an exception occurs (e.g. JSON parse error). |

---

## 📌 Example

### Inputs:

#### `source_list_as_string`
```json
[
  { "id": "1", "package": { "embedding_text": "a" } },
  { "id": "2", "package": { "embedding_text": "b" } }
]
```

#### `values_to_inject_as_string`
```json
[
  [0.1, 0.2, 0.3],
  [0.4, 0.5, 0.6]
]
```

#### `target_path`
```
package.embedding
```

### Output via `true_path`:
```json
[
  { "id": "1", "package": { "embedding_text": "a", "embedding": [0.1, 0.2, 0.3] } },
  { "id": "2", "package": { "embedding_text": "b", "embedding": [0.4, 0.5, 0.6] } }
]
```

---

## ⚠️ Notes

- Both lists must have the same length. Otherwise, an error will be raised.
- If the `target_path` leads through non-existent keys, intermediate dictionaries will be created.
- Supports both object-based input and JSON strings, making it highly compatible with dynamic handle-based flows.

