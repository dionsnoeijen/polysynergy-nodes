# ✨ String Trim Node

The `String Trim` node removes whitespace or specified characters from the beginning and end of a text string.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to trim                         |
| characters | str    | ❌        | Characters to remove (default: whitespace) |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The trimmed string                          |
| false_path  | dict      | Error information if trim fails             |

---

## ✅ Examples

### Trim Whitespace (Default):
```json
{
  "text": "   Hello World   "
}
```
**Output:** `"Hello World"`

### Trim Specific Characters:
```json
{
  "text": "***Hello***",
  "characters": "*"
}
```
**Output:** `"Hello"`

### Trim Multiple Characters:
```json
{
  "text": "...Hello World...",
  "characters": "."
}
```
**Output:** `"Hello World"`

### Trim Mixed Whitespace:
```json
{
  "text": "\n\t  Hello World  \t\n"
}
```
**Output:** `"Hello World"`

---

## 💡 Use Cases

- Clean user input
- Remove padding from parsed data
- Normalize text before processing
- Strip unwanted characters from strings

---

## ⚠️ Notes

- Text must be a string
- Default behavior removes all whitespace characters (spaces, tabs, newlines)
- Only trims from beginning and end, not from middle
- Empty characters parameter defaults to whitespace
- Multiple character types can be specified (e.g., ".,-")
