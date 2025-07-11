# Upload File(s) From UI

🧪 **Work in Progress**

> ⚠️ File management is still under active development.  
> File uploads are functional, but not yet robust for production use.  
> Known limitations include:
> - Changing the `directory` between uploads may lead to inconsistent file paths.
> - File overwrite prevention and versioning are not yet implemented.
> - No validation on filename collisions or reserved paths.

> Planned improvements:
> - Safer and consistent directory usage across multiple uploads
> - Improved UI feedback and context binding
> - Full file management capabilities (rename, delete, version control)

---

## **Category:** File

## **Description**
The **Upload File(s) From UI** node makes uploaded files available to a flow.  
These files are uploaded through the UI and referenced inside the node setup.

The files are passed to the node either:
- Via the upload modal in the visual editor (frontend)
- Or programmatically through an API

## **Variables**

| Name         | Type    | Input | Output | Description                                  |
|--------------|---------|-------|--------|----------------------------------------------|
| `files`      | list    | ❌    | ✅     | List of uploaded file keys                   |
| `directory`  | string  | ✅    | ❌     | Logical folder path to organize uploaded files |
| `is_public`  | boolean | ✅    | ❌     | Whether uploaded files are public or private |

## **Flow Control**

| Name         | Description                                  |
|--------------|----------------------------------------------|
| `true_path`  | Contains the list of uploaded file keys      |
| `false_path` | Triggered when no files were uploaded        |

## **How It Works**
1. This node receives uploaded files via the UI.
2. Each file is stored in S3 under the current tenant/project, within an optional subdirectory.
3. The file paths are returned in the `true_path`.
4. If no files were found, the node triggers `false_path`.

> ℹ️ The actual upload logic is handled by the system's backend endpoint. This node only reflects what has been received.

---

## **Example Usage**

### Input
- Files uploaded through UI (drag & drop or file select)
- `directory` = `"example"`
- `is_public` = `false`

### Output
```json
[
  "01c76259-.../example/photo1.jpg",
  "01c76259-.../example/photo2.jpg"
]