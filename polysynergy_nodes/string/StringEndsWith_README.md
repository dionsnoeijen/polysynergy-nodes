# 🏁 String Ends With Node

The `String Ends With` node checks if a text string ends with a specific suffix, with optional case-sensitive matching.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| text           | str    | ✅        | The text to check                        |
| suffix         | str    | ✅        | The suffix to check for                  |
| case_sensitive | bool   | ❌        | Whether to match case (default: true)    |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | bool      | True if text ends with the suffix           |
| false_path  | dict      | Error information if check fails            |

---

## ✅ Example

### Check File Extension:
```json
{
  "text": "document.PDF",
  "suffix": ".pdf",
  "case_sensitive": false
}
```
**Output:** `true`

### Case Sensitive Check:
```json
{
  "text": "Hello World!",
  "suffix": "world!",
  "case_sensitive": true
}
```
**Output:** `false`

---

## 💡 Use Cases

- Validate file extensions
- Check URL patterns
- Verify string formats
- Route based on text endings

---

## ⚠️ Notes

- Both text and suffix must be strings
- Case-sensitive matching is enabled by default
- Empty suffix will always return `true`
