# KeyValue - Get Value

Retrieves a single value from persistent storage by key.
The perfect companion to "KeyValue - Set Value" for reading saved data like settings, usernames, or timestamps.

## **Category:** Persistent

## **Description**
The **KeyValue - Get Value** node fetches a value based on a given key from DynamoDB-backed persistent storage.
It's designed for simplicity - just provide a key and get your stored value back.

Supports:
- Simple key-based retrieval
- Automatic tenant/project isolation for security
- Clear error messages when keys don't exist

This node is ideal for reading preferences, configuration values, or any simple data you've previously stored.

## **Variables**

| Name  | Type | Input | Output | Description |
|-------|------|-------|--------|-------------|
| `key` | str  | ✅     | ❌      | The key to retrieve (e.g. 'theme', 'username', 'last_login'). |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Contains the retrieved value if the key exists. |
| `false_path` | Contains error info if the key doesn't exist or another error occurred. |

## **How It Works**
1. Connects to the DynamoDB key-value store.
2. Creates a secure lookup key using your tenant/project ID.
3. Searches for the key in the "simple" collection.
4. If found:
   - Returns the stored value via `true_path`.
5. If not found or error occurs:
   - Returns error details via `false_path`.

---

## **Example Usage**

### **Input**
- `key` = `"user_theme"`

### **Output (success)**
- `true_path` = `"dark"`

### **Output (key not found)**
- `false_path`:
```json
{
  "error": "Key 'user_theme' not found"
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
- Key doesn't exist → `false_path` with "not found" message.
- Key exists but has no value → `false_path` with "no value" message.
- Missing environment variables → `false_path` with clear error message.
- All unexpected exceptions are logged with full trace in `false_path`.

---

## **Use Cases**
✔ Reading user preferences (theme, language, settings)
✔ Checking last execution timestamps
✔ Loading simple configuration values
✔ Reading feature flags or toggle switches
✔ Retrieving usernames, API keys, or other stored data

---

🔍 **The easiest way to retrieve data your workflow remembered — just ask for it by key.**