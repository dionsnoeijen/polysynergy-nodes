
# 🧮 Multiply Node

The `Multiply` node is part of the **math** category and returns the **product** of two numbers.

---

## ✅ Functionality

This node applies the mathematical `multiplication` operation to the provided inputs `a` and `b`, returning the product of `a * b`.

---

## 🔌 Inputs

| Name    | Type             | Required | Description                                    |
|---------|------------------|----------|------------------------------------------------|
| a       | int, float, str   | Yes      | The first operand. Can be a number or a numeric string. |
| b       | int, float, str   | Yes      | The second operand. Can be a number or a numeric string. |

---

## 🔀 Outputs

| Name        | Type    | Description                               |
|-------------|---------|-------------------------------------------|
| true_path   | int, float | The result of `a * b` (the product). |
| false_path  | dict    | Error information if failure.             |

---

## 💡 Example

### Input:
```json
{
  "a": 5,
  "b": 4
}
```

### Output via `true_path`:
```json
{
  "true_path": 20
}
```

---

## ⚠️ Notes

- If `a` or `b` are strings, they will be parsed into numbers first.
- If parsing fails, the node outputs via `false_path` with an appropriate error message.
