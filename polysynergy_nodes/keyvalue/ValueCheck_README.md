# ✔️ KeyValue - Check Value Node

The `KeyValue - Check Value` node checks if a key exists in persistent storage without retrieving its value.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name    | Type   | Required | Description                              |
|---------|--------|----------|------------------------------------------|
| key     | str    | ✅        | The key to check for                     |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | bool      | True if key exists                          |
| false_path  | bool      | False if key doesn't exist or access error  |

---

## ✅ Example

### Check for Existing Key:
```json
{
  "key": "theme"
}
```
**Output:** `true` (if key exists)

### Check for Non-existent Key:
```json
{
  "key": "missing_key"
}
```
**Output (false_path):** `false`

---

## 🔀 Flow Control

This node is useful for conditional branching:
- **true_path**: Key exists → proceed with retrieval or update
- **false_path**: Key doesn't exist → create new entry or use default

---

## 💡 Use Cases

- Check if user preferences are initialized
- Validate session data exists before accessing
- Conditional logic based on key presence
- Guard against missing configuration

---

## ⚠️ Notes

- Returns `false` instead of error for non-existent keys
- Security check ensures key belongs to current tenant/project
- Does not return the actual value (use `Get Value` for that)
- Minimal data transfer - efficient for existence checks
