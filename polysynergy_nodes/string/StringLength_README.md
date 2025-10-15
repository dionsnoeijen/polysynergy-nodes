# 📏 String Length Node

The `String Length` node returns the character count of a text string.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to measure                      |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | int       | The length of the string                    |
| false_path  | dict      | Error information if input is invalid       |

---

## ✅ Examples

### Basic Length:
```json
{
  "text": "Hello World"
}
```
**Output:** `11`

### Empty String:
```json
{
  "text": ""
}
```
**Output:** `0`

### Multi-line Text:
```json
{
  "text": "Line 1\nLine 2\nLine 3"
}
```
**Output:** `20` (includes newline characters)

---

## 💡 Use Cases

- Validate input length constraints
- Count characters for text limits
- Check if string is empty
- Calculate text metrics

---

## ⚠️ Notes

- Input must be a string type
- Counts all characters including spaces and special characters
- Unicode characters are counted as single characters
- Empty string returns `0`, not an error
