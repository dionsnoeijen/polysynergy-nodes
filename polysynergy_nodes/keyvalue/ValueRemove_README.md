# 🗑️ KeyValue - Remove Value Node

The `KeyValue - Remove Value` node deletes a key-value pair from persistent storage.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name    | Type   | Required | Description                              |
|---------|--------|----------|------------------------------------------|
| key     | str    | ✅        | The key to remove                        |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | Confirmation message with removed key       |
| false_path  | dict      | Error if key not found or removal fails     |

---

## ✅ Example

### Remove Existing Key:
```json
{
  "key": "temp_session_data"
}
```
**Output:** `"Removed key 'temp_session_data'"`

### Attempt to Remove Non-existent Key:
```json
{
  "key": "non_existent"
}
```
**Output (false_path):** `{"error": "Key 'non_existent' not found"}`

---

## 🔒 Security Features

- **Ownership Verification**: Checks that key belongs to current tenant/project
- **Pre-deletion Check**: Verifies key exists before attempting removal
- **Access Denial**: Prevents removal of keys from other tenants/projects

---

## 💡 Use Cases

- Clean up temporary session data
- Remove outdated cached values
- Delete user preferences on reset
- Clear expired or invalid data

---

## ⚠️ Notes

- Returns error if key doesn't exist (not silent deletion)
- Security check prevents cross-tenant deletion
- Cannot be undone - use with caution
- Includes detailed error information in `false_path`
