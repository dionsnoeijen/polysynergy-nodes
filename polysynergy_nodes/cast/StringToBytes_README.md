# String to Bytes

Converts string data to bytes using UTF-8 encoding.  
Essential for preparing text data for binary operations, file writing, or network transmission.

## **Category:** Cast

## **Description**
The **String to Bytes** node converts string objects to bytes format using UTF-8 encoding.

It supports:
- String input (preferred)
- Bytes passthrough (already converted)
- Automatic conversion for other data types
- UTF-8 encoding for universal compatibility

## **Variables**

| Name          | Type | Input | Output | Description |
|---------------|------|-------|--------|-------------|
| `input_value` | str  | ✅     | ❌      | The string data to convert to bytes. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when conversion succeeds. Contains the encoded bytes. |
| `false_path` | Triggered when conversion fails. Contains error information. |

## **How It Works**
1. Receives string input via `input_value`.
2. If input is string, encodes using UTF-8.
3. If input is already bytes, passes through unchanged.
4. If input is another type, converts to string first, then to bytes.
5. On success:
   - Sends encoded bytes to `true_path`.
6. On failure:
   - Sends error details to `false_path`.

---

## **Example Usage**

### **Input (string)**
- `input_value` = `"Hello World"`

### **Output (success)**
- `true_path` = `b"Hello World"`

### **Input (Unicode string)**
- `input_value` = `"Hello 世界"`

### **Output (success)**
- `true_path` = `b"Hello \xe4\xb8\x96\xe7\x95\x8c"` (UTF-8 encoded)

### **Output (error)**
- `false_path`:
```json
{
  "error": "encoding error message"
}
```

---

## **Error Handling**
- Encoding errors → `false_path` with encoding error details
- Unexpected exceptions → `false_path` with error message

---

## **Use Cases**
✔ Preparing strings for file writing  
✔ Encoding data for HTTP requests  
✔ Converting text for binary protocols  
✔ Processing data for hash functions  
✔ Preparing content for Base64 encoding

---

📝 **Use this node when you need to convert strings to bytes for binary operations.**