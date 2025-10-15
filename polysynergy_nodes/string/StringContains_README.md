# 🔍 String Contains Node

The `String Contains` node checks if a text string contains a specific substring, with optional case-sensitive matching.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name           | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| text           | str    | ✅        | The text to search in                    |
| search         | str    | ✅        | The substring to search for              |
| case_sensitive | bool   | ❌        | Whether to match case (default: true)    |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | bool      | True if text contains the search string     |
| false_path  | dict      | Error information if search fails           |

---

## ✅ Example

### Case Sensitive Search:
```json
{
  "text": "Hello World",
  "search": "world",
  "case_sensitive": true
}
```
**Output:** `false`

### Case Insensitive Search:
```json
{
  "text": "Hello World",
  "search": "world",
  "case_sensitive": false
}
```
**Output:** `true`

---

## 💡 Use Cases

- Validate user input contains required text
- Filter data based on content
- Search for keywords in documents
- Conditional routing based on text content

---

## ⚠️ Notes

- Both text and search must be strings
- Case-sensitive matching is enabled by default
- Returns `false` (boolean) when substring is not found, not an error
