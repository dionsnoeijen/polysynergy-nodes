# 🔎 KeyValue - Get Collection Node

The `KeyValue - Get Collection` node retrieves a value from a specific collection using its key.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name to search in             |
| key         | str    | ✅        | The key to retrieve                      |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The retrieved value                         |
| false_path  | dict      | Error if key not found or retrieval fails   |

---

## ✅ Examples

### Retrieve from User Settings:
```json
{
  "collection": "user_settings",
  "key": "notification_enabled"
}
```
**Output:** `"true"` (if previously stored)

### Key Not Found:
```json
{
  "collection": "api_credentials",
  "key": "missing_token"
}
```
**Output (false_path):** `{"error": "Key 'missing_token' not found in collection 'api_credentials'"}`

---

## 🔒 Security Features

- **Ownership Verification**: Only retrieves values from current tenant/project
- **Collection Isolation**: Keys from different collections don't conflict
- **Access Control**: Prevents cross-tenant data access

---

## 💡 Use Cases

- Load module-specific configuration
- Retrieve API credentials per service
- Access organized user preferences
- Fetch grouped application state

---

## ⚠️ Notes

- Returns error if collection or key doesn't exist
- Both collection and key support placeholder replacement
- Security check ensures data belongs to current tenant/project
- Collection must exist with the specified key
