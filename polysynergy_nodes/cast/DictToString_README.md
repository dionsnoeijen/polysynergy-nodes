# Dict to String

Converts a Python dictionary to a JSON string representation.  
Essential for serializing data for APIs, storage, or transmission.

## **Category:** Cast

## **Description**
The **Dict to String** node converts Python dictionaries and other JSON-serializable objects to properly formatted JSON strings.

It supports:
- Dictionary objects
- Nested data structures
- Lists and arrays
- Unicode characters (preserved)
- Comprehensive serialization error handling

## **Variables**

| Name          | Type | Input | Output | Description |
|---------------|------|-------|--------|-------------|
| `input_value` | dict | ✅     | ❌      | The dictionary to convert to JSON string. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when serialization succeeds. Contains the JSON string. |
| `false_path` | Triggered when serialization fails. Contains error information. |

## **How It Works**
1. Receives dictionary input via `input_value`.
2. Serializes using Python's `json.dumps()` with `ensure_ascii=False`.
3. Preserves Unicode characters in output.
4. On success:
   - Sends JSON string to `true_path`.
5. On failure:
   - Sends error details to `false_path`.

---

## **Example Usage**

### **Input (simple dict)**
- `input_value` = `{"name": "John", "age": 30}`

### **Output (success)**
- `true_path` = `'{"name": "John", "age": 30}'`

### **Input (nested dict)**
- `input_value` = `{"user": {"name": "John", "details": {"age": 30}}}`

### **Output (success)**
- `true_path` = `'{"user": {"name": "John", "details": {"age": 30}}}'`

### **Input (with Unicode)**
- `input_value` = `{"greeting": "Hello 世界", "emoji": "🌍"}`

### **Output (success)**
- `true_path` = `'{"greeting": "Hello 世界", "emoji": "🌍"}'`

### **Input (with lists)**
- `input_value` = `{"items": ["apple", "banana"], "count": 2}`

### **Output (success)**
- `true_path` = `'{"items": ["apple", "banana"], "count": 2}'`

### **Output (error)**
- `false_path`:
```json
{
  "error": "Object not JSON serializable: Object of type set is not JSON serializable"
}
```

---

## **Error Handling**
- Non-serializable objects → `false_path` with specific error details
- Circular references → `false_path` with circular reference error
- Other serialization issues → `false_path` with error message

---

## **Use Cases**
✔ Preparing data for API requests  
✔ Serializing configuration objects  
✔ Converting data for storage  
✔ Formatting data for webhooks  
✔ Creating JSON responses

---

📦 **Use this node when you need to convert structured data to JSON strings for transmission or storage.**