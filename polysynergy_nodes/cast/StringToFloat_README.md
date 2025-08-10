# String to Float

Converts string representations of numbers to floating-point values.  
Essential for processing decimal numbers, scientific notation, and precise numeric data.

## **Category:** Cast

## **Description**
The **String to Float** node converts string representations of floating-point numbers to Python float objects with comprehensive format support.

It supports:
- Decimal numbers (positive and negative)
- Integer strings (converted to float)
- Scientific notation (e.g., "1.23e-4")
- Whitespace trimming
- Type coercion from numeric types

## **Variables**

| Name          | Type | Input | Output | Description |
|---------------|------|-------|--------|-------------|
| `input_value` | str  | ✅     | ❌      | The string representation of a floating-point number. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when conversion succeeds. Contains the float value. |
| `false_path` | Triggered when conversion fails. Contains error information. |

## **How It Works**
1. Receives string input via `input_value`.
2. Strips leading/trailing whitespace.
3. Attempts conversion using Python's `float()` function.
4. Handles existing numeric types by converting to float.
5. On success:
   - Sends float value to `true_path`.
6. On failure:
   - Sends detailed error information to `false_path`.

---

## **Example Usage**

### **Input (decimal number)**
- `input_value` = `"123.45"`

### **Output (success)**
- `true_path` = `123.45`

### **Input (negative decimal)**
- `input_value` = `"-456.78"`

### **Output (success)**
- `true_path` = `-456.78`

### **Input (integer string)**
- `input_value` = `"123"`

### **Output (success)**
- `true_path` = `123.0`

### **Input (scientific notation)**
- `input_value` = `"1.23e-4"`

### **Output (success)**
- `true_path` = `0.000123`

### **Input (with whitespace)**
- `input_value` = `"  789.12  "`

### **Output (success)**
- `true_path` = `789.12`

### **Input (zero)**
- `input_value` = `"0.0"`

### **Output (success)**
- `true_path` = `0.0`

### **Output (error - invalid format)**
- `false_path`:
```json
{
  "error": "Invalid float format: could not convert string to float: 'not_a_number'"
}
```

### **Output (error - multiple dots)**
- `false_path`:
```json
{
  "error": "Invalid float format: could not convert string to float: '12.34.56'"
}
```

---

## **Error Handling**
- Invalid number format → `false_path` with format error
- Multiple decimal points → `false_path` with parsing error
- Empty strings → `false_path` with appropriate error
- Non-numeric content → `false_path` with validation error
- Malformed scientific notation → `false_path` with format error

---

## **Use Cases**
✔ Processing form input with decimal values  
✔ Converting measurement data  
✔ Parsing scientific or financial data  
✔ Handling API numeric parameters  
✔ Converting configuration values with precision  
✔ Processing sensor readings

---

🎯 **Use this node when you need to convert string representations to floating-point values with precision.**