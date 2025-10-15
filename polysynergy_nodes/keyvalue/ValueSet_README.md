# 💾 KeyValue - Set Value Node

The `KeyValue - Set Value` node stores a key-value pair in persistent DynamoDB storage. Values are stored in a default "simple" collection and are isolated per tenant/project.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name    | Type   | Required | Description                              |
|---------|--------|----------|------------------------------------------|
| key     | str    | ✅        | The key to store (e.g. 'theme', 'username') |
| value   | str    | ✅        | The value to store                       |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The stored value                            |
| false_path  | dict      | Error information if storage fails          |

---

## ✅ Example

### Store User Preference:
```json
{
  "key": "theme",
  "value": "dark"
}
```
**Output:** `"dark"`

### Store Session Data:
```json
{
  "key": "last_login",
  "value": "2025-01-15T10:30:00Z"
}
```
**Output:** `"2025-01-15T10:30:00Z"`

---

## 🔒 Security Features

- **Tenant Isolation**: Data is automatically scoped to current tenant and project
- **Environment Variables**: Requires `TENANT_ID` and `PROJECT_ID` to be set
- **Placeholder Support**: Keys and values support placeholder replacement

---

## 💡 Use Cases

- Store user preferences and settings
- Cache temporary session data
- Maintain application state across executions
- Store configuration values

---

## ⚠️ Notes

- Stored in DynamoDB table with automatic tenant/project isolation
- Keys and values support placeholder replacement (e.g. `{user_id}`)
- Overwrites existing values with the same key
- Requires AWS credentials configured in environment
