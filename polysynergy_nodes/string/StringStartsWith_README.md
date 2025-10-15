# 🎬 String Starts With Node

The `String Starts With` node checks if a text string begins with a specific prefix, with optional case-sensitive matching.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| text           | str    | ✅        | The text to check                        |
| prefix         | str    | ✅        | The prefix to check for                  |
| case_sensitive | bool   | ❌        | Whether to match case (default: true)    |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | bool      | True if text starts with the prefix         |
| false_path  | dict      | Error information if check fails            |

---

## ✅ Examples

### Check Protocol:
```json
{
  "text": "https://example.com",
  "prefix": "https://",
  "case_sensitive": true
}
```
**Output:** `true`

### Case Insensitive Check:
```json
{
  "text": "Hello World",
  "prefix": "hello",
  "case_sensitive": false
}
```
**Output:** `true`

### File Path Validation:
```json
{
  "text": "/home/user/documents/file.txt",
  "prefix": "/home/"
}
```
**Output:** `true`

---

## 💡 Use Cases

- Validate URL protocols
- Check file path patterns
- Verify string formats
- Route based on text prefixes

---

## ⚠️ Notes

- Both text and prefix must be strings
- Case-sensitive matching is enabled by default
- Empty prefix will always return `true`
- Prefix longer than text will return `false`
