# File Selection

A node for handling files selected through the Portal's file manager interface.

## **Category:** File

## **Description**
The **File Selection** node receives a list of file locations that have been selected through the Portal's file manager. Unlike the traditional upload nodes, this node works with files that are already managed and stored, allowing users to select from existing files rather than uploading new ones.

This node is designed to work with the Portal's new file manager functionality, which handles file organization, storage, and selection separately from workflow execution.

---

## **Variables**

### **Input Variables**

| Name             | Type | Description |
|------------------|------|-------------|
| `selected_files` | list | List of file locations selected from the file manager |

### **Output Variables**

| Name             | Type | Description |
|------------------|------|-------------|
| `selected_files` | list | The same list of selected file locations (pass-through) |
| `file_count`     | int  | Number of files selected |

---

## **Flow Control**

| Path        | Condition | Description |
|-------------|-----------|-------------|
| `true_path` | Files selected | Contains the list of selected file locations |
| `false_path` | No files selected | Triggered when no files were selected |

---

## **How It Works**

1. **File Manager Integration**: Files are selected through the Portal's file manager interface
2. **Node Configuration**: The selected file locations are passed to this node
3. **Validation**: Node checks if any files were selected
4. **Output**: If files exist, they're passed to `true_path`; otherwise `false_path` is triggered
5. **Count**: The number of selected files is provided as `file_count`

### **File Manager Workflow**
```
Portal File Manager → File Selection Node → Workflow Processing
     ↓                      ↓                      ↓
  - Browse files         - Receive list         - Process files
  - Select files         - Validate selection   - Continue workflow  
  - Organize files       - Count files          - Handle errors
```

---

## **Example Usage**

### **Basic File Selection**
```yaml
# Node receives files selected from file manager
File Selection:
  selected_files: 
    - "tenant123/project456/private/documents/report.pdf"
    - "tenant123/project456/private/images/chart.png"
    - "tenant123/project456/private/data/dataset.csv"
  
# Output:
true_path: [list of 3 file locations]
file_count: 3
```

### **No Files Selected**
```yaml
# When no files are selected
File Selection:
  selected_files: []

# Output:
false_path: {"error": "No files selected from file manager."}
file_count: 0
```

### **Single File Selection**
```yaml
# Single file selected
File Selection:
  selected_files: 
    - "tenant123/project456/public/uploads/document.pdf"

# Output:
true_path: ["tenant123/project456/public/uploads/document.pdf"]
file_count: 1
```

---

## **Integration Patterns**

### **With File Processing Nodes**
```yaml
# Chain file selection with processing
File Selection → File Type Detection → Document Analysis
     ↓                  ↓                    ↓
  Select files     Identify types      Process content
```

### **With Conditional Logic**
```yaml
# Handle different file counts
File Selection → Switch Case (based on file_count)
     ↓              ↓
  Get files    ├── Single file processing
               ├── Batch processing  
               └── Error handling
```

### **With Upload Validation**
```yaml
# Validate selected files before processing
File Selection → File Type Filter → Content Validation
     ↓                ↓                    ↓
  Get files      Filter by type       Validate content
```

---

## **File Location Format**

File locations follow the standard PolySynergy path structure:
```
{tenant_id}/{project_id}/{scope}/{directory}/{filename}

Examples:
- tenant123/project456/private/documents/report.pdf
- tenant123/project456/public/images/logo.png  
- tenant123/project456/private/uploads/data.csv
```

### **Scope Types**
- **private**: Files accessible only within the project
- **public**: Publicly accessible files

---

## **Best Practices**

### **File Selection**
- **Organized Selection**: Use the file manager's organization features for logical file grouping
- **Scope Awareness**: Be mindful of public vs private file scopes
- **Batch Processing**: Select related files together for efficient batch processing
- **Validation**: Always handle the case where no files are selected

### **Workflow Design**
- **Error Handling**: Always connect the `false_path` for graceful error handling
- **File Count Logic**: Use `file_count` for conditional processing based on selection size
- **Type Checking**: Consider following with file type detection for mixed selections
- **Performance**: Be aware that large file selections may impact performance

### **File Management**
- **Organization**: Keep files organized in logical directories through the file manager
- **Naming**: Use descriptive filenames for better workflow clarity
- **Cleanup**: Regularly review and manage files through the file manager
- **Access Control**: Properly configure file scopes based on security requirements

---

## **Troubleshooting**

### **Common Issues**

#### **No Files in Output**
- **Symptom**: `false_path` is triggered unexpectedly
- **Cause**: File selection was not properly configured or files were deselected
- **Resolution**: Verify file selection in the Portal's file manager

#### **File Access Errors**
- **Symptom**: Files show in selection but can't be accessed in subsequent nodes
- **Cause**: File permissions or scope mismatches
- **Resolution**: Check file scope settings and access permissions

#### **Performance Issues**
- **Symptom**: Node processing is slow with large file selections
- **Cause**: Too many files selected at once
- **Resolution**: Consider batch processing or filtering files before selection

---

## **Differences from Upload Nodes**

### **File Selection vs Upload From UI**

| Aspect | File Selection | Upload From UI |
|--------|----------------|----------------|
| **Source** | Existing managed files | New file uploads |
| **Interface** | File manager selection | Upload modal/drag-drop |
| **Storage** | Files already stored | Files uploaded on demand |
| **Organization** | Pre-organized through file manager | Organized during upload |
| **Performance** | Fast (no upload time) | Depends on file size/count |

### **When to Use Each**

#### **Use File Selection When:**
- Working with existing, managed files
- Files are already organized and stored
- Need to reuse files across multiple workflows
- Want to leverage file manager's organization features
- Processing previously uploaded or generated files

#### **Use Upload From UI When:**
- Need to upload new files as part of the workflow
- Files are not yet in the system
- One-time file processing scenarios
- Direct file upload is required from external sources

---

## **Migration from Upload From UI**

If migrating from the traditional upload approach:

### **Before (Upload From UI)**
```yaml
Upload File(s) From UI:
  directory: "documents"
  is_public: false
  # Files uploaded through UI
```

### **After (File Selection)**
```yaml
File Selection:
  selected_files: [pre-selected through file manager]
  # Files already managed and organized
```

### **Migration Benefits**
- **Better Organization**: Files are managed centrally through the file manager
- **Reusability**: Files can be used across multiple workflows
- **Performance**: No upload delays during workflow execution
- **Management**: Better file lifecycle management and organization

---

## **Related Components**

### **Portal File Manager**
- **Purpose**: Central file management interface
- **Features**: File organization, selection, permissions, lifecycle management
- **Integration**: Provides file locations to this node

### **Other File Nodes**
- **Upload From UI**: For new file uploads during workflow execution
- **Upload From Data**: For programmatic file uploads from data
- **File Type**: For detecting and working with file types

---

🗂️ **Use this node to work with files that have been selected through the Portal's file manager interface.**