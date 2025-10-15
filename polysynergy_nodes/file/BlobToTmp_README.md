# 💾 Blob to Tmp Node

The `Blob to Tmp` node saves binary data (blob) to a temporary file with optional naming and extension control. Returns file path and metadata.

---

## 📂 Category

**file**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| blob       | bytes  | ✅        | Binary file data to save                 |
| filename   | str    | ❌        | Optional filename (with/without extension) |
| extension  | str    | ❌        | Optional file extension (.pdf, .docx, etc) |

---

## 🔌 Outputs

| Name              | Type   | Description                              |
|-------------------|--------|------------------------------------------|
| tmp_path          | str    | Full path to created temp file           |
| file_size         | int    | Size of file in bytes                    |
| file_extension    | str    | Final extension used                     |
| original_filename | str    | Original filename provided               |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | File path (same as tmp_path)                |
| false_path  | Error if file writing fails                 |

---

## ✅ Examples

### Basic Blob Storage:
```json
{
  "blob": "<binary pdf data>",
  "extension": ".pdf"
}
```
**Output:** `"/tmp/a1b2c3d4_download.pdf"`

### Named File:
```json
{
  "blob": "<binary image data>",
  "filename": "photo.jpg"
}
```
**Output:** `"/tmp/e5f6g7h8_photo.jpg"`

### With Custom Extension:
```json
{
  "blob": "<binary data>",
  "filename": "document",
  "extension": ".docx"
}
```
**Output:** `"/tmp/i9j0k1l2_document.docx"`

---

## 📁 File Naming Logic

1. **Unique ID**: 8-character UUID prefix prevents collisions
2. **Base Name**: From filename parameter or defaults to "download"
3. **Extension Priority**:
   - Explicit `extension` parameter
   - Extension from `filename`
   - Default: `.bin`

**Format:** `{unique_id}_{basename}{extension}`

---

## 🔒 Security Features

- **Sanitization**: Removes unsafe characters from paths
- **Collision Prevention**: UUID prefix ensures uniqueness
- **Placeholder Support**: Both inputs support placeholder replacement
- **Type Handling**: Accepts both bytes and string input

---

## 💡 Use Cases

- **Download Processing**: Save API downloads to disk
- **File Conversion**: Store intermediate conversion results
- **Attachment Handling**: Save email attachments temporarily
- **Batch Processing**: Store files for batch operations

---

## ⚠️ Notes

- Files saved to system temp directory
- Files persist until manually deleted or system cleanup
- Supports placeholder replacement in filename/extension
- String input automatically converted to bytes (UTF-8)
- Returns absolute file path for easy chaining
