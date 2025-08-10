# File Storage

Universal file storage node that accepts any type of content and intelligently stores it in your file manager.  
Handles text, binary data, generated content, and files from various sources with automatic format detection.

## **Category:** File

## **Description**
The **File Storage** node provides a unified way to store any type of content as files in your file manager. It automatically detects content types, handles different input formats, and manages file naming and organization.

Perfect for:
- **Generated Content**: Store PDFs, reports, or documents created by other nodes
- **API Responses**: Save JSON, XML, or HTML data as files
- **User Uploads**: Handle files from UI components or external sources
- **Binary Data**: Store images, documents, or any binary content
- **Text Content**: Save logs, reports, or processed text data

Key features:
- **Smart Content Detection**: Automatically identifies file types (PDF, JSON, HTML, images, etc.)
- **Flexible Input**: Accepts strings, bytes, base64, or data URLs
- **Intelligent Naming**: Auto-generates meaningful filenames or uses custom names
- **Path Organization**: Customizable directory structure with security validation
- **Duplicate Handling**: Option to overwrite or create unique filenames
- **Rich Metadata**: Returns comprehensive file information and storage details

## **Variables**

### **Content Input**
| Name           | Type   | Input | Required | Description |
|----------------|--------|-------|----------|-------------|
| `content_data` | str/bytes | ✅   | ✅        | File content (string, bytes, or base64) |
| `content_type` | str    | ✅     | ❌        | Type of content (`auto`, `text`, `html`, `json`, `pdf`, `image`, etc.) |
| `data_format`  | str    | ✅     | ❌        | Input format (`auto`, `string`, `base64`, `bytes`) |

### **File Configuration**
| Name             | Type | Input | Required | Description |
|------------------|------|-------|----------|-------------|
| `filename`       | str  | ✅     | ❌        | Custom filename (without extension) |
| `file_extension` | str  | ✅     | ❌        | Custom file extension (overrides auto-detection) |
| `save_path`      | str  | ✅     | ❌        | Directory path (default: `generated/files/`) |
| `overwrite`      | bool | ✅     | ❌        | Allow overwriting existing files |

### **Output Variables**
| Name            | Type | Output | Description |
|-----------------|------|--------|-------------|
| `file_url`     | str  | ✅      | Direct URL to the stored file |
| `file_path`     | str  | ✅      | S3 key/path of the stored file |
| `file_size`     | int  | ✅      | File size in bytes |
| `mime_type`     | str  | ✅      | Detected MIME type |
| `file_metadata` | dict | ✅      | Complete file information and metadata |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Triggered when file is successfully stored. Contains file metadata. |
| `false_path` | Triggered when storage fails. Contains error details. |

## **How It Works**

### **Processing Pipeline**
1. **Content Processing**: Convert input to bytes based on data format
2. **Type Detection**: Identify content type from data signatures or structure  
3. **Filename Generation**: Create meaningful filename or use custom name
4. **Path Validation**: Ensure safe directory structure
5. **File Storage**: Upload to S3 with appropriate metadata
6. **URL Generation**: Return accessible URLs and file information

### **Smart Content Detection**
- **PDF Files** → Detects PDF signature (`%PDF`)
- **Images** → Recognizes PNG, JPEG, GIF, WebP headers
- **JSON Data** → Parses and validates JSON structure
- **HTML Content** → Identifies HTML tags and DOCTYPE
- **CSV Data** → Detects comma-separated structure
- **XML Documents** → Recognizes XML declaration and tags
- **JavaScript** → Identifies function patterns and syntax
- **CSS Stylesheets** → Detects CSS rule patterns
- **Plain Text** → Default for readable text content
- **Binary Data** → Fallback for non-text content

---

## **Example Usage**

### **Store Generated PDF**
```
Input:
- content_data: [PDF bytes from PDF generator node]
- content_type: "auto"
- filename: "invoice_2024_001"
- save_path: "invoices/2024/"

Output:
- file_url: "https://cdn.example.com/invoices/2024/invoice_2024_001_a1b2c3d4.pdf"
- file_path: "invoices/2024/invoice_2024_001_a1b2c3d4.pdf"
- mime_type: "application/pdf"
```

### **Save JSON API Response**
```
Input:
- content_data: '{"users": [{"name": "John", "age": 30}], "total": 1}'
- content_type: "auto"  # Will detect as JSON
- filename: "user_export"
- save_path: "exports/"

Output:
- file_url: "https://cdn.example.com/exports/user_export_e5f6g7h8.json"
- mime_type: "application/json"
- file_metadata: {"content_type": "json", "processing": {"auto_detected_type": "json"}}
```

### **Store HTML Report**
```
Input:
- content_data: "<html><head><title>Report</title></head><body><h1>Monthly Report</h1>...</body></html>"
- content_type: "html"
- filename: "monthly_report"
- save_path: "reports/2024/"

Output:
- file_url: "https://cdn.example.com/reports/2024/monthly_report_i9j0k1l2.html"
- mime_type: "text/html"
```

### **Handle Base64 Image from UI**
```
Input:
- content_data: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
- data_format: "base64"  # Will auto-detect data URL
- content_type: "auto"   # Will detect as image
- save_path: "uploads/"

Output:
- file_url: "https://cdn.example.com/uploads/image_20240315_143022_123.png"
- mime_type: "image/png"
```

### **Store CSV Export**
```
Input:
- content_data: "name,email,status\nJohn,john@email.com,active\nJane,jane@email.com,inactive"
- content_type: "csv"
- filename: "user_export"
- overwrite: true

Output:
- file_url: "https://cdn.example.com/generated/files/user_export.csv"
- file_metadata: {"filename": "user_export.csv", "content_type": "csv"}
```

