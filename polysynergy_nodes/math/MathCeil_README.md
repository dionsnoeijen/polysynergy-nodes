# Ceil Node

The **Ceil** node rounds a number up to the nearest whole number using the mathematical `ceil` function.

---

## 🧠 Description

This node accepts a numeric input (integer, float, or numeric string) and returns the smallest integer greater than or equal to that number.

It is useful when you want to round up values, such as pricing calculations, pagination, or buffer time adjustments.

---

## 🧩 Category
`math`

---

## 📥 Inputs

| Name   | Type              | Required | Description                                 |
|--------|-------------------|----------|---------------------------------------------|
| value  | int / float / str | ✅        | The number to round up (can be a string).   |

---

## 📤 Outputs

| Name        | Type        | Description                          |
|-------------|-------------|--------------------------------------|
| true_path   | int         | The rounded-up integer value.        |
| false_path  | dict / bool | Error information if something fails.|

---

## 🔁 Flow Control

- **true_path** — triggered with the rounded value when execution succeeds.
- **false_path** — triggered if the input is invalid or cannot be parsed as a number.

---

## ⚠️ Errors

If the input cannot be parsed into a number, the node will trigger the `false_path` and provide an error message.

---

## ✅ Example

**Input:**

```json
{
  "value": "3.2"
}
```

**Output:**

```json
{
  "true_path": 4
}
```

---

## 🛠️ Internals

This node uses the `math.ceil()` function and a shared utility `to_number()` to handle numeric conversion.
