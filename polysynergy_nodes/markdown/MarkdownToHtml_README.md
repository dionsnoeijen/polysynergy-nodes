# Markdown to HTML

Converts Markdown text to HTML format with extended syntax support.  
Perfect for rendering rich text content from Markdown files or user input.

## **Category:** Utils

## **Description**
The **Markdown to HTML** node transforms raw Markdown text into properly formatted HTML.

It supports:
- Standard Markdown syntax (headers, paragraphs, lists, links, images)
- Extended syntax via the "extra" extension (tables, fenced code blocks, definition lists)
- Smart typography via the "smarty" extension (smart quotes, dashes, ellipses)
- Graceful error handling for conversion issues

## **Variables**

| Name             | Type | Input | Output | Description |
|------------------|------|-------|--------|-------------|
| `markdown_input` | str  | ✅     | ❌      | The raw markdown string to convert to HTML. |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered if conversion succeeds. Contains the HTML string. |
| `false_path` | Triggered if conversion fails. Contains an error dictionary. |

## **How It Works**
1. Accepts raw Markdown input (`markdown_input`) as a string.
2. Processes the Markdown using the Python `markdown` library with:
   - `extra` extension: Adds support for tables, fenced code blocks, and more
   - `smarty` extension: Converts quotes and dashes to typographically correct forms
3. If successful:
   - Emits the converted HTML string to `true_path`.
4. If conversion fails:
   - Sends a descriptive error to `false_path`.

---

## **Example Usage**

### **Input**
- `markdown_input` = `"# Hello World\n\nThis is **bold** text with a [link](https://example.com)."`

### **Output (success)**
- `true_path` = `"<h1>Hello World</h1>\n<p>This is <strong>bold</strong> text with a <a href=\"https://example.com\">link</a>.</p>"`

### **Advanced Example - Table**
- `markdown_input`:
```markdown
| Name    | Age |
|---------|-----|
| Alice   | 30  |
| Bob     | 25  |
```

- `true_path`:
```html
<table>
<thead>
<tr>
<th>Name</th>
<th>Age</th>
</tr>
</thead>
<tbody>
<tr>
<td>Alice</td>
<td>30</td>
</tr>
<tr>
<td>Bob</td>
<td>25</td>
</tr>
</tbody>
</table>
```

### **Smart Typography Example**
- `markdown_input` = `"She said \"Hello world\" -- it was nice."`
- `true_path` = `"<p>She said "Hello world" – it was nice.</p>"`

### **Output (error)**
- `false_path`:
```json
{
  "error": "Markdown conversion error details"
}
```

---

## **Error Handling**
- Unexpected exceptions during conversion are caught and returned with descriptive error messages.
- Invalid input types or processing errors trigger the `false_path`.

---

## **Supported Markdown Features**

### **Standard Markdown**
✔ Headers (`# ## ###`)  
✔ Paragraphs and line breaks  
✔ **Bold** and *italic* text  
✔ Links and images  
✔ Ordered and unordered lists  
✔ Code spans and blocks  

### **Extended Features (via "extra" extension)**
✔ Tables  
✔ Fenced code blocks with syntax highlighting classes  
✔ Definition lists  
✔ Footnotes  
✔ Abbreviations  

### **Smart Typography (via "smarty" extension)**
✔ Smart quotes (`"` becomes `"` and `"`)  
✔ Em dashes (`--` becomes `–`)  
✔ Ellipses (`...` becomes `…`)  

---

## **Use Cases**
✔ Converting Markdown documentation to HTML  
✔ Rendering user-generated content from Markdown editors  
✔ Processing README files for web display  
✔ Creating rich text outputs from simple Markdown input  
✔ Blog post or article content conversion  

---

📝 **Use this node when you need to convert Markdown text into HTML for web display or further processing.**