# 🔗 String Join Node

The `String Join` node joins a list of items into a single string with a specified separator.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| items      | list   | ✅        | List of items to join                    |
| separator  | str    | ❌        | String to join with (default: "")        |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The joined string                           |
| false_path  | dict      | Error information if join fails             |

---

## ✅ Examples

### Join with Comma:
```json
{
  "items": ["apple", "banana", "cherry"],
  "separator": ", "
}
```
**Output:** `"apple, banana, cherry"`

### Join without Separator:
```json
{
  "items": ["Hello", "World"],
  "separator": ""
}
```
**Output:** `"HelloWorld"`

### Join with Newline:
```json
{
  "items": ["Line 1", "Line 2", "Line 3"],
  "separator": "\n"
}
```
**Output:**
```
Line 1
Line 2
Line 3
```

### Join Mixed Types:
```json
{
  "items": ["Total:", 42, "items"],
  "separator": " "
}
```
**Output:** `"Total: 42 items"`

---

## 💡 Use Cases

- Build CSV or delimited text
- Concatenate list values into single string
- Create formatted output from arrays
- Generate file paths or URLs

---

## ⚠️ Notes

- Items must be a list
- Non-string items are automatically converted to strings
- Empty list produces empty string
- Separator defaults to empty string if not provided
