# 🏗️ JSON Example to Response Model Node

The `JSON Example to Response Model` node dynamically creates a Pydantic BaseModel from an example JSON structure. Perfect for generating response schemas for AI agents and API validation.

---

## 📂 Category

**pydantic**

---

## ⚙️ Inputs

| Name          | Type          | Required | Description                              |
|---------------|---------------|----------|------------------------------------------|
| example_json  | str \| dict \| list | ✅  | Example JSON to infer schema from        |
| model_name    | str           | ❌        | Name for model (default: DynamicModel)   |
| make_optional | bool          | ❌        | Make all fields optional (default: false) |

---

## 🔌 Outputs

| Name            | Type       | Description                              |
|-----------------|------------|------------------------------------------|
| response_model  | BaseModel  | Generated Pydantic model                 |

---

## ✅ Examples

### Simple Object:
```json
{
  "example_json": {
    "name": "John Doe",
    "age": 30,
    "active": true
  },
  "model_name": "User"
}
```

**Generated Model:**
```python
class User(BaseModel):
    name: str
    age: int
    active: bool
```

### Nested Object:
```json
{
  "example_json": {
    "user": {
      "id": 123,
      "email": "user@example.com"
    },
    "items": ["item1", "item2"]
  },
  "model_name": "OrderResponse"
}
```

**Generated Model:**
```python
class UserModel(BaseModel):
    id: int
    email: str

class OrderResponse(BaseModel):
    user: UserModel
    items: List[str]
```

### Optional Fields:
```json
{
  "example_json": {
    "title": "Article",
    "content": "Lorem ipsum"
  },
  "make_optional": true
}
```

**Generated Model:**
```python
class DynamicModel(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
```

---

## 🔍 Type Inference

The node automatically infers types from example values:

| Example Value | Inferred Type |
|---------------|---------------|
| `"text"` | `str` |
| `123` | `int` |
| `45.67` | `float` |
| `true` | `bool` |
| `{"key": "value"}` | Nested `BaseModel` |
| `["item1", "item2"]` | `List[str]` |
| `[{"id": 1}]` | `List[NestedModel]` |
| `null` | `Any` |

---

## 🎯 Common Use Cases

### Agno Agent Responses:
```
JSON Example to Response Model → Agent (response_model=model)
```

### API Response Validation:
```
API Call → JSON Example to Response Model → Validate Response
```

### Dynamic Schema Generation:
```
User Input → JSON Example to Response Model → Create Schema
```

---

## 🔄 Nested Structure Support

**Deep Nesting:**
```json
{
  "user": {
    "profile": {
      "address": {
        "city": "NYC",
        "zip": "10001"
      }
    }
  }
}
```

**Generates:**
```python
class AddressModel(BaseModel):
    city: str
    zip: str

class ProfileModel(BaseModel):
    address: AddressModel

class DynamicModel(BaseModel):
    user: ProfileModel
```

---

## 💡 Features

- **Auto Type Inference**: Detects types from example data
- **Nested Objects**: Supports arbitrary nesting depth
- **List Support**: Handles arrays of primitives or objects
- **Optional Fields**: Configurable field requirements
- **Service Node**: Provides model instance for injection

---

## ⚠️ Notes

- **Example Must Be Object**: Root level must be JSON object (dict), not array
- **First Item Inference**: For lists, type inferred from first element
- **Field Names**: JSON keys become model field names
- **Service Node**: Extends ServiceNode for dependency injection
- **Module Context**: Properly sets `__module__` to avoid KeyErrors
