
# 🧮 Modulus Node

The `Modulus` node is part of the **math** category and returns the **remainder** when one number is divided by another.

---

## ✅ Functionality

This node applies the mathematical `modulus` function to the provided inputs `a` and `b`, returning the remainder of the division `a % b`.

---

## 🔌 Inputs

| Name    | Type             | Required | Description                                    |
|---------|------------------|----------|------------------------------------------------|
| a       | int, float, str   | Yes      | The dividend. Can be a number or a numeric string. |
| b       | int, float, str   | Yes      | The divisor. Can be a number or a numeric string. |

---

## 🔀 Outputs

| Name        | Type    | Description                               |
|-------------|---------|-------------------------------------------|
| true_path   | int, float | The result of `a % b` (the remainder). |
| false_path  | dict    | Error information if failure.             |

---

## 💡 Example

### Input:
```json
{
  "a": 10,
  "b": 3
}
```

### Output via `true_path`:
```json
{
  "true_path": 1
}
```

---

## ⚠️ Notes

- If `a` or `b` are strings, they will be parsed into numbers first.
- If parsing fails, the node outputs via `false_path` with an appropriate error message.
- If `b` is zero, the operation will raise a division-by-zero error.
