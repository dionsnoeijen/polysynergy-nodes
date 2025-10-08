# KeyValue - Set Value

Stores a single key-value pair in persistent storage.
Perfect for beginners who want to save simple values like usernames, settings, or timestamps.

## **Category:** Persistent

## **Description**
The **KeyValue - Set Value** node stores a key and value in DynamoDB-backed persistent storage.
It's the easiest way to remember data between workflow executions without needing to worry about collections or categories.

Supports:
- Multi-line values via textarea
- Automatic tenant/project isolation for security
- Simple key-value storage without complexity

## **Variables**

| Name    | Type | Input | Output | Description |
|---------|------|-------|--------|-------------|
| `key`   | str  | ✅     | ❌      | The key to store (e.g. 'theme', 'username', 'last_login'). |
| `value` | str  | ✅     | ❌      | The value to store. Supports multi-line input (textarea). |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Contains the stored value on success. |
| `false_path` | Contains error info if the operation failed. |

## **How It Works**
1. Connects to the DynamoDB key-value store.
2. Creates a secure storage key using your tenant/project ID.
3. Stores the key-value pair in the "simple" collection.
4. On success:
   - Returns the stored value via `true_path`.
5. On failure:
   - Returns error details via `false_path`.

---

## **Example Usage**

### **Input**
- `key` = `"user_theme"`
- `value` = `"dark"`

### **Output (success)**
- `true_path` = `"dark"`

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
✔ Storing user preferences (theme, language, settings)
✔ Saving last execution timestamps
✔ Persisting simple configuration values
✔ Creating feature flags or toggle switches
✔ Storing usernames, API keys, or other simple data

---

🚀 **The easiest way to make your workflow remember something — no complexity, just simple key-value storage.**