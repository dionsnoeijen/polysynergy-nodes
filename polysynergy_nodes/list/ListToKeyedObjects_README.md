# 🔑 List to Keyed Objects Node

The `List to Keyed Objects` node transforms a simple list into a list of objects with a specified key name, enabling structured data formatting.

---

## 📂 Category

**list**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| input_list  | list   | ✅        | List of values to transform              |
| key_name    | str    | ❌        | Key name for objects (default: "value")  |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | list      | List of keyed objects                       |
| false_path  | dict      | Error if transformation fails               |

---

## ✅ Examples

### Default Key Name:
```json
{
  "input_list": ["apple", "banana", "cherry"]
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
  "input_list": ["apple", "banana", "cherry"],
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

### Numeric Data:
```json
{
  "input_list": [100, 200, 300],
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

### Complex Values:
```json
{
  "input_list": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "key_name": "user"
}
```
**Output:**
```json
[
  {"user": {"id": 1, "name": "Alice"}},
  {"user": {"id": 2, "name": "Bob"}}
]
```

---

## 🎯 Use Cases

- **API Response Formatting**: Structure data for API responses
- **Data Normalization**: Standardize list formats
- **JSON Schema Compliance**: Match specific JSON schemas
- **Database Record Preparation**: Format data for insertion

---

## 🔄 Transformation Pattern

```
Input:  ["a", "b", "c"]
           ↓ (key_name: "item")
Output: [{"item": "a"}, {"item": "b"}, {"item": "c"}]
```

---

## 📊 Comparison with Similar Nodes

| Feature | List to Keyed Objects | Wrap List Values |
|---------|----------------------|------------------|
| **Error Handling** | Returns error dict | Returns empty list |
| **Validation** | Strict type checking | Graceful fallback |
| **Key Validation** | Requires non-empty string | Uses default if invalid |
| **Use Case** | Production pipelines | Flexible transformations |

---

## 💡 Integration Examples

### Prepare for Database:
```
Query Results → List to Keyed Objects(key="record") → Bulk Insert
```

### API Response:
```
IDs → List to Keyed Objects(key="user_id") → JSON Response
```

### Data Pipeline:
```
Raw Data → List to Keyed Objects(key="data") → Process → Store
```

---

## ⚠️ Notes

- **Input Validation**: Requires valid list input
- **Key Validation**: Key name must be non-empty string
- **Error Handling**: Returns structured error in `false_path`
- **Default Key**: Uses "value" if key_name not specified
- **Type Preservation**: Original item types preserved in objects
