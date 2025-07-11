# 🔢 MathAbsolute Node

The `MathAbsolute` node calculates the **absolute value** of a given input. This means that any negative number is converted to its positive counterpart.

---

## 📂 Category
**math**

---

## ✅ Functionality

This node accepts a numeric value (or a string that represents a number) and returns its absolute value.

---

## 🔌 Inputs

| Name   | Type              | Required | Description                                          |
|--------|-------------------|----------|------------------------------------------------------|
| value  | int / float / str | ✅        | The input value from which to compute the absolute value. |

---

## 🔀 Outputs

| Name        | Type        | Description                                |
|-------------|-------------|--------------------------------------------|
| true_path   | int / float | The absolute value of the input.           |
| false_path  | dict / bool | An error message if the input is invalid.  |

---

## ⚠️ Error Handling

If the input cannot be converted to a number, `false_path` is triggered with an error message.

---

## 🧠 Example

### Input
```json
{ "value": "-42" }
```

### Output
```json
{ "true_path": 42 }
```

---

## 🧪 Notes
- Supports both string and numeric inputs.
- Useful for calculations where only positive values make sense, such as distances, amounts, etc.
