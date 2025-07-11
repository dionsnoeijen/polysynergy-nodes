# Upload From Data

🧪 **Work in Progress**

> ⚠️ This node is still under active development.  
> It can upload files from base64 or binary data, but assumes clean input and a stable runtime environment.  
> Known limitations include:
> - Overwrites files silently if the same name/path is used
> - No file-type validation or size limits
> - Depends on environment variables `TENANT_ID` and `PROJECT_ID` being available

> Planned improvements:
> - File existence checks or overwrite settings
> - Optional hashing or automatic filename prefixing
> - Support for file-type and size validation

---

## **Category:** File

## **Description**
The **Upload From Data** node uploads a file to S3 using either base64-encoded content or raw binary input.  
It is used to send files into your workspace from API or dynamic content pipelines.

## **Variables**

| Name           | Type     | Input | Output | Description                                      |
|----------------|----------|-------|--------|--------------------------------------------------|
| `file_base64`  | string   | ✅    | ❌     | Base64-encoded file content                      |
| `file_bytes`   | bytes    | ✅    | ❌     | Binary content of the file (alternative to base64) |
| `file_name`    | string   | ✅    | ❌     | Name of the file to be saved (e.g. `data.csv`)   |
| `directory`    | string   | ✅    | ❌     | Optional folder name in your S3 scope            |
| `is_public`    | boolean  | ✅    | ✅     | Whether the file is public or private            |
| `url`          | string   | ❌    | ✅     | Direct (presigned) URL to the uploaded file      |

## **Flow Control**

| Name         | Description                        |
|--------------|------------------------------------|
| `true_path`  | File key of the uploaded file      |
| `false_path` | Triggered when an error occurs     |

---

## **How It Works**
1. Receives file content in either base64 or bytes format.
2. Builds an S3 file key: `{tenant_id}/{project_id}/{scope}/{directory}/{filename}`
3. Uploads the file using the appropriate visibility.
4. Returns a download URL and the file key.

---

## **Example Usage**

### Input
- `file_base64` = `"VGhpcyBpcyBhIHRlc3QuCg=="`
- `file_name` = `"test.txt"`
- `directory` = `"uploads"`
- `is_public` = `false`

### Output
- `true_path` = `".../uploads/test.txt"`
- `url` = `"https://.../uploads/test.txt?X-Amz-Signature=..."`

---

## **Use Cases**
✔ Uploading dynamically generated files (CSV, PDF, images)  
✔ Forwarding files from API payloads  
✔ Generating temporary links for downloads

---

📁 **This node is part of a growing file management system. Improvements are ongoing.**