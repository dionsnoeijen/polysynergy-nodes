# Create Email Attachment

Converts local files into base64-encoded attachments for email nodes.  
Features async file processing, size validation, and comprehensive MIME type support.

## **Category:** Email

## **Description**
The **Create Email Attachment** node reads a file from the local filesystem and converts it into a base64-encoded attachment dictionary that can be used with email sending nodes. The node executes asynchronously to prevent blocking during file I/O operations.

### **Key Features**
- **Async File Processing:** Non-blocking file reading operations
- **Size Validation:** Automatic file size checking with configurable limits
- **MIME Type Support:** Extensive MIME type selection for proper email handling
- **Error Handling:** Comprehensive validation and error reporting
- **Memory Efficient:** Streams large files without loading entirely into memory

---

## **Variables**

### **Input Variables**

| Name       | Type | Required | Description |
|------------|------|----------|-------------|
| `filepath` | str  | ✅       | Full path to the file to attach (e.g., "/tmp/report.pdf") |
| `filename` | str  | ✅       | Name for the attachment in the email (e.g., "Monthly Report.pdf") |
| `mimetype` | str  | ❌       | MIME type of the file (auto-detected from dropdown) |

### **Output Variables**

| Path        | Type | Description |
|-------------|------|-------------|
| `true_path` | dict | Attachment dictionary with file data |

### **Attachment Dictionary Format**
```json
{
  "filename": "document.pdf",
  "content": "JVBERi0xLjQKJeLjz9MK...",
  "mimetype": "application/pdf",
  "size": 1024000
}
```

---

## **Supported MIME Types**

The node provides a comprehensive list of MIME types organized by category:

### **Documents**
- `application/pdf` - PDF files
- `application/msword` - Microsoft Word (DOC)
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` - Word (DOCX)
- `application/vnd.ms-excel` - Microsoft Excel (XLS)
- `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` - Excel (XLSX)
- `application/vnd.ms-powerpoint` - PowerPoint (PPT)
- `application/vnd.openxmlformats-officedocument.presentationml.presentation` - PowerPoint (PPTX)
- `application/rtf` - Rich Text Format
- `text/plain` - Plain text files
- `text/csv` - Comma-separated values

### **Images**
- `image/png` - PNG images
- `image/jpeg` - JPEG images  
- `image/gif` - GIF images
- `image/webp` - WebP images
- `image/svg+xml` - SVG vector images

### **Archives**
- `application/zip` - ZIP archives
- `application/x-tar` - TAR archives
- `application/gzip` - GZIP compressed files

### **Data Formats**
- `application/json` - JSON files
- `application/xml` - XML files
- `text/html` - HTML files
- `application/yaml` - YAML files

### **Other**
- `application/octet-stream` - Generic binary files (default)

---

## **File Size Limits**

### **Individual File Limits**
- **Maximum file size:** 25MB per file
- **Minimum file size:** 1 byte (empty files rejected)

### **Validation Process**
1. **File Existence:** Verifies file exists at specified path
2. **Size Check:** Validates file size before reading
3. **Content Validation:** Ensures file is not empty
4. **Encoding:** Base64 encodes file content for email transport

---

## **Example Usage**

### **Basic File Attachment**
```yaml
filepath: "/tmp/reports/monthly_report.pdf"
filename: "Monthly Report - January 2024.pdf"
mimetype: "application/pdf"
```

### **Image Attachment**
```yaml
filepath: "/var/data/charts/sales_chart.png"
filename: "Q1 Sales Chart.png"
mimetype: "image/png"
```

### **CSV Data Export**
```yaml
filepath: "/exports/customer_data.csv"
filename: "Customer Export.csv"
mimetype: "text/csv"
```

### **Multiple Attachments Workflow**
```yaml
# Node 1: Create PDF attachment
filepath: "/reports/summary.pdf"
filename: "Executive Summary.pdf"
mimetype: "application/pdf"

