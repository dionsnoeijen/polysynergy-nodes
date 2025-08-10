# Bytes to String

Converts bytes data to a UTF-8 string representation.  
Essential for handling binary data from files, network responses, or encoded content.

## **Category:** Cast

## **Description**
The **Bytes to String** node converts bytes objects to readable string format using UTF-8 encoding.

It supports:
- Raw bytes input (preferred)
- Automatic fallback for other data types
- Proper UTF-8 decoding
- Graceful error handling for encoding issues

## **Variables**

| Name          | Type  | Input | Output | Description |
|---------------|-------|-------|--------|-------------|
| `input_value` | bytes | ✅     | ❌      | The bytes data to convert to string. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when conversion succeeds. Contains the decoded string. |
| `false_path` | Triggered when conversion fails. Contains error information. |

## **How It Works**
1. Receives bytes input via `input_value`.
2. If input is bytes, decodes using UTF-8 encoding.
3. If input is another type, converts to string using `str()`.
4. On success:
   - Sends decoded string to `true_path`.
5. On failure:
   - Sends error details to `false_path`.

---

## **Example Usage**

### **Input (bytes)**
- `input_value` = `b"Hello World"`

### **Output (success)**
- `true_path` = `"Hello World"`

### **Input (UTF-8 bytes)**
- `input_value` = `"Hello 世界".encode("utf-8")`

### **Output (success)**  
- `true_path` = `"Hello 世界"`

### **Output (error)**
- `false_path`:
```json
{
  "error": "codec can't decode byte..."
}
```

---

## **Error Handling**
- Invalid UTF-8 sequences → `false_path` with decoding error
- Unexpected exceptions → `false_path` with error message

---

## **Use Cases**
✔ Decoding API response bodies  
✔ Converting file contents to readable text  
✔ Processing binary data from external sources  
✔ Handling encoded webhook payloads

---

🔤 **Use this node when you need to convert bytes data to readable strings.**