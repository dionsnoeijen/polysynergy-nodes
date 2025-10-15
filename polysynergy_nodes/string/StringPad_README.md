# ↔️ String Pad Node

The `String Pad` node pads a string to a specified width using a fill character. Supports left padding (rjust), right padding (ljust), and centering.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to pad                          |
| width      | int    | ✅        | Total width of the padded string         |
| fill_char  | str    | ❌        | Character to use for padding (default: space) |
| pad_type   | str    | ❌        | Padding type: left, right, center (default: left) |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The padded string                           |
| false_path  | dict      | Error information if padding fails          |

---

## ✅ Examples

### Left Padding (rjust):
```json
{
  "text": "42",
  "width": 5,
  "fill_char": "0",
  "pad_type": "left"
}
```
**Output:** `"00042"`

### Right Padding (ljust):
```json
{
  "text": "Name",
  "width": 10,
  "fill_char": ".",
  "pad_type": "right"
}
```
**Output:** `"Name......"`

### Center Padding:
```json
{
  "text": "TITLE",
  "width": 15,
  "fill_char": "=",
  "pad_type": "center"
}
```
**Output:** `"=====TITLE====="`

---

## 🎯 Pad Types

- **left** (rjust): Pads on the left side - useful for number formatting
- **right** (ljust): Pads on the right side - useful for aligning text
- **center**: Pads on both sides - useful for titles and headers

---

## 💡 Use Cases

- Format fixed-width text output
- Align text in tables or reports
- Add leading zeros to numbers
- Create ASCII art borders

---

## ⚠️ Notes

- Text must be a string
- Fill character must be exactly one character
- If text is already wider than specified width, it is returned unchanged
- Default fill character is space (" ")