# Node 2: Create Excel attachment  
filepath: "/data/analysis.xlsx"
filename: "Data Analysis.xlsx"
mimetype: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Node 3: Combine in list and send email
attachments: [attachment1_output, attachment2_output]
```

---

## **Flow Control**

### **Success Path (`true_path`)**
Returns attachment dictionary when file is successfully processed:
```json
{
  "filename": "document.pdf",
  "content": "base64-encoded-file-content",
  "mimetype": "application/pdf",
  "size": 1048576
}
```

### **Error Path (`false_path`)**
Returns error dictionary when processing fails:
```json
{
  "error": "File not found: /path/to/file.pdf"
}
```

---

## **Error Handling**

### **Common Error Messages**
- **`"File not found: /path/to/file.pdf"`** - File doesn't exist at specified path
- **`"File too large: 26214400 bytes (max 25MB)"`** - File exceeds size limit
- **`"File is empty"`** - File exists but contains no data
- **`"Permission denied"`** - Insufficient permissions to read file
- **`"Invalid attachment content: [error details]"`** - File corruption or encoding issues

### **Error Prevention**
- Verify file paths before node execution
- Check file permissions and ownership
- Monitor disk space for temporary files
- Validate file integrity before processing

---

## **Performance Considerations**

### **Async Operations**
- File reading occurs in background thread
- Large files don't block the execution pipeline
- Memory usage optimized for streaming operations

### **Memory Usage**
- Files are read and encoded in chunks
- Base64 encoding increases size by ~33%
- Total memory usage: `file_size * 1.33 + overhead`

### **File System Impact**
- Uses standard file system read operations
- No temporary files created during processing
- Respects file system locks and permissions

---

## **Integration Patterns**

### **Single Attachment**
```yaml
# Create attachment -> Send email
Create Attachment -> Send Email
```

### **Multiple Attachments**
```yaml
# Create multiple attachments -> Combine -> Send email
Create Attachment 1 ----\
Create Attachment 2 ------> List Merge -> Send Email
Create Attachment 3 ----/
```

### **Conditional Attachments**
```yaml
# Attach file only if it exists and meets criteria
File Exists Check -> Create Attachment -> Send Email
                 \-> Skip if no file
```

### **Dynamic File Processing**
```yaml
# Process files from directory listing
List Files -> For Each File -> Create Attachment -> Collect -> Send Email
```

---

## **Best Practices**

### **File Management**
- Use absolute file paths when possible
- Verify file existence before processing
- Clean up temporary files after use
- Monitor file system permissions

### **Size Management**
- Check file sizes before attachment creation
- Consider compression for large text files
- Use appropriate MIME types for better client handling
- Split large datasets into multiple smaller attachments

### **Security**
- Validate file paths to prevent directory traversal
- Scan files for malware before attachment
- Use appropriate file permissions
- Log attachment creation for audit trails

### **Error Handling**
- Always handle the `false_path` scenario
- Provide meaningful error messages to users
- Implement retry logic for transient file system errors
- Monitor file system health and capacity

---

## **Use Cases**

### **Report Distribution**
- PDF reports from reporting systems
- Excel spreadsheets with data analysis
- CSV exports for further processing

### **Document Sharing**
- Contract documents and agreements
- Technical documentation and manuals
- Image files and diagrams

### **Data Export**
- Database exports in various formats
- Log files for troubleshooting
- Configuration backups

### **Content Delivery**
- Marketing materials and brochures
- Product catalogs and price lists
- Training materials and resources

---

## **Troubleshooting**

### **File Not Found Errors**
1. Verify the complete file path
2. Check file system permissions
3. Ensure the file hasn't been moved or deleted
4. Use absolute paths instead of relative paths

### **Size Limit Errors**
1. Check actual file size vs. limit
2. Consider file compression
3. Split large files into smaller parts
4. Use cloud storage links for very large files

### **Permission Errors**
1. Verify read permissions on the file
2. Check directory permissions
3. Ensure the process has appropriate access
4. Consider running with elevated permissions if needed

---

📎 **Use this node to reliably convert local files into email-ready attachments with comprehensive validation and error handling.**