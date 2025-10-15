# 🔁 String Repeat Node

The `String Repeat` node repeats a text string a specified number of times, optionally with a separator between repetitions.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to repeat                       |
| count      | int    | ✅        | Number of times to repeat                |
| separator  | str    | ❌        | String to insert between repetitions (default: "") |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The repeated string                         |
| false_path  | dict      | Error information if repeat fails           |

---

## ✅ Examples

### Basic Repetition:
```json
{
  "text": "Hello",
  "count": 3
}
```
**Output:** `"HelloHelloHello"`

### Repeat with Separator:
```json
{
  "text": "🎵",
  "count": 5,
  "separator": " "
}
```
**Output:** `"🎵 🎵 🎵 🎵 🎵"`

### Create Pattern:
```json
{
  "text": "=-",
  "count": 10,
  "separator": ""
}
```
**Output:** `"=-=-=-=-=-=-=-=-=-=-=-=-=-"`

### Zero Count:
```json
{
  "text": "Hello",
  "count": 0
}
```
**Output:** `""` (empty string)

---

## 💡 Use Cases

- Create decorative borders or dividers
- Generate test data
- Build patterns or repeated elements
- Create padding or spacing

---

## ⚠️ Notes

- Text must be a string
- Count must be a non-negative integer
- Count of `0` returns an empty string
- Large count values may create very long strings
- Separator is optional and defaults to empty string
