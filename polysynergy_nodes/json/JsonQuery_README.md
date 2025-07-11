# JSON Query Node

This node allows querying JSON data using **JMESPath**, a powerful query language for JSON, similar to XPath for XML.

## **Category:** Transformation

## **Description**
The **JSON Query** node extracts data from a JSON input using a **JMESPath query**.  
**[Full Documentation](https://jmespath.org/)** _(opens in a new tab)_
It supports both **raw JSON strings** and **JSON objects (dicts)** as input and returns results as both **a string and a dictionary**.

## **Variables**

| Name                 | Type  | Input | Output | Description |
|----------------------|-------|-------|--------|-------------|
| `json_input_as_dict` | dict  | ✅     | ❌      | JSON input as a Python dictionary. |
| `json_input_as_string` | str   | ✅     | ❌      | JSON input as a raw string. |
| `query`             | str   | ✅     | ❌      | JMESPath query used to extract data. |
| `result_as_string`  | str   | ❌     | ✅      | Query result formatted as a JSON string. |
| `result_as_dict`    | dict  | ❌     | ✅      | Query result as a Python dictionary. |

## **Flow Control**
- **`false_path` (bool)** – triggered if the query fails due to invalid JSON or an incorrect query.

## **How It Works**
1. The node receives either:
   - A JSON object (`json_input_as_dict`), or  
   - A JSON string (`json_input_as_string`).
2. If a JSON object is provided, it takes priority. Otherwise, the string is parsed into JSON.
3. The **JMESPath query** is executed on the JSON input.
4. The result is stored as:
   - `result_as_string` (formatted JSON string)
   - `result_as_dict` (direct Python dictionary output)
5. If an error occurs, `false_path` is triggered, and an error message is returned.

## **Example Usage**

### **Example 1: Filtering Items**
#### **JSON Input**
```json
{
    "items": [
        {"name": "Apple", "price": 10},
        {"name": "Orange", "price": 25},
        {"name": "Banana", "price": 30}
    ]
}
```

#### **JMESPath Query**
```jmespath
items[?price > 20].name
```

#### **Result**
- **`result_as_string`**:
  ```json
  [
      "Orange",
      "Banana"
  ]
  ```
- **`result_as_dict`**:
  ```python
  ["Orange", "Banana"]
  ```

---

### **Example 2: Extracting Nested Data**
#### **JSON Input**
```json
{
    "users": [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25}
    ]
}
```

#### **JMESPath Query**
```jmespath
users[*].name
```

#### **Result**
- **`result_as_string`**:
  ```json
  [
      "Alice",
      "Bob"
  ]
  ```
- **`result_as_dict`**:
  ```python
  ["Alice", "Bob"]
  ```

## **Error Handling**
- If **invalid JSON** is provided in `json_input_as_string`, the node sets:
  - `result_as_string = "Error: Invalid JSON string input"`
  - `result_as_dict = {}`
  - `false_path = True`
- If the **query fails**, an error message is returned.

## **Use Cases**
✔ Extracting structured data from JSON responses.  
✔ Filtering and selecting specific fields in API responses.  
✔ Querying nested objects efficiently in workflows.  
✔ Creating dynamic conditions based on JSON content.

---

🚀 **Now you can extract and manipulate JSON easily using JMESPath!**