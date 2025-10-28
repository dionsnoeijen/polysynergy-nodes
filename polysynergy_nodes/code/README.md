# Code Node

Execute custom Python code within your flow with full async support.

## Features

- **Dynamic Arguments**: Connect any values as arguments via the dock dictionary
- **Async Support**: Use `await` for async operations
- **Full Python Access**: No restrictions on what you can execute
- **Error Handling**: Automatic exception catching with details in `false_path`

## Usage

### Simple Calculation

```python
return x + y
```

Connect values to arguments `x` and `y`, and the result will be available in `true_path`.

### String Manipulation

```python
# Arguments: text="hello"
return text.upper()
```

### List Processing

```python
# Arguments: items=[1, 2, 3]
result = []
for item in items:
    result.append(item * 2)
return result
```

### Async Operations

```python
# Arguments: url="https://api.example.com/data"
import aiohttp

async with aiohttp.ClientSession() as session:
    response = await session.get(url)
    data = await response.json()
    return data['result']
```

### Complex Logic

```python
# Arguments: data={"users": [...]}
import json

# Process data
processed = []
for user in data['users']:
    if user['age'] > 18:
        processed.append({
            'name': user['name'],
            'email': user['email']
        })

# Return as JSON string
return json.dumps(processed)
```

## Arguments

All arguments defined in the `arguments` dock dictionary are available as local variables in your code scope.

## Return Value

Use the `return` statement to output a value. The returned value will be available in the `true_path` output.

## Error Handling

If an exception occurs during execution:
- `true_path` will be `False`
- `false_path` will contain:
  - `error`: The error message
  - `type`: The exception type name

## Notes

- The code runs in an async context, so you can use `await`
- You have access to Python's standard library
- You can import any available packages
- The code has full access to the Python environment (no sandboxing)
