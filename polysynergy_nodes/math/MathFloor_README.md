# 🧮 Floor Node

The `Floor` node is part of the **math** category and returns the **largest integer less than or equal to** a given numeric input.

---

## ✅ Functionality

This node applies the mathematical `floor()` function to the provided input, returning the nearest **lower-bound integer**.

---

## 🔌 Inputs

| Name    | Type             | Required | Description                          |
|---------|------------------|----------|--------------------------------------|
| value   | int, float, str  | Yes      | The value to be floored. Can be a number or a numeric string. |

---

## 🔀 Outputs

| Name        | Type    | Description                   |
|-------------|---------|-------------------------------|
| true_path   | int     | The floored integer result.   |
| false_path  | dict    | Error information if failure. |

---

## 💡 Example

### Input:
```json
"value": 3.75
```

### Output via `true_path`:
```json
3
```

---

## ⚠️ Notes

- If `value` is a string, it will be parsed into a number first.
- If parsing fails, the node outputs via `false_path`.

