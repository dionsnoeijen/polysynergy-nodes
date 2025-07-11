
# 🧮 Round Node

The `Round` node is part of the **math** category and returns the **rounded value** of a number to a specified number of decimal places.

---

## ✅ Functionality

This node applies the mathematical `round()` function to the provided `value`, rounding it to the specified number of decimal places (`decimals`).

---

## 🔌 Inputs

| Name      | Type             | Required | Description                                      |
|-----------|------------------|----------|--------------------------------------------------|
| value     | int, float, str   | Yes      | The number to be rounded. Can be a number or a numeric string. |
| decimals  | int, str          | Yes      | The number of decimal places to round to. Can be a number or a numeric string. |

---

## 🔀 Outputs

| Name        | Type    | Description                                     |
|-------------|---------|-------------------------------------------------|
| true_path   | int, float | The rounded value based on the specified decimals. |
| false_path  | dict    | Error information if failure.                   |

---

## 💡 Example

### Input:
```json
{
  "value": 10.5678,
  "decimals": 2
}
```

### Output via `true_path`:
```json
{
  "true_path": 10.57
}
```

---

## ⚠️ Notes

- If `value` or `decimals` are strings, they will be parsed into numbers first.
- If parsing fails, the node outputs via `false_path` with an appropriate error message.
