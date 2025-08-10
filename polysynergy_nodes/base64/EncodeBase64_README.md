# Encode Base64

Encodes a raw value into Base64 format.  
Useful for preparing data for transmission, storage, or embedding in text-based formats.

## **Category:** Encoding

## **Description**
The **Encode Base64** node transforms a raw byte input into a Base64-encoded string.

It supports:
- Binary or string input (as bytes or string)
- Encodes to standard Base64
- Graceful error handling for unexpected input issues

## **Variables**

| Name    | Type        | Input | Output | Description |
|---------|-------------|-------|--------|-------------|
| `value` | str \| bytes | ✅     | ❌      | The raw value to encode in Base64. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered if encoding succeeds. Contains the Base64 string. |
| `false_path` | Triggered if encoding fails. Contains an error dictionary. |

## **How It Works**
1. Accepts raw input (`value`) as either string or bytes.
2. If input is a string, it's automatically converted to bytes using UTF-8 encoding.
3. Encodes the bytes using Python's built-in `base64.b64encode`.
4. If successful:
   - Emits the result as a Base64 string to `true_path`.
5. If encoding fails:
   - Sends a descriptive error to `false_path`.

---

## **Example Usage**

### **Input**
- `value` = `b"Hello World!"`

### **Output (success)**
- `true_path` = `"SGVsbG8gV29ybGQh"`

### **Output (invalid input)**
- `false_path`:
```json
{
  "error": "a bytes-like object is required, not 'str'"
}
```

---

## **Error Handling**
- If the input is not bytes → `false_path` contains a Python error message.
- Unexpected exceptions are returned with minimal detail for clarity.

---

## **Use Cases**
✔ Preparing data for APIs that expect Base64  
✔ Encoding binary payloads for safe transmission  
✔ Storing binary data in text-friendly formats

---

📤 **Use this node when you need to encode binary or raw content to Base64.**