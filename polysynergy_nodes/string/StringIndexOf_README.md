# 🎯 String Index Of Node

The `String Index Of` node finds the position of a substring within text. Supports finding first or last occurrence and starting from a specific position.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to search in                    |
| search     | str    | ✅        | The substring to find                    |
| start      | int    | ❌        | Starting position (default: 0)           |
| find_last  | bool   | ❌        | Find last occurrence (default: false)    |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | int       | Index position (-1 if not found)            |
| false_path  | dict      | Error information if search fails           |

---

## ✅ Examples

### Find First Occurrence:
```json
{
  "text": "hello world, hello universe",
  "search": "hello",
  "find_last": false
}
```
**Output:** `0`

### Find Last Occurrence:
```json
{
  "text": "hello world, hello universe",
  "search": "hello",
  "find_last": true
}
```
**Output:** `13`

### Search from Position:
```json
{
  "text": "abcabcabc",
  "search": "abc",
  "start": 3
}
```
**Output:** `3`

### Not Found:
```json
{
  "text": "hello world",
  "search": "goodbye"
}
```
**Output:** `-1`

---

## 💡 Use Cases

- Find character positions for substring extraction
- Locate delimiters in formatted text
- Validate text structure
- Parse structured data

---

## ⚠️ Notes

- Returns `-1` when substring is not found (not an error)
- Both text and search must be strings
- Start position can be used to find multiple occurrences
- Negative start positions are supported (counts from end)
