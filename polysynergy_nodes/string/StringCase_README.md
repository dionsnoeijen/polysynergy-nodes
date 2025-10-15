# 🔤 String Case Node

The `String Case` node converts text to different case formats including uppercase, lowercase, title case, and capitalize first letter.

---

## 📂 Category

**string**

---

## ⚙️ Inputs

| Name       | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| text       | str    | ✅        | The text to transform                    |
| case_type  | str    | ✅        | Case format: upper, lower, title, capitalize |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The text transformed to the selected case   |
| false_path  | dict      | Error information if transformation fails   |

---

## ✅ Example

### Input:
```json
{
  "text": "hello world",
  "case_type": "title"
}
```

### Output:
```json
"Hello World"
```

---

## 🎯 Case Types

- **upper**: CONVERTS TO UPPERCASE
- **lower**: converts to lowercase
- **title**: Converts To Title Case (First Letter Of Each Word)
- **capitalize**: Converts to sentence case (first letter only)

---

## ⚠️ Notes

- Input must be a string type
- Invalid case types will trigger the `false_path`
- Non-string inputs will return an error
