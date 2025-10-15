# 📝 String Format Node

The `String Format` node formats a template string with provided values using Python's format string syntax. Supports both positional (`{}`) and named (`{key}`) placeholders.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type        | Required | Description                              |
|------------|-------------|----------|------------------------------------------|
| template   | str         | ✅        | Template with {} or {key} placeholders   |
| values     | dict \| list | ✅        | Values for placeholders                  |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The formatted string                        |
| false_path  | dict      | Error information if formatting fails       |

---

## ✅ Examples

### Named Placeholders (Dictionary):
```json
{
  "template": "Hello {name}, you have {count} new messages",
  "values": {
    "name": "Alice",
    "count": 5
  }
}
```
**Output:** `"Hello Alice, you have 5 new messages"`

### Positional Placeholders (List):
```json
{
  "template": "Result: {} + {} = {}",
  "values": [2, 3, 5]
}
```
**Output:** `"Result: 2 + 3 = 5"`

---

## 🎯 Placeholder Types

### Named Placeholders
Use a dictionary with `{key}` syntax:
- `"Hello {name}"` with `{"name": "Bob"}` → `"Hello Bob"`

### Positional Placeholders
Use a list with `{}` syntax:
- `"{} and {}"` with `["cats", "dogs"]` → `"cats and dogs"`

---

## 💡 Use Cases

- Generate dynamic messages
- Create formatted reports
- Build URL strings with parameters
- Construct email templates

---

## ⚠️ Notes

- Template must be a string
- Values must be either a dictionary or list
- Missing keys/indices will trigger the `false_path`
- Use `{{` and `}}` to escape braces in the template
