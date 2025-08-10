# String to Dict

Parses a JSON string into a Python dictionary.  
Essential for processing API responses, configuration data, and structured text content.

## **Category:** Cast

## **Description**
The **String to Dict** node converts JSON-formatted strings to Python dictionaries using secure JSON parsing.

It supports:
- Valid JSON object strings
- JSON arrays (converted to lists)
- Nested JSON structures
- Whitespace handling
- Comprehensive error reporting for invalid JSON

## **Variables**

| Name          | Type | Input | Output | Description |
|---------------|------|-------|--------|-------------|
| `input_value` | str  | ✅     | ❌      | The JSON string to parse into a dictionary. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when JSON parsing succeeds. Contains the parsed dictionary/list. |
| `false_path` | Triggered when JSON parsing fails. Contains error information. |

## **How It Works**
1. Receives JSON string input via `input_value`.
2. Strips whitespace and validates JSON format.
3. Parses using Python's built-in `json.loads()`.
4. On success:
   - Sends parsed data structure to `true_path`.
5. On failure:
   - Sends detailed error information to `false_path`.

---

## **Example Usage**

### **Input (JSON object)**
- `input_value` = `'{"name": "John", "age": 30}'`

### **Output (success)**
- `true_path` = `{"name": "John", "age": 30}`

### **Input (JSON array)**
- `input_value` = `'["apple", "banana", "cherry"]'`

### **Output (success)**
- `true_path` = `["apple", "banana", "cherry"]`

### **Input (nested JSON)**
- `input_value` = `'{"user": {"name": "John", "details": {"age": 30}}}'`

### **Output (success)**
- `true_path` = `{"user": {"name": "John", "details": {"age": 30}}}`

### **Output (error)**
- `false_path`:
```json
{
  "error": "Invalid JSON: Expecting ':' delimiter: line 1 column 15 (char 14)"
}
```

---

## **Error Handling**
- Invalid JSON syntax → `false_path` with detailed parsing error
- Empty strings → `false_path` with appropriate error message
- Malformed JSON → `false_path` with position information

---

## **Use Cases**
✔ Processing API response data  
✔ Parsing configuration files  
✔ Converting JSON webhooks to usable data  
✔ Handling user input JSON  
✔ Processing stored JSON settings

---

🔧 **Use this node when you need to convert JSON strings to structured data for processing.**