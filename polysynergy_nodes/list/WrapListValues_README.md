# 📦 Wrap List Values Node

The `Wrap List Values` node transforms a simple list into a list of objects, wrapping each value with a specified key name.

---

## 📂 Category

**list**

---

## ⚙️ Inputs

| Name      | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| items     | list   | ✅        | Input list to transform                  |
| key_name  | str    | ❌        | Key name for objects (default: "value")  |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | list      | List of objects with wrapped values         |

---

## ✅ Examples

### Basic Wrapping (Default Key):
```json
{
  "items": ["apple", "banana", "cherry"]
}
```
**Output:**
```json
[
  {"value": "apple"},
  {"value": "banana"},
  {"value": "cherry"}
]
```

### Custom Key Name:
```json
{
  "items": ["apple", "banana", "cherry"],
  "key_name": "fruit"
}
```
**Output:**
```json
[
  {"fruit": "apple"},
  {"fruit": "banana"},
  {"fruit": "cherry"}
]
```

### Numeric Values:
```json
{
  "items": [100, 200, 300],
  "key_name": "price"
}
```
**Output:**
```json
[
  {"price": 100},
  {"price": 200},
  {"price": 300}
]
```

### Mixed Types:
```json
{
  "items": [1, "text", true, {"nested": "object"}],
  "key_name": "data"
}
```
**Output:**
```json
[
  {"data": 1},
  {"data": "text"},
  {"data": true},
  {"data": {"nested": "object"}}
]
```

---

## 🔄 Transformation Logic

```
Input:  [item1, item2, item3]
           ↓
Output: [{key: item1}, {key: item2}, {key: item3}]
```

---

## 💡 Use Cases

- **API Formatting**: Prepare list data for APIs requiring object format
- **Data Normalization**: Standardize list format for processing
- **Schema Transformation**: Convert simple lists to structured objects
- **JSON Preparation**: Format data for JSON APIs

---

## 🎯 Common Patterns

### Prepare for API:
```
List → Wrap List Values(key="id") → Send to API
```

### Database Insertion:
```
Values → Wrap List Values(key="column_name") → Insert Records
```

### Object Creation:
```
IDs → Wrap List Values(key="user_id") → Create User Objects
```

---

## ⚠️ Notes

- Non-list inputs return empty list `[]`
- Works with any data type (strings, numbers, objects, etc.)
- Default key name is "value"
- No validation errors - gracefully handles invalid input
- Preserves original order
