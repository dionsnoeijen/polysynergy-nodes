
# 🎲 Random Data Node

The `Random Data` node is part of the **data** category and generates random data based on the selected type.

---

## ✅ Functionality

This node generates random data depending on the selected `type`. It supports generating a variety of random values, including names, emails, UUIDs, text, numbers (integer and float), dates, and company names.

---

## 🔌 Inputs

| Name    | Type    | Required | Description                                     |
|---------|---------|----------|-------------------------------------------------|
| type    | string  | Yes      | The type of random data to generate. Possible values: `name`, `email`, `uuid`, `text`, `int`, `float`, `date`, `company`. |
| min     | int     | Yes      | The minimum value for numbers (for `int` and `float` types). |
| max     | int     | Yes      | The maximum value for numbers (for `int` and `float` types). |

---

## 🔀 Outputs

| Name        | Type        | Description                                    |
|-------------|-------------|------------------------------------------------|
| true_path   | string, int, float, or date | The generated random value based on the selected `type`. |
| false_path  | dict        | Error information if failure (e.g., unsupported type or invalid input). |

---

## 💡 Example

### Input:
```json
{
  "type": "name",
  "min": 0,
  "max": 100
}
```

### Output via `true_path`:
```json
{
  "true_path": "John Doe"
}
```

---

## ⚠️ Notes

- The `type` input determines the kind of data that will be generated. If an unsupported type is provided, the node will output an error message via `false_path`.
- For number types (`int` and `float`), the `min` and `max` inputs define the range for random generation.
- The `date` type generates a random date between 1 year ago and the current date, formatted in ISO format.
- This node uses external libraries (`Faker` and `uuid`) to generate the data, so the results will vary on each execution.

---

## 🔧 Dependencies

- `random` (for generating random numbers)
- `uuid` (for generating UUIDs)
- `Faker` (for generating random text, names, emails, and more)