### **Store Binary Data**
```
Input:
- content_data: [Binary bytes from external API]
- data_format: "bytes"
- filename: "document"
- file_extension: ".docx"

Output:
- file_url: "https://cdn.example.com/generated/files/document_m3n4o5p6.docx"
- mime_type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
```

---

## **Supported Content Types**

### **Auto-Detected Types**
✅ **PDF Documents** → `.pdf` (detects PDF signature)  
✅ **JSON Data** → `.json` (validates JSON structure)  
✅ **HTML Documents** → `.html` (finds HTML tags)  
✅ **XML Documents** → `.xml` (detects XML declaration)  
✅ **CSV Data** → `.csv` (identifies comma-separated format)  
✅ **JavaScript** → `.js` (recognizes JS syntax patterns)  
✅ **CSS Stylesheets** → `.css` (identifies CSS rules)  
✅ **Images** → `.png/.jpg/.gif/.webp` (detects image headers)  
✅ **Plain Text** → `.txt` (readable text fallback)  
✅ **Binary Data** → `.bin` (non-text binary fallback)  

### **Explicit Content Types**
- `text` → Plain text files (`.txt`)
- `html` → HTML documents (`.html`) 
- `css` → CSS stylesheets (`.css`)
- `javascript` → JavaScript files (`.js`)
- `json` → JSON data files (`.json`)
- `xml` → XML documents (`.xml`)
- `csv` → CSV data files (`.csv`)
- `pdf` → PDF documents (`.pdf`)
- `image` → Image files (`.png` default)
- `binary` → Binary data (`.bin`)

### **Input Data Formats**
✅ **String** → Text content, JSON, HTML, CSV, etc.  
✅ **Base64** → Encoded binary data or data URLs  
✅ **Bytes** → Raw binary content  
✅ **Data URLs** → `data:image/png;base64,...` format  

---

## **File Naming & Organization**

### **Automatic Filename Generation**
When no custom filename is provided:
```
text_20240315_143022_123.txt
data_20240315_143055_456.json  
document_20240315_144012_789.html
image_20240315_145030_012.png
```

### **Custom Naming**
```
Input: filename = "user_report"
Output: user_report_a1b2c3d4.json  # Hash added when overwrite=false
```

### **Path Organization**
```
save_path: "reports/2024/march/"
→ Full path: reports/2024/march/monthly_report_hash.pdf
```

### **Duplicate Handling**
- **`overwrite: true`** → Replaces existing files with same name
- **`overwrite: false`** → Adds unique hash to prevent conflicts

---

## **Integration Examples**

### **PDF Generation Pipeline**
```
Generate PDF → File Storage → Email Attachment
             └─ file_url   └─ attachment_url
```

### **API Data Export**
```
HTTP Request → JSON Extract → File Storage → File Manager
             └─ response   └─ file_url    └─ Download Link
```

### **Report Generation Workflow**
```
Data Query → HTML Template → File Storage → Notification
           └─ data        └─ report.html └─ "Report ready!"
```

### **User File Upload**
```
UI File Upload → File Storage → Database Record
               └─ file_data   └─ file_url stored
```

### **Multi-Format Content Hub**
```
Various Sources → File Storage → File Manager
├─ PDF Reports     ├─ /reports/
├─ JSON Exports    ├─ /exports/
├─ HTML Pages      ├─ /pages/
└─ Images          └─ /images/
```

---

## **Security & Validation**

### **Path Security**
✅ **Prevents directory traversal** (`../` blocked)  
✅ **Relative paths only** (absolute paths rejected)  
✅ **Character validation** (dangerous chars removed)  
✅ **Length limits** (prevents excessively long paths)  

### **Content Validation**
✅ **Size limits** (configurable file size restrictions)  
✅ **Type validation** (MIME type verification)  
✅ **Safe naming** (filename sanitization)  
✅ **Extension security** (prevents dangerous extensions)  

---

## **Error Handling**

### **Common Issues**
| Error | Cause | Solution |
|-------|-------|----------|
| Empty content | No content provided | Ensure content_data is not empty |
| Invalid base64 | Malformed encoding | Check base64 format is correct |
| Path validation | Unsafe directory path | Use relative paths without `../` |
| Upload failure | S3 connectivity/permissions | Verify AWS credentials and bucket access |
| Type detection failure | Unrecognizable format | Specify content_type explicitly |

---

## **Migration from Old Nodes**

### **Replace Upload From Data**
```
Old Node: Upload From Data
- file_base64 → content_data
- file_bytes  → content_data
- file_name   → filename
- directory   → save_path

New: File Storage (handles both formats automatically)
```

### **Replace Upload From UI**
```
Old Node: Upload From UI  
- files[0].data → content_data
- directory     → save_path

New: File Storage (with UI file picker integration)
```

---

## **Use Cases**
✔ **Document Generation**: Store generated PDFs, reports, invoices  
✔ **Data Export**: Save API responses, database exports, analytics data  
✔ **Content Management**: Organize generated HTML, CSS, JavaScript files  
✔ **File Processing**: Store processed images, converted documents  
✔ **Backup & Archive**: Preserve important data and generated content  
✔ **Integration Hub**: Central storage for multi-source file handling  
✔ **Report Distribution**: Generate and store reports for download  

---

📁 **Use this node as your universal file storage solution - it intelligently handles any content type and organizes files in your file manager.**