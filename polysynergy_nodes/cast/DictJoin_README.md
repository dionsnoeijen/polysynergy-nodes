# Dict Join

Joins dictionary key-value pairs into a string with configurable separators.

## Inputs

- **Dictionary** (required): The dictionary to join into a string
- **Item Separator** (default: "&"): Separator between items
- **Key-Value Separator** (default: "="): Separator between key and value. Leave empty for values only.
- **Skip Empty** (default: true): Skip null or empty string values

## Flow Control

- **True Path (Result)**: The joined string
- **False Path (Error)**: Error if input is not a dictionary

## Behavior

The node iterates over all key-value pairs in the dictionary and:
1. Skips empty/null values if `skip_empty` is true
2. Converts each value to a string
3. Combines key and value with `key_value_separator` (or just value if separator is empty)
4. Joins all items with `item_separator`

## Example Usage

### Example 1: URL Query String
```
Dictionary: {"tier": "gold", "limit": "10", "offset": "0"}
Item Separator: "&"
Key-Value Separator: "="
Skip Empty: true

Result: "tier=gold&limit=10&offset=0"
```

### Example 2: Skip Empty Values
```
Dictionary: {"tier": "gold", "select": "", "limit": "10"}
Item Separator: "&"
Key-Value Separator: "="
Skip Empty: true

Result: "tier=gold&limit=10"
(select was skipped because it's empty)
```

### Example 3: CSV-like Format
```
Dictionary: {"name": "John", "age": "30", "city": "Amsterdam"}
Item Separator: ", "
Key-Value Separator: ": "
Skip Empty: true

Result: "name: John, age: 30, city: Amsterdam"
```

### Example 4: Values Only (No Keys)
```
Dictionary: {"filter1": "tier=eq.gold", "filter2": "active=eq.true"}
Item Separator: "&"
Key-Value Separator: ""
Skip Empty: true

Result: "tier=eq.gold&active=eq.true"
```

### Example 5: Pipe-Separated
```
Dictionary: {"field1": "value1", "field2": "value2", "field3": "value3"}
Item Separator: "|"
Key-Value Separator: "="
Skip Empty: true

Result: "field1=value1|field2=value2|field3=value3"
```

### Example 6: Custom Format
```
Dictionary: {"apple": "2", "banana": "5", "orange": ""}
Item Separator: " and "
Key-Value Separator: " costs $"
Skip Empty: true

Result: "apple costs $2 and banana costs $5"
(orange was skipped)
```

## Use Cases

- **URL Query Strings**: Build Supabase/API query parameters
- **CSV Generation**: Create comma-separated key-value pairs
- **Log Formatting**: Format structured data for logs
- **Configuration Strings**: Build config strings from dictionaries
- **Data Export**: Convert dict to custom string formats

## Pattern: Supabase Query Building

Build complete Supabase query strings:

```
[Variable Dict: {
  "filters": "tier=eq.gold",
  "select": "id,name,email",
  "order": "created_at.desc",
  "limit": "10"
}]
→ [Dict Join]
   - Item Separator: "&"
   - Key-Value Separator: ""
   - Skip Empty: true
→ Result: "tier=eq.gold&id,name,email&created_at.desc&10"
```

Or with key=value format:

```
[Variable Dict: {
  "tier": "gold",
  "active": "true",
  "limit": "10"
}]
→ [Dict Join]
   - Item Separator: "&"
   - Key-Value Separator: "="
   - Skip Empty: true
→ Result: "tier=gold&active=true&limit=10"
```
