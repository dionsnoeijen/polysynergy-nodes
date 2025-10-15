# 💾 HTML to PDF (Save to File) Node

The `HTML to PDF (Save to File)` node converts HTML content into a PDF file saved to disk, returning the file path for further processing.

---

## 📂 Category

**pdf**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| html_input  | str    | ✅        | Raw HTML to convert to PDF               |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | File path to generated PDF                  |
| false_path  | dict      | Error if conversion fails                   |

---

## ✅ Examples

### Generate Invoice:
```json
{
  "html_input": "<html><body><h1>Invoice #12345</h1><p>Amount Due: $250</p></body></html>"
}
```
**Output:** `"/tmp/tmpXYZ123.pdf"` (temporary file path)

---

## 🎯 Common Use Cases

### File Storage:
```
Generate HTML → HTML to PDF (File) → Upload to S3/Storage
```

### File Processing Chain:
```
HTML to PDF (File) → OCR Processing → Text Extraction
```

### Archive Generation:
```
Report Data → Format HTML → HTML to PDF (File) → Archive Storage
```

---

## 📁 File Management

- **Temporary Files**: Creates temporary PDF with unique name
- **Auto-naming**: Automatically generates `.pdf` extension
- **Persistence**: File persists until explicitly deleted
- **Location**: Saved to system temp directory

---

## 💡 Features

- **File-based**: Returns path to physical file
- **No Memory Limits**: Suitable for large documents
- **Reusable**: File can be read multiple times
- **CSS Support**: Supports inline and embedded CSS

---

## ⚠️ Notes

- File is created in system temp directory
- File persists after node execution (manual cleanup may be needed)
- Returns absolute file path
- Requires valid HTML structure
- For in-memory PDF (bytes), use "HTML to PDF (Bytes)" instead
