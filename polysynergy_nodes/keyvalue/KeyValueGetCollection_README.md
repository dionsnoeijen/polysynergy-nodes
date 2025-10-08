# KeyValue - Get Collection

Retrieves a value from a specific collection in persistent storage.
Advanced version that lets you read organized data from categories like 'google_drive_files', 'user_settings', or 'cache_data'.

## **Category:** Persistent

## **Description**
The **KeyValue - Get Collection** node fetches a value based on a collection and key from DynamoDB-backed persistent storage.
This allows you to retrieve data from organized collections, keeping different types of data separated and easy to manage.

Supports:
- Collection-based data organization
- Automatic tenant/project isolation for security
- Clear error messages for missing keys or collections
- Perfect for complex workflows with multiple data categories

## **Variables**

| Name         | Type | Input | Output | Description |
|--------------|------|-------|--------|-------------|
| `collection` | str  | ✅     | ❌      | The category/collection name to search in. |
| `key`        | str  | ✅     | ❌      | The key to retrieve. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Contains the retrieved value if the key exists in the collection. |
| `false_path` | Contains error info if the key doesn't exist or another error occurred. |

## **How It Works**
1. Connects to the DynamoDB key-value store.
2. Creates a secure lookup key using tenant/project/collection.
3. Searches for the key within the specified collection.
4. If found:
   - Returns the stored value via `true_path`.
5. If not found or error occurs:
   - Returns error details via `false_path`.

---

## **Example Usage**

### **Check Google Drive File Status**
- `collection` = `"drive_files"`
- `key` = `"file_abc123"`

**Output (success):**
- `true_path` = `"processed"`

### **Get User Setting**
- `collection` = `"user_settings"`
- `key` = `"notification_email"`

**Output (success):**
- `true_path` = `"user@example.com"`

### **Output (key not found)**
- `false_path`:
```json
{
  "error": "Key 'file_abc123' not found in collection 'drive_files'"
}
```

### **Output (system error)**
- `false_path`:
```json
{
  "error": "Missing tenant_id or project_id in environment"
}
```

---

## **Error Handling**
- Key doesn't exist in collection → `false_path` with specific error message.
- Key exists but has no value → `false_path` with "no value" message.
- Access denied (security) → `false_path` with access denied error.
- All unexpected exceptions are logged with full trace in `false_path`.

---

## **Use Cases**
✔ Check Google Drive file processing status
✔ Read user preferences by category
✔ Retrieve cached API responses
✔ Get feature flag settings
✔ Load configuration values by environment
✔ Query complex workflow state

---

## **Common Collection Patterns**
- `"drive_files"` + `"file_123"` → Get file processing status
- `"user_settings"` + `"theme"` → Get user's theme preference
- `"cache_data"` + `"api_response_users"` → Get cached API data
- `"feature_flags"` + `"new_feature_enabled"` → Check if feature is on

---

🎯 **Precisely retrieve your organized data — know exactly where to look and what you'll find.**