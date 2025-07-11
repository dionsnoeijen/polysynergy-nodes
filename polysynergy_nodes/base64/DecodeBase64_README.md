# Decode Base64

Decodes a Base64-encoded string into its original form.  
Useful for decoding API responses, form submissions, or other base64-encoded data.

## **Category:** Decode

## **Description**
The **Decode Base64** node converts a Base64-encoded string (or byte input) into its original value.

It supports:
- Raw byte input or encoded strings
- Output as decoded string
- Graceful error handling if the input is not valid Base64

## **Variables**

| Name    | Type  | Input | Output | Description |
|---------|-------|-------|--------|-------------|
| `value` | bytes | ✅     | ❌      | The base64-encoded value to decode. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered if decoding succeeds. Contains the decoded value as a string. |
| `false_path` | Triggered if decoding fails. Contains an error dictionary. |

## **How It Works**
1. Accepts an encoded input (`value`).
2. Attempts to decode it using Python’s built-in `base64.b64decode`.
3. If successful:
   - Emits the result to `true_path`.
4. If decoding fails:
   - Sends a descriptive error to `false_path`.

---

## **Example Usage**

### **Input**
- `value` = `"SGVsbG8gV29ybGQh"`

### **Output (success)**
- `true_path` = `"Hello World!"`

### **Output (invalid input)**
- `false_path`:
```json
{
  "error": "Incorrect padding"
}
```

---

## **Error Handling**
- If the input is not valid Base64 → `false_path` contains a Python error message.
- Unexpected exceptions are returned with minimal detail for clarity.

---

## **Use Cases**
✔ Decoding webhook payloads  
✔ Handling base64-formatted uploads or content  
✔ Processing encoded data across flows

---

🔓 **Use this node when you need to decode base64 strings or binary data in your workflows.**