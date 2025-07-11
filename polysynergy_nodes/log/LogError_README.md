# 🪵 Log Error Node

The **Log Error** node is part of the `log` category.  
It allows you to log an error-level message to the system logger.

---

## ✅ Functionality

This node writes a message to the log with **error severity**.  
It can be used to track runtime failures, exceptional cases, or diagnostics inside your node flow.

---

## 🔌 Inputs

| Name      | Type | Required | Description                    |
|-----------|------|----------|--------------------------------|
| `message` | str  | ✅        | The message to be logged.      |

---

## 🚫 Outputs

This node does not output data. It is used solely for logging side-effects.

---

## 🛠 Example

If you provide:

```json
"Something went wrong while processing payment"
```

You will get a log entry similar to:

```bash
[ERROR] Something went wrong while processing payment
```

---

## 📘 Notes

- The log output depends on your system's logging configuration (e.g., stdout, file logging, etc.).
- It’s useful in conjunction with error-handling branches in your flows.

---

