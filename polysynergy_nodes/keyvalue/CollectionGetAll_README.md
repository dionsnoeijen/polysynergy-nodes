# 📋 KeyValue - Get All Collection Node

The `KeyValue - Get All Collection` node retrieves all key-value pairs from a collection as a JSON object.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name to retrieve              |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | JSON string of all key-value pairs          |
| false_path  | dict      | Error if collection empty or access fails   |

---

## ✅ Examples

### Retrieve All User Settings:
```json
{
  "collection": "user_settings"
}
```
**Output:**
```json
{
  "theme": "dark",
  "language": "en",
  "notification_enabled": "true"
}
```

### Empty Collection:
```json
{
  "collection": "empty_collection"
}
```
**Output (false_path):** `{"error": "Collection 'empty_collection' is empty or does not exist"}`

---

## 📊 Output Format

Returns a JSON-formatted string with all key-value pairs:
```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": "value3"
}
```

Can be parsed with `StringToDict` or `JSON Parse` nodes for further processing.

---

## 🔒 Security Features

- **Tenant Filtering**: Only returns items from current tenant/project
- **Ownership Verification**: Filters out items from other tenants
- **Secure Query**: Uses DynamoDB query with proper isolation

---

## 💡 Use Cases

- Export all settings from a collection
- Backup collection data
- Audit stored values
- Batch process all items in a collection
- Display configuration overview

---

## ⚠️ Notes

- Returns formatted JSON string (with indentation)
- Only includes items owned by current tenant/project
- Empty collections trigger `false_path`
- Large collections may have significant data transfer
