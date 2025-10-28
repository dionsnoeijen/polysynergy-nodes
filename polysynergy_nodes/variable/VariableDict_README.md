# Variable Dict

Combines and manipulates dictionaries with support for smart list operations.

## Parameters

- **value**: Base dictionary (can be connected or manually entered)
- **merge**: Dictionary to merge into value
- **wrap**: Wrap multiple dicts under keys
- **operation**: How to merge (default: "merge")

## Operation Modes

### Merge (default)
Updates dictionary keys. If a key exists, it overwrites the value.

**Example:**
```
value:  {"name": "Alice", "items": ["milk"]}
merge:  {"name": "Bob", "age": 25}
result: {"name": "Bob", "age": 25, "items": ["milk"]}
```

### Append/Extend
Smart list operations that automatically detect whether to append or extend.

**Append (single item):**
```
value:  {"shopping_list": ["milk"]}
merge:  {"shopping_list": "eggs"}
result: {"shopping_list": ["milk", "eggs"]}
```

**Extend (multiple items):**
```
value:  {"shopping_list": ["milk"]}
merge:  {"shopping_list": ["eggs", "bread"]}
result: {"shopping_list": ["milk", "eggs", "bread"]}
```

**Fallback to merge (non-list):**
```
value:  {"counter": 5}
merge:  {"counter": 10}
result: {"counter": 10}  // Not a list, so overwrites
```

## Use Cases

### Session State with Agno Agents
Perfect for mutating session state in Agno agent path tools:

```
[Agent session_state={"shopping_list": ["milk"]}]
  ↓
[Path Tool] → injects session_state automatically
  ↓
[Variable Dict]
  operation: "append_or_extend"
  value: session_state (connected from path tool)
  merge: {"shopping_list": "eggs"}
  ↓
Result: {"shopping_list": ["milk", "eggs"]}

Agent session_state updated by reference!
```

### Combining Multiple Dicts
```
[Dict A] → merge
[Dict B] → merge
[Dict C] → merge
  ↓
[Variable Dict] combines all into one
```

### Wrapping Dicts Under Keys
```
wrap:
  user: {name: "Alice", age: 25}
  settings: {theme: "dark"}
  ↓
result: {
  user: {name: "Alice", age: 25},
  settings: {theme: "dark"}
}
```

## Backwards Compatibility

Default operation is "merge" - existing flows work unchanged.
