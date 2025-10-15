# ✅ KeyValue - Check Collection Node

The `KeyValue - Check Collection` node checks if a key exists within a specific collection without retrieving its value.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name to check in              |
| key         | str    | ✅        | The key to check for                     |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | bool      | True if key exists in collection            |
| false_path  | bool      | False if key doesn't exist                  |

---

## ✅ Examples

### Check for Existing Key:
```json
{
  "collection": "user_settings",
  "key": "theme"
}
```
**Output:** `true` (if key exists)

### Check Non-existent Key:
```json
{
  "collection": "api_credentials",
  "key": "missing_token"
}
```
**Output (false_path):** `false`

---

## 🔀 Flow Control Pattern

```
Check Collection → [exists?]
├─ true_path → Update existing value
└─ false_path → Create new value
```

---

## 💡 Use Cases

- Validate collection item exists before update
- Conditional logic based on key presence
- Guard against missing configuration
- Check if API credentials are configured

---

## ⚠️ Notes

- Returns `false` for non-existent keys (not an error)
- Efficient check - only fetches minimal data
- Security check ensures key belongs to current tenant/project
- Does not return the actual value
