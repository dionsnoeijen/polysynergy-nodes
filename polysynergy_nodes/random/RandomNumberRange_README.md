# 🔢 Random Number Range Node

The `Random Number Range` node is part of the **random** category and generates lists of random numbers with advanced configuration options.

---

## ✅ Functionality

This node creates arrays of random numbers with precise control over range, type, uniqueness, and decimal precision. Perfect for data generation, testing, simulations, and statistical sampling.

---

## 🔌 Inputs

| Name           | Type  | Required | Description                                          |
|----------------|-------|----------|------------------------------------------------------|
| count          | int   | Yes      | Number of random values to generate (minimum 1)     |
| min_value      | float | Yes      | Minimum value for generated numbers                  |
| max_value      | float | Yes      | Maximum value for generated numbers                  |
| number_type    | string| Yes      | Number type: `int` (integers) or `float` (decimals) |
| unique         | bool  | Yes      | Whether all generated numbers should be unique       |
| decimal_places | int   | Yes      | Decimal places for float type (default: 2)          |

---

## 🔀 Outputs

| Name       | Type        | Description                                    |
|------------|-------------|------------------------------------------------|
| true_path  | list        | Array of generated random numbers              |
| false_path | dict        | Error information if failure occurs           |

---

## 💡 Examples

### Basic Integer Range:
```json
{
  "count": 5,
  "min_value": 1,
  "max_value": 100,
  "number_type": "int",
  "unique": false,
  "decimal_places": 2
}
```

### Output:
```json
{
  "true_path": [23, 67, 12, 89, 45]
}
```

### Unique Float Range:
```json
{
  "count": 3,
  "min_value": 0.0,
  "max_value": 1.0,
  "number_type": "float",
  "unique": true,
  "decimal_places": 3
}
```

### Output:
```json
{
  "true_path": [0.234, 0.789, 0.456]
}
```

### Large Dataset Generation:
```json
{
  "count": 100,
  "min_value": -50,
  "max_value": 50,
  "number_type": "int",
  "unique": false,
  "decimal_places": 2
}
```

---

## ⚠️ Notes

- **Range Validation**: `min_value` must be less than `max_value`
- **Count Limits**: `count` must be at least 1
- **Unique Integers**: When generating unique integers, count cannot exceed available values in range
- **Unique Floats**: Uses attempt-based generation with 1000 retry limit to prevent infinite loops
- **Decimal Precision**: Float values are rounded to specified decimal places
- **Inclusive Ranges**: Both min and max values are included in possible results

---

## 🔧 Advanced Features

- **Negative Ranges**: Supports negative number ranges
- **High Precision**: Configurable decimal places for float generation  
- **Uniqueness Guarantee**: Ensures no duplicate values when unique=true
- **Large Datasets**: Efficiently generates large arrays of random numbers
- **Type Safety**: Strict integer/float type enforcement

---

## 🎯 Use Cases

- **Data Testing**: Generate test datasets with specific numerical ranges
- **Statistical Sampling**: Create random samples for data analysis
- **Game Development**: Generate random stats, coordinates, or game values
- **Simulation**: Create input data for mathematical simulations
- **Load Testing**: Generate random numerical data for system testing
- **Machine Learning**: Create synthetic numerical datasets for training