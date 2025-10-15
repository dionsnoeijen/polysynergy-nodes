# 🧹 KeyValue - Clear Collection Node

The `KeyValue - Clear Collection` node deletes all items from a collection, effectively clearing it completely.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name to clear                 |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | Confirmation with count of removed items    |
| false_path  | dict      | Error if collection empty or clear fails    |

---

## ✅ Examples

### Clear Collection:
```json
{
  "collection": "temp_cache"
}
```
**Output:** `"Removed all 15 items from collection 'temp_cache'"`

### Empty Collection:
```json
{
  "collection": "already_empty"
}
```
**Output (false_path):** `{"error": "Collection 'already_empty' is empty or does not exist"}`

---

## ⚙️ How It Works

1. Queries all items in the collection
2. Verifies ownership for each item
3. Deletes items in batches (efficient bulk deletion)
4. Returns count of removed items

---

## ⚠️ **DANGER ZONE**

This operation is **irreversible**:
- Deletes **ALL** items in the collection
- Cannot be undone
- No confirmation prompt
- Use with extreme caution

---

## 🔒 Security Features

- **Tenant Isolation**: Only deletes items from current tenant/project
- **Batch Deletion**: Uses DynamoDB batch writer for efficiency
- **Ownership Verification**: Filters out items from other tenants

---

## 💡 Use Cases

- Clear temporary cache collection
- Reset user session data
- Clean up test data
- Remove all expired items
- Reset feature-specific storage

---

## ⚠️ Notes

- Deletes **all** items - use `Remove Collection` for single items
- Returns error if collection doesn't exist or is empty
- Batch deletion handles large collections efficiently
- Collection structure remains (only data is deleted)
