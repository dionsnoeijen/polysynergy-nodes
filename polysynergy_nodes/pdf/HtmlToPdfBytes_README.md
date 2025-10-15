# 📄 HTML to PDF (Bytes) Node

The `HTML to PDF (Bytes)` node converts HTML content into a PDF document returned as binary data. Perfect for email attachments, API responses, or in-memory processing.

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
| true_path   | bytes     | Binary PDF data                             |
| false_path  | dict      | Error if conversion fails                   |

---

## ✅ Examples

### Simple HTML:
```json
{
  "html_input": "<html><body><h1>Invoice</h1><p>Total: $100</p></body></html>"
}
```
**Output:** PDF bytes ready for use

### Styled HTML:
```html
<html>
  <head>
    <style>
      body { font-family: Arial; margin: 40px; }
      h1 { color: #333; }
      table { width: 100%; border-collapse: collapse; }
      td, th { border: 1px solid #ddd; padding: 8px; }
    </style>
  </head>
  <body>
    <h1>Report</h1>
    <table>
      <tr><th>Item</th><th>Price</th></tr>
      <tr><td>Product A</td><td>$50</td></tr>
    </table>
  </body>
</html>
```

---

## 🎯 Common Use Cases

### Email Attachments:
```
Generate HTML → HTML to PDF (Bytes) → Send Email with Attachment
```

### API Response:
```
Query Data → Format HTML → HTML to PDF (Bytes) → HTTP Response
```

### Document Generation:
```
Template + Data → Render HTML → HTML to PDF (Bytes) → Store/Send
```

---

## 💡 Features

- **Binary Output**: Returns PDF as bytes, not file
- **Memory Efficient**: No temporary files created
- **CSS Support**: Supports inline and embedded CSS
- **Fast Conversion**: Using xhtml2pdf engine

---

## ⚠️ Notes

- Output is binary bytes (not base64 encoded)
- Requires valid HTML structure
- CSS support is limited compared to browsers
- Large documents may consume significant memory
- For file-based output, use "HTML to PDF (Save to File)" instead
