
# ➕ MathAdd Node

The `MathAdd` node adds two numeric values together and outputs the result. It supports both integers, floats, and numeric strings (e.g. `"5"` or `"3.14"`).

---

## 📂 Category

**math**

---

## ⚙️ Inputs

| Name | Type              | Required | Description                     |
|------|-------------------|----------|---------------------------------|
| a    | int \| float \| str | ✅        | First operand to add.           |
| b    | int \| float \| str | ✅        | Second operand to add.          |

Both values can be integers, floats, or strings that represent numbers. If either value cannot be converted to a number, the node triggers the `false_path`.

---

## 🔌 Outputs

| Name        | Type              | Description                                 |
|-------------|-------------------|---------------------------------------------|
| true_path   | int \| float \| bool | The result of `a + b`, if successful.      |
| false_path  | int \| float \| bool | `True` if an error occurred.               |

---

## ✅ Example

### Input:
```json
{
  "a": "3.5",
  "b": 4
}
```

### Output:
```json
7.5
```

---

## ⚠️ Notes

- If either `a` or `b` is non-numeric and cannot be parsed, the node triggers the `false_path` and sets `true_path` to `False`.
- Internally uses a shared utility `to_number` to convert values.

---

## 🧪 Test Coverage

This node is covered by unit tests to verify:
- Addition of valid integers and floats
- Addition of numeric strings
- Error handling for non-numeric input
