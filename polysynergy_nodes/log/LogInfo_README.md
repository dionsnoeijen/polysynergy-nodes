# Log Info Node

The **Log Info** node is used to write informational messages to the system log.

---

## 🧠 Purpose

This node allows you to add custom informational log entries during the execution of a flow.  
It's useful for debugging or monitoring purposes — especially when tracing what values are passing through the system.

---

## 🔌 Inputs

| Name     | Type | Required | Description             |
|----------|------|----------|-------------------------|
| message  | str  | ✅       | The message to log.     |

---

## ⚙️ Behavior

When the node is executed, it logs the message using Python’s standard logging at the `INFO` level.

---

## ✅ Example

### Input
```json
message: "Fetching data from endpoint X"
```

### Log Output
```
INFO:root:Fetching data from endpoint X
```

---

## 🧪 Tip

- You can connect this node to critical stages of your flows to verify which branches are active.
- Combine with conditionals or switches to trace unexpected execution paths.
