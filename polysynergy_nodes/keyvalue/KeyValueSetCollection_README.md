# KeyValue - Set Collection

Stores a key-value pair within a specific collection in persistent storage.
Advanced version that lets you organize data into categories like 'google_drive_files', 'user_settings', or 'cache_data'.

## **Category:** Persistent

## **Description**
The **KeyValue - Set Collection** node stores a key and value within a named collection in DynamoDB-backed persistent storage.
This allows you to organize your data into logical groups and prevents key collisions between different types of data.

Supports:
- Collection-based organization (categories)
- Multi-line values via textarea
- Automatic tenant/project isolation for security
- Perfect for complex workflows with multiple data types

## **Variables**

| Name         | Type | Input | Output | Description |
|--------------|------|-------|--------|-------------|
| `collection` | str  | ✅     | ❌      | The category/collection name (e.g. 'google_drive_files', 'user_settings'). |
| `key`        | str  | ✅     | ❌      | The unique key within this collection. |
| `value`      | str  | ✅     | ❌      | The value to store. Supports multi-line input (textarea). |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Contains the stored value on success. |
| `false_path` | Contains error info if the operation failed. |

## **How It Works**
1. Connects to the DynamoDB key-value store.
2. Creates a secure storage key using tenant/project/collection.
3. Stores the key-value pair within the specified collection.
4. On success:
   - Returns the stored value via `true_path`.
5. On failure:
   - Returns error details via `false_path`.

---

## **Example Usage**

### **Google Drive File Tracking**
- `collection` = `"drive_files"`
- `key` = `"file_abc123"`
- `value` = `"processed"`

### **User Preferences**
- `collection` = `"user_settings"`
- `key` = `"notification_email"`
- `value` = `"user@example.com"`

### **Output (success)**
- `true_path` = `"processed"`

### **Output (error)**
- `false_path`:
```json
{
  "error": "Missing tenant_id or project_id in environment"
}
```

---

## **Error Handling**
- Missing environment variables → `false_path` with clear error message.
- DynamoDB connection issues → `false_path` with connection error.
- All unexpected exceptions are logged with full trace in `false_path`.

---

## **Use Cases**
✔ Google Drive file processing status tracking
✔ Organizing user settings by category
✔ Cache data with expiration tracking
✔ API response storage by endpoint
✔ Multi-tenant data organization
✔ Complex workflow state management

---

## **Collection Examples**
- `"drive_files"` → Track file processing status
- `"user_preferences"` → Store user settings
- `"cache_data"` → Temporary data storage
- `"api_responses"` → Cache API calls
- `"feature_flags"` → Environment-specific toggles

---

🗂️ **Organize your persistent data like a pro — keep different types of data in their own collections.**