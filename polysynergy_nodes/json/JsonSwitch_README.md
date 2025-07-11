# 🔀 JSON Switch Node

The **JSON Switch** node allows conditional branching based on values extracted from a JSON input using a JMESPath expression.

---

## ✅ Functionality

- Parses input JSON (as string or dict)
- Executes a **JMESPath** query
- Matches the result to predefined branches
- Only keeps the matching output path alive (kills others)

---

## 🔌 Inputs

| Name             | Type   | Required | Description |
|------------------|--------|----------|-------------|
| `json_as_string` | string | Optional | Raw JSON input (string format) |
| `json_as_dict`   | dict   | Optional | Pre-parsed JSON dict |
| `json_path`      | string | ✅        | JMESPath expression used to extract a value |

> Either `json_as_string` or `json_as_dict` must contain valid data.

---

## ⚙️ Settings

| Name      | Type  | Description |
|-----------|-------|-------------|
| `branches` | dict | Defines branches that can be matched. Keys represent values the switch can match on. |

---

## 🔀 Output

- **Matching branch:** Only the matching connection remains active.
- **Other branches:** Their connections are killed (`make_killer()` called).
- **`false_path`:** Triggered if no match or if JSON parsing/query fails.

---

## 📌 Example

```json
{
  "type": "email",
  "payload": {
    "to": "hello@example.com"
  }
}
```

- `json_path`: `type`
- `branches`: `{"email": ..., "sms": ...}`

✅ Result: only the `email` branch remains active, others are killed.

---

## ❗ Notes

- Uses `jmespath` for powerful and flexible querying.
- Matching is done **as strings**.
- Can return errors in `false_path` for invalid JSON or paths.

