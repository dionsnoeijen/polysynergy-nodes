# File Type

Determines the file type based on a file's extension.

## **Category:** File

## **Description**
The **File Type** node extracts the file extension from a given filename and outputs it.  
This can be used to determine how a file should be handled in a flow.

If the filename does not contain an extension, the node routes to `false_path`.

## **Variables**

| Name       | Type | Input | Output | Description |
|------------|------|-------|--------|-------------|
| `filename` | str  | ✅     | ❌      | The name of the file, including its extension. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Contains the file extension if it could be extracted. |
| `false_path` | Triggered if the filename has no extension or is empty. Contains an error dict. |

## **How It Works**
1. Checks whether the filename is valid and contains a dot.
2. If so, extracts the extension after the last dot.
3. If not, sends an error to `false_path`.

---

## **Example Usage**

### **Input**
- `filename` = `"report.pdf"`

### **Output**
- `true_path` = `"pdf"`

---

### **Input**
- `filename` = `"untitled"`

### **Output**
- `false_path`:
```json
{
  "error": "Filename does not contain an extension."
}
```

---

## **Error Handling**
- Missing or invalid filename triggers `false_path`.
- Extensions are extracted using string manipulation.

---

## **Use Cases**
✔ Determining how to parse or process uploaded files  
✔ Routing files to different nodes based on type  
✔ Validating that file inputs are correctly formatted

---

📂 **Use this node to extract and respond to file types dynamically within your flow.**