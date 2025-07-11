
# 🧮 Power Node

The `Power` node is part of the **math** category and returns the **result** of raising one number to the power of another.

---

## ✅ Functionality

This node applies the mathematical `exponentiation` operation to the provided inputs `a` and `b`, returning the result of `a ^ b` (a raised to the power of b).

---

## 🔌 Inputs

| Name    | Type             | Required | Description                                     |
|---------|------------------|----------|-------------------------------------------------|
| a       | int, float, str   | Yes      | The base number. Can be a number or a numeric string. |
| b       | int, float, str   | Yes      | The exponent. Can be a number or a numeric string. |

---

## 🔀 Outputs

| Name        | Type    | Description                                 |
|-------------|---------|---------------------------------------------|
| true_path   | int, float | The result of `a ^ b` (a raised to the power of b). |
| false_path  | dict    | Error information if failure.               |

---

## 💡 Example

### Input:
```json
{
  "a": 2,
  "b": 3
}
```

### Output via `true_path`:
```json
{
  "true_path": 8
}
```

---

## ⚠️ Notes

- If `a` or `b` are strings, they will be parsed into numbers first.
- If parsing fails, the node outputs via `false_path` with an appropriate error message.
