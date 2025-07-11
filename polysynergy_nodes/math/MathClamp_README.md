# 🧮 MathClamp Node

The **MathClamp** node restricts a numeric value within a given minimum and maximum range.

---

## ✅ Functionality

This node receives a value and two bounds (`min_value`, `max_value`) and clamps the value to stay within those limits.

---

## 🔌 Inputs

| Name        | Type              | Required | Description                                |
|-------------|-------------------|----------|--------------------------------------------|
| `value`     | int, float, str    | ✅       | The value to clamp. Can be a number or string. |
| `min_value` | int, float, str    | ✅       | Lower boundary of the clamping range.      |
| `max_value` | int, float, str    | ✅       | Upper boundary of the clamping range.      |

---

## 🔀 Outputs

| Name         | Type              | Description                        |
|--------------|-------------------|------------------------------------|
| `true_path`  | int, float        | The clamped numeric result.        |
| `false_path` | dict              | Error information, if conversion or logic fails. |

---

## 🧠 Logic

- Converts all inputs using a `to_number` utility.
- Returns `false_path` if any of the inputs can't be converted.
- Otherwise returns:  
  `max(min_value, min(value, max_value))`

---

## 📌 Example

If you input:

```json
{
  "value": 120,
  "min_value": 0,
  "max_value": 100
}
```

Then `true_path` will return:

```json
100
```
