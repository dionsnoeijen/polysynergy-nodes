# Json Combine

Combines multiple dictionaries into a single flat dictionary.  
All values in the `combine` input must be dictionaries themselves.

## **Category:** JSON

---

## **Description**
The **Json Combine** node takes a dictionary input (`combine`) where each value is expected to be a dictionary.  
It merges all of these inner dictionaries into a single combined dictionary.

If any of the values is **not** a dictionary, the node will fail and send the error to the `false_path`.

---

## **Variables**

| Name     | Type | Input | Output | Description |
|----------|------|-------|--------|-------------|
| `combine` | dict | ✅     | ❌      | A dictionary whose values are dictionaries to be merged. |

---

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | Contains the combined dictionary if all values are valid dicts. |
| `false_path` | Contains an error message if one or more values are not dicts. |

---

## **How It Works**
1. Expects an input dictionary `combine` with nested dictionaries as values.
2. Merges all inner dicts into one flat dict.
3. Returns the result via `true_path`.
4. If a value is not a dictionary, returns an error via `false_path`.

---

## **Example Usage**

### **Input**
```json
{
  "combine": {
    "a": { "foo": 1 },
    "b": { "bar": 2 },
    "c": { "baz": 3 }
  }
}
```

### **Output**
```json
{
  "foo": 1,
  "bar": 2,
  "baz": 3
}
```

### **Invalid Input**
```json
{
  "combine": {
    "a": { "foo": 1 },
    "b": "oops"
  }
}
```

### **Error Output**
```json
{
  "error": "Key 'b' does not contain a dict"
}
```

---

## **Use Cases**
✔ Merging configuration fragments  
✔ Composing API request payloads  
✔ Normalizing input data for downstream nodes