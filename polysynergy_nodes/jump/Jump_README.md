# 🚀 Jump Node

The `Jump` node transfers flow execution to a designated "To" node, enabling dynamic routing and retry logic. Supports optional retry limits with configurable timeouts.

---

## 📂 Category

**flow**

---

## ⚙️ Inputs

| Name            | Type   | Required | Description                              |
|-----------------|--------|----------|------------------------------------------|
| to              | str    | ✅        | Name of the "To" node to jump to         |
| has_max_retries | bool   | ❌        | Enable retry limit (default: false)      |
| max_retries     | int    | ❌        | Maximum retry attempts (default: 5)      |
| retry_timeout   | int    | ❌        | Seconds between retries (default: 5)     |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| false_path  | dict      | Error if jump fails or retries exceeded     |

---

## 🔀 Flow Control

The Jump node redirects execution flow to a specific "To" node:
```
Node A → Jump (to="ProcessData") → To[ProcessData] → Node B
```

---

## ✅ Example Usage

### Basic Jump:
```json
{
  "to": "DataProcessing"
}
```
Jumps to the "To" node named "DataProcessing"

### Jump with Retry Logic:
```json
{
  "to": "APICall",
  "has_max_retries": true,
  "max_retries": 3,
  "retry_timeout": 10
}
```
Attempts up to 3 times with 10-second delays

---

## 🔄 Retry Mechanism

### Retry Counter:
- Increments on each jump attempt
- Stops when `max_retries` is reached
- Triggers `false_path` when limit exceeded

### Retry Timeout:
- Waits `retry_timeout` seconds before retry
- Only applies to retries (not first attempt)
- Blocking sleep operation

---

## 💡 Use Cases

- **Error Recovery**: Jump back to retry failed operations
- **Conditional Routing**: Direct flow based on conditions
- **Loop Alternatives**: Create custom loop patterns
- **Retry Logic**: Implement retry mechanisms for unstable operations

---

## 🎯 Pattern Examples

### Retry Pattern:
```
API Call → [Fails] → Jump (to="API Call", max_retries=3)
         → [Success] → Continue
```

### Conditional Jump:
```
Check Condition → Jump (to="Path A" or "Path B")
```

### Error Handling:
```
Risky Operation → [Error] → Jump (to="Error Handler")
```

---

## ⚠️ Notes

- **Target Requirement**: Must jump to a "To" node specifically
- **Node Resurrection**: Resets nodes in the jump path for re-execution
- **Blocking Retry**: Retry timeout uses blocking sleep
- **Error Handling**: Returns error dict if target not found or wrong node type
- **Counter Persistence**: Retry counter persists across attempts
