# 🗑️ KeyValue - Remove Collection Node

The `KeyValue - Remove Collection` node deletes a specific key-value pair from a collection.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name to remove from           |
| key         | str    | ✅        | The key to remove                        |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | Confirmation message                        |
| false_path  | dict      | Error if key not found or removal fails     |

---

## ✅ Examples

### Remove Item from Collection:
```json
{
  "collection": "user_settings",
  "key": "temp_preference"
}
```
**Output:** `"Removed key 'temp_preference' from collection 'user_settings'"`

### Key Not Found:
```json
{
  "collection": "api_credentials",
  "key": "non_existent"
}
```
**Output (false_path):** `{"error": "Key 'non_existent' not found in collection 'api_credentials'"}`

---

## 🔒 Security Features

- **Ownership Verification**: Checks item belongs to current tenant/project
- **Pre-deletion Validation**: Verifies key exists before removal
- **Access Denial**: Prevents deletion of items from other tenants

---

## 💡 Use Cases

- Remove temporary or expired data from collection
- Clean up invalid configuration entries
- Delete outdated API credentials
- Remove specific user preferences

---

## ⚠️ Notes

- Returns error if collection or key doesn't exist
- Deletion is permanent and cannot be undone
- Security check prevents cross-tenant deletion
- Only removes the specified key, not the entire collection
