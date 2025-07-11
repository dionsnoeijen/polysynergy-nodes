# KeyValueStore - Set

Stores a key-value pair in a DynamoDB-backed store.  
Useful for persisting values across flows, such as timestamps, flags, or other dynamic data.

## **Category:** Persistent

## **Description**
The **KeyValueStore - Set** node writes a key and value to a DynamoDB table.  
It is part of a simple persistent storage mechanism for use in PolySynergy workflows.

Supports:
- Custom table names (default: `KeyValueStore`)
- Optional multi-line input via text area (for values)

## **Variables**

| Name         | Type | Input | Output | Description |
|--------------|------|-------|--------|-------------|
| `table_name` | str  | ✅     | ❌      | Name of the DynamoDB table to write to (default is `"KeyValueStore"`). |
| `key`        | str  | ✅     | ❌      | The key under which the value should be stored. |
| `value`      | str  | ✅     | ❌      | The value to be stored. Supports multi-line input (textarea). |

## **Flow Control**

| Name         | Description                                      |
|--------------|--------------------------------------------------|
| `true_path`  | If succesful it contains the value that was set. |
| `false_path` | Contains error info if the operation failed.     |

## **How It Works**
1. Connects to the specified DynamoDB table.
2. Executes a `put_item()` with the `Key` and `Value`.
3. On success:
   - A confirmation message is sent to `true_path`.
4. On failure:
   - The error is passed to `false_path`, including traceback details if unexpected.

---

## **Example Usage**

### **Input**
- `table_name` = `"KeyValueStore"`
- `key` = `"last_checked_at"`
- `value` = `"2025-04-07T15:00:00Z"`

### **Output**
- `true_path` = `"Stored key 'last_checked_at' successfully."`

---

## **Error Handling**
- If the table doesn't exist → `false_path` contains a `ResourceNotFoundException`.
- All unexpected exceptions → `false_path` with traceback for debugging.

---

## **Use Cases**
✔ Persisting last execution timestamps  
✔ Saving configuration overrides  
✔ Writing status flags between workflows  
✔ Setting debug or toggle switches

---

💾 **This node lets your flow remember things — across executions, schedules, or different parts of your system.**
