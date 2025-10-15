# 🔑 KeyValue - Get All Keys Node

The `KeyValue - Get All Keys` node retrieves a list of all keys in a collection without fetching their values.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name to list keys from        |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | JSON array of all keys                      |
| false_path  | dict      | Error if collection empty or access fails   |

---

## ✅ Examples

### List All Keys:
```json
{
  "collection": "user_settings"
}
```
**Output:** `["theme", "language", "notification_enabled", "timezone"]`

### Empty Collection:
```json
{
  "collection": "empty_collection"
}
```
**Output (false_path):** `{"error": "Collection 'empty_collection' is empty or does not exist"}`

---

## 📊 Output Format

Returns a JSON-formatted array of key names:
```json
["key1", "key2", "key3", "key4"]
```

Can be parsed with `StringToDict` or used with `List Loop` node for iteration.

---

## 💡 Use Cases

- List all available settings in a collection
- Iterate over collection keys for batch processing
- Audit what keys are stored
- Display available options to users
- Check collection contents without loading values

---

## 🔒 Security Features

- **Tenant Filtering**: Only returns keys from current tenant/project
- **Minimal Data Transfer**: Fetches only keys, not values
- **Ownership Verification**: Filters out keys from other tenants

---

## ⚠️ Notes

- Returns only key names, not their values (efficient for large collections)
- Output is JSON array format as string
- Empty collections trigger `false_path`
- Keys are filtered by tenant/project ownership
