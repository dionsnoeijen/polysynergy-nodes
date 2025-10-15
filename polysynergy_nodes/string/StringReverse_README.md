# ↩️ String Reverse Node

The `String Reverse` node reverses the character order of a text string.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to reverse                      |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The reversed string                         |
| false_path  | dict      | Error information if reversal fails         |

---

## ✅ Examples

### Basic Reversal:
```json
{
  "text": "Hello World"
}
```
**Output:** `"dlroW olleH"`

### Palindrome Check:
```json
{
  "text": "racecar"
}
```
**Output:** `"racecar"` (same as input)

### Reverse Numbers:
```json
{
  "text": "12345"
}
```
**Output:** `"54321"`

---

## 💡 Use Cases

- Check for palindromes
- Reverse sequences for algorithms
- Create mirror effects
- Text manipulation puzzles

---

## ⚠️ Notes

- Input must be a string type
- Reverses at character level (not word level)
- Unicode characters are properly handled
- Empty string returns empty string
