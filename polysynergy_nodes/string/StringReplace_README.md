# 🔄 String Replace Node

The `String Replace` node replaces occurrences of a substring with another string, with optional limit on the number of replacements.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to process                      |
| old        | str    | ✅        | The substring to find                    |
| new        | str    | ❌        | The replacement string (default: "")     |
| count      | int    | ❌        | Max replacements (-1 for all, default: -1) |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The text with replacements made             |
| false_path  | dict      | Error information if replace fails          |

---

## ✅ Examples

### Replace All:
```json
{
  "text": "Hello World, Hello Universe",
  "old": "Hello",
  "new": "Hi"
}
```
**Output:** `"Hi World, Hi Universe"`

### Replace First Occurrence Only:
```json
{
  "text": "cat cat cat",
  "old": "cat",
  "new": "dog",
  "count": 1
}
```
**Output:** `"dog cat cat"`

### Remove Text (Empty Replacement):
```json
{
  "text": "Hello [REDACTED] World",
  "old": "[REDACTED]",
  "new": ""
}
```
**Output:** `"Hello  World"`

### Replace Multiple Occurrences:
```json
{
  "text": "a-b-c-d-e",
  "old": "-",
  "new": " | ",
  "count": 2
}
```
**Output:** `"a | b | c-d-e"`

---

## 💡 Use Cases

- Clean and normalize text data
- Remove unwanted characters or patterns
- Update placeholders with actual values
- Sanitize user input
- Format output strings

---

## ⚠️ Notes

- All parameters (text, old, new) must be strings
- Count of `-1` replaces all occurrences (default behavior)
- Empty `old` string will raise an error
- Case-sensitive replacement only
- If `old` is not found, original text is returned unchanged
