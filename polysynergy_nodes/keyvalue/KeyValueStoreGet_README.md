# KeyValueStore - Get

Retrieves a stored value from a key-value store (DynamoDB-based).  
Used to persist simple values across executions or between schedules.

## **Category:** Persistent

## **Description**
The **KeyValueStore - Get** node fetches a value based on a given key from a DynamoDB-backed key-value store.

It supports:
- Custom table names (default: `KeyValueStore`)
- Error handling if the key does not exist or the table is missing

This node is useful for reading state, flags, timestamps, or other persisted values across flows.

## **Variables**

| Name         | Type | Input | Output | Description |
|--------------|------|-------|--------|-------------|
| `table_name` | str  | ✅     | ❌      | Name of the DynamoDB table to read from (default is `"KeyValueStore"`). |
| `key`        | str  | ✅     | ❌      | The key to look up in the key-value store. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered if a value was successfully retrieved. Will contain the value as a string. |
| `false_path` | Triggered if the key does not exist or another error occurred. Will contain an error dictionary. |

## **How It Works**
1. Connects to the configured DynamoDB table.
2. Looks for the item with the specified key (`Key`).
3. If found:
   - Sends the value to `true_path`.
4. If not found or the value is missing:
   - Sends an error to `false_path`.
5. Errors such as missing tables or unexpected issues are caught and passed as detailed error messages.

---

## **Example Usage**

### **Input**
- `table_name` = `"KeyValueStore"`
- `key` = `"last_checked_at"`

### **Output (success)**
- `true_path` = `"2025-04-07T15:00:00Z"`

### **Output (missing key)**
- `false_path`:
```json
{
  "error": "Key 'last_checked_at' not found or has no value."
}
```

---

## **Error Handling**
- If the table doesn't exist → `false_path` contains AWS error message.
- If the key exists but the value is missing or `None` → triggers `false_path`.
- All unexpected exceptions are logged with full trace in `false_path`.

---

## **Use Cases**
✔ Storing and checking last execution times  
✔ Reading flags or feature toggles across flows  
✔ Creating persistent "memory" in otherwise stateless nodes

---

🔑 **Use this node when your flows need to remember something between executions.**
