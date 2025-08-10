# String to Int

Converts string representations of numbers to integer values.  
Essential for processing user input, form data, and numeric strings from external sources.

## **Category:** Cast

## **Description**
The **String to Int** node converts string representations of integers to Python integer objects with robust error handling.

It supports:
- Integer strings (positive and negative)
- Whitespace trimming
- Type coercion from float and other numeric types
- Comprehensive validation and error reporting

## **Variables**

| Name          | Type | Input | Output | Description |
|---------------|------|-------|--------|-------------|
| `input_value` | str  | ✅     | ❌      | The string representation of an integer. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when conversion succeeds. Contains the integer value. |
| `false_path` | Triggered when conversion fails. Contains error information. |

## **How It Works**
1. Receives string input via `input_value`.
2. Strips leading/trailing whitespace.
3. Attempts conversion using Python's `int()` function.
4. Handles numeric types by converting to int directly.
5. On success:
   - Sends integer value to `true_path`.
6. On failure:
   - Sends detailed error information to `false_path`.

---

## **Example Usage**

### **Input (positive integer)**
- `input_value` = `"123"`

### **Output (success)**
- `true_path` = `123`

### **Input (negative integer)**
- `input_value` = `"-456"`

### **Output (success)**
- `true_path` = `-456`

### **Input (with whitespace)**
- `input_value` = `"  789  "`

### **Output (success)**
- `true_path` = `789`

### **Input (zero)**
- `input_value` = `"0"`

### **Output (success)**
- `true_path` = `0`

### **Input (float to int)**
- `input_value` = `12.7`

### **Output (success)**
- `true_path` = `12` (truncated)

### **Output (error - invalid format)**
- `false_path`:
```json
{
  "error": "Invalid integer format: invalid literal for int() with base 10: 'not_a_number'"
}
```

### **Output (error - float string)**
- `false_path`:
```json
{
  "error": "Invalid integer format: invalid literal for int() with base 10: '12.34'"
}
```

---

## **Error Handling**
- Invalid number format → `false_path` with format error
- Float strings (like "12.34") → `false_path` with parsing error
- Empty strings → `false_path` with appropriate error
- Non-numeric content → `false_path` with validation error

---

## **Use Cases**
✔ Processing form input fields  
✔ Converting user-provided numeric data  
✔ Parsing configuration values  
✔ Handling API parameters  
✔ Converting database string fields to integers

---

🔢 **Use this node when you need to convert string representations to integer values with validation.**