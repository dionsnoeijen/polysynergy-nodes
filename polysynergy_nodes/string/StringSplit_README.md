# ✂️ String Split Node

The `String Split` node splits a text string into a list of substrings using a specified separator, with optional limit on the number of splits.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to split                        |
| separator  | str    | ❌        | String to split on (default: space)      |
| max_split  | int    | ❌        | Maximum number of splits (-1 for unlimited, default: -1) |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | list      | List of split strings                       |
| false_path  | dict      | Error information if split fails            |

---

## ✅ Examples

### Split by Space:
```json
{
  "text": "Hello World Welcome",
  "separator": " "
}
```
**Output:** `["Hello", "World", "Welcome"]`

### Split by Comma:
```json
{
  "text": "apple,banana,cherry,date",
  "separator": ","
}
```
**Output:** `["apple", "banana", "cherry", "date"]`

### Limited Splits:
```json
{
  "text": "a-b-c-d-e",
  "separator": "-",
  "max_split": 2
}
```
**Output:** `["a", "b", "c-d-e"]`

### Split Lines:
```json
{
  "text": "Line 1\nLine 2\nLine 3",
  "separator": "\n"
}
```
**Output:** `["Line 1", "Line 2", "Line 3"]`

---

## 💡 Use Cases

- Parse CSV or delimited data
- Extract tokens from text
- Break sentences into words
- Process structured input strings

---

## ⚠️ Notes

- Text and separator must be strings
- Max split of `-1` splits all occurrences (default)
- Empty separator will raise an error
- If separator not found, returns list with original text
- Consecutive separators create empty strings in the result
