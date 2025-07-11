# ➗ Divide Node

The **Divide** node performs a mathematical division between two input values, `a` and `b`. It is part of the **math** category.

---

## ✅ Function
Divides value `a` by value `b` and returns the result.

---

## 🔌 Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `a` | int / float / str | Yes | Dividend. Will be converted to number if possible. |
| `b` | int / float / str | Yes | Divisor. Will be converted to number. Must not be 0. |

---

## 🔀 Outputs

| Name | Type | Description |
|------|------|-------------|
| `true_path` | float | Result of the division `a / b`. |
| `false_path` | dict | Contains error info if conversion or division fails. |

---

## ⚠️ Notes
- If either `a` or `b` is not a number or can't be converted to one, the node returns an error.
- Division by zero raises a clear error message.
- Strings will be automatically parsed to numbers when possible.

---

## 📌 Example

### Input:
```json
{
  "a": "10",
  "b": "2"
}
```

### Output:
```json
true_path: 5.0
```

---

## 🧠 Internals
- Uses a shared utility function `to_number()` to normalize input.
- Uses `PathSettings` for both success and error handling.

---

## 💡 Use Cases
- Arithmetic in automation flows
- Derived values from datasets
- Simplifying preconditions for later processing steps
