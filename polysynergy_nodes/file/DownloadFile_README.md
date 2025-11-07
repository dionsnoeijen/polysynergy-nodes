# Download File Node

The **Download File** node downloads files from multiple sources:
- **File Manager** (S3 storage) - Works with the File Selection node
- **HTTP/HTTPS URLs** - Download files from any web location

The node automatically detects the source type and handles the download appropriately.

---

## 🔧 Node Configuration

### Inputs

- **file_path** (`str`, required):
  File Manager path (e.g., `"folder/document.csv"`) or URL (e.g., `"https://example.com/data.csv"`).
  - File Manager: Use with File Selection node output
  - URLs: Any publicly accessible HTTP/HTTPS URL

- **timeout** (`int`, optional):
  Timeout in seconds for URL downloads. Default: `30`. Only applies to HTTP/HTTPS downloads.

- **decode_as_text** (`bool`, optional):
  Whether to decode the file content as UTF-8 text. Default: `True`.
  - If `True`: Returns content as string (for text files, CSV, JSON, etc.)
  - If `False`: Returns content as raw bytes (for binary files, images, PDFs, etc.)

---

### Outputs

- **file_content** (`str | bytes`):
  The file content. Type depends on `decode_as_text` setting.

- **file_name** (`str`):
  Name of the downloaded file (extracted from the path).

- **file_size** (`int`):
  Size of the file in bytes.

- **local_path** (`str`):
  Path to the downloaded file in `/tmp/` directory. Useful if you need to pass the file to other nodes that expect file paths.

- **true_path** (path):
  Triggered on success. Returns the file content.

- **false_path** (path):
  Triggered if download fails. Returns error info.

---

## 🧠 Example Use

### Download from File Manager (CSV)

**Workflow**: File Selection → Get Item by Index → Download File → CSV to List

```json
{
  "file_path": "csv_companies/sales_data.csv",
  "decode_as_text": true
}
```

**Output (`file_content`):**
```
"name,revenue,employees
Acme Corp,1500000,250
Tech Inc,3200000,480"
```

**Output (`file_name`):** `"sales_data.csv"`
**Output (`file_size`):** `85`
**Output (`local_path`):** `"/tmp/sales_data.csv"`

---

### Download from URL (CSV)

```json
{
  "file_path": "https://example.com/data/sales_2024.csv",
  "decode_as_text": true,
  "timeout": 30
}
```

**Output (`file_content`):**
```
"product,quantity,price
Widget A,150,29.99
Widget B,230,19.99"
```

**Output (`file_name`):** `"sales_2024.csv"`

---

### Download from URL (Image)

```json
{
  "file_path": "https://example.com/assets/logo.png",
  "decode_as_text": false
}
```

**Output (`file_content`):** `b'\x89PNG\r\n\x1a\n...'` (raw bytes)
**Output (`file_name`):** `"logo.png"`

---

### Common Workflow

1. **File Selection** - User selects file from file manager → outputs `["folder/file.csv"]`
2. **Get Item by Index** (index: 0) - Extract first file path → outputs `"folder/file.csv"`
3. **Download File** - Download and read content → outputs file content as text
4. **CSV to List** - Parse CSV → outputs list of dicts

---

## ⚠️ Notes

- **Source Detection**: Automatically detects URL (starts with `http://` or `https://`) vs File Manager path
- **File Manager**: Uses tenant and project IDs from environment to determine S3 bucket automatically
- **URLs**: Downloads from any publicly accessible HTTP/HTTPS location
- **Storage**: Files are downloaded to `/tmp/` directory with their original filename
- **Text vs Binary**:
  - Use `decode_as_text=True` for text files (CSV, JSON, TXT, XML, etc.)
  - Use `decode_as_text=False` for binary files (images, PDFs, ZIP, etc.)
- **Local Path**: The `local_path` output can be passed to nodes that expect file paths
- **File Size**: Maximum depends on available memory and Lambda/container limits
- **Timeout**: Only applies to URL downloads; S3 downloads use boto3 defaults
- **Error Handling**: `false_path` is triggered for:
  - File not found (404 for URLs, missing S3 key)
  - Network errors (timeouts, connection failures)
  - Permission errors (unauthorized S3 access)

---

## 🧩 Category

- `file`
