# ✂️ String Substring Node

The `String Substring` node extracts a portion of text using start and end indices. Supports negative indices for counting from the end.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type      | Required | Description                              |
|------------|-----------|----------|------------------------------------------|
| text       | str       | ✅        | The text to extract from                 |
| start      | int       | ❌        | Starting index (default: 0)              |
| end        | int \| None | ❌        | Ending index (default: None = end of string) |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The extracted substring                     |
| false_path  | dict      | Error information if extraction fails       |

---

## ✅ Examples

### Extract from Start:
```json
{
  "text": "Hello World",
  "start": 0,
  "end": 5
}
```
**Output:** `"Hello"`

### Extract to End:
```json
{
  "text": "Hello World",
  "start": 6
}
```
**Output:** `"World"`

### Extract from Middle:
```json
{
  "text": "Hello World",
  "start": 3,
  "end": 8
}
```
**Output:** `"lo Wo"`

### Negative Indices (from End):
```json
{
  "text": "Hello World",
  "start": -5,
  "end": -1
}
```
**Output:** `"Worl"`

### Last Characters:
```json
{
  "text": "filename.txt",
  "start": -3
}
```
**Output:** `"txt"`

---

## 📊 Index Behavior

- **Positive indices**: Count from the start (0-based)
- **Negative indices**: Count from the end (-1 is last character)
- **None as end**: Extract to the end of the string
- **Out of bounds**: Python handles gracefully, no error

---

## 💡 Use Cases

- Extract file extensions
- Get first/last N characters
- Parse structured text fields
- Implement substring search logic

---

## ⚠️ Notes

- Text must be a string
- Uses Python slice notation: `text[start:end]`
- Start is inclusive, end is exclusive
- Negative indices are supported and count from the end
- Out-of-range indices are handled gracefully
