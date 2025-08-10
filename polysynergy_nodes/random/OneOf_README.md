
# 🎲 One Of Node

The `One Of` node is part of the **random** category and randomly selects one value from a list of provided values.

---

## ✅ Functionality

This node randomly selects one value from the provided list `values`. It uses the `random.choice()` function to make a random selection. The node outputs the selected value via the `true_path`.

---

## 🔌 Inputs

| Name    | Type    | Required | Description                                    |
|---------|---------|----------|------------------------------------------------|
| values  | list    | Yes      | A list of possible values to choose from. Can include various data types such as integers, strings, or floats. |

---

## 🔀 Outputs

| Name        | Type             | Description                          |
|-------------|------------------|--------------------------------------|
| true_path   | any              | The randomly selected value from the list. |
| false_path  | dict             | Error information if failure (e.g., if `values` is not a valid list). |

---

## 💡 Example

### Input:
```json
{
  "values": [1, 2, 3, "apple", "banana"]
}
```

### Output via `true_path`:
```json
{
  "true_path": "banana"
}
```

### Output via `false_path` (if an error occurs):
```json
{
  "false_path": {
    "error": "Values must be a non-empty list"
  }
}
```

---

## ⚠️ Notes

- The `values` input must be a non-empty list. If it is an empty list or not a list at all, an error will be generated and output via `false_path`.
- This node can handle any data type within the list (integers, strings, floats, etc.).
- The node does not process the data but simply returns one value from the list, chosen randomly.
- **Async Execution**: This node uses asynchronous execution for consistency with the framework.
- **Error Handling**: All errors are properly formatted using `NodeError.format()` for consistent error reporting.
