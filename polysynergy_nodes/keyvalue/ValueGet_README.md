# 🔍 KeyValue - Get Value Node

The `KeyValue - Get Value` node retrieves a previously stored value from persistent DynamoDB storage using its key.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name    | Type   | Required | Description                              |
|---------|--------|----------|------------------------------------------|
| key     | str    | ✅        | The key to retrieve                      |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The retrieved value                         |
| false_path  | dict      | Error if key not found or retrieval fails   |

---

## ✅ Example

### Retrieve User Preference:
```json
{
  "key": "theme"
}
```
**Output:** `"dark"` (if previously stored)

### Key Not Found:
```json
{
  "key": "non_existent_key"
}
```
**Output (false_path):** `{"error": "Key 'non_existent_key' not found"}`

---

## 🔒 Security Features

- **Automatic Isolation**: Only retrieves values from current tenant/project
- **Access Control**: Verifies ownership before returning values
- **Environment Requirements**: Requires `TENANT_ID` and `PROJECT_ID`

---

## 💡 Use Cases

- Retrieve user preferences
- Load cached configuration
- Access session or state data
- Fetch previously stored values

---

## ⚠️ Notes

- Returns error if key doesn't exist (triggers `false_path`)
- Security check ensures values belong to current tenant/project
- Keys support placeholder replacement
- Returns stored value as-is (string format)
