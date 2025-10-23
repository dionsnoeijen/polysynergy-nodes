# Dict Pop

Removes and returns a key-value pair from a dictionary, similar to Python's `dict.pop()` method.

## Configuration

The node can be configured through the following inputs:

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| Input Dict | `dict` \| `str` \| `bytes` | The dictionary to pop from. Accepts dict objects, JSON strings, or bytes |
| Key | `str` | The key to remove from the dictionary |
| Default Value | `any` | Value to return if the key doesn't exist (default: None) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Popped Value | `any` | The value that was removed from the dict (or default if key didn't exist) |
| Remaining Dict | `dict` | The dictionary without the popped key |
| Key Existed | `bool` | Whether the key was present in the dictionary |

## Examples

### Example 1: Pop Existing Key

**Input Dict:**
```json
{
  "id": 123,
  "text": "Hello world",
  "author": "John"
}
```

**Key:** `"text"`

**Result:**
- Popped Value: `"Hello world"`
- Remaining Dict: `{"id": 123, "author": "John"}`
- Key Existed: `true`

### Example 2: Pop Non-Existent Key with Default

**Input Dict:**
```json
{
  "id": 123,
  "author": "John"
}
```

**Key:** `"text"`
**Default Value:** `"No text"`

**Result:**
- Popped Value: `"No text"`
- Remaining Dict: `{"id": 123, "author": "John"}`
- Key Existed: `false`

### Example 3: From HTTP Request (JSON bytes)

HTTP Request returns JSON as bytes → Dict Pop

The node automatically parses JSON strings and bytes to dictionaries.

## Notes

- The original dictionary is not modified (a copy is made)
- If the key exists, it is removed and its value is returned via true_path
- If the key doesn't exist, the default value is returned via true_path
- The `key_existed` output allows you to check whether the key was actually in the dict
- Handles JSON strings and bytes input automatically (useful for HTTP responses)
- Only uses false_path for actual errors (invalid JSON, not a dict, etc.)

## Category

**dict** - Dictionary manipulation operations
