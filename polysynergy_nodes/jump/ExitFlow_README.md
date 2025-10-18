# 🛑 Exit Flow

The `Exit Flow` node is part of the `flow` category and is used to **immediately stop the entire flow execution**.

---

## 🧠 Purpose

This node stops **all flow execution**, including:
- The current branch
- All parallel branches
- All unprocessed nodes

The flow exits with **success status** (not an error).

---

## 📥 Inputs

- **Exit Message** (optional): A message describing why the flow was stopped (will be logged)
  - Default: `"Flow stopped"`

---

## 🔄 Usage

Connect this node when you want to gracefully stop the entire flow execution:
- When required data is missing
- When a validation condition fails
- When there's nothing left to process
- When early termination is desired

---

## 🧪 Examples

### Example 1: Stop on Empty Data

```
[Data Source] → [Is Not Empty] --false_path--> [Exit Flow: "No data to process"]
                                --true_path---> [Continue Processing]
```

### Example 2: Stop After Validation Failure

```
[Validate Input] --false_path--> [Exit Flow: "Validation failed"]
                 --true_path---> [Process Valid Data]
```

### Example 3: Conditional Early Exit

```
[Check Condition] → [Equal] --false_path--> [Exit Flow: "Condition not met"]
                            --true_path---> [Continue Workflow]
```

---

## 🧩 Behavior

When this node executes:
1. Logs the exit message to the console
2. Kills **all unprocessed nodes** in the flow
3. Kills **all outgoing connections** from those nodes
4. Stops execution immediately
5. Flow completes with **success status**

---

## ⚠️ Important Notes

- This node **stops the ENTIRE flow**, not just the current branch
- The flow is marked as **successful** (not failed)
- Use this for **graceful exits**, not for error handling
- All processed nodes remain processed (their results are saved)

---

## 🆚 Comparison with Other Flow Control

| Node | Scope | Status | Use Case |
|------|-------|--------|----------|
| **Exit Flow** | Entire flow | Success | Graceful early termination |
| **Break Loop** | Current loop only | N/A | Exit from loop iteration |
| **Path (false)** | Single branch | N/A | Conditional routing |

---

## 💡 Best Practices

1. **Always provide a descriptive message** to help with debugging
2. **Use for validation failures** where continuing is pointless
3. **Combine with Is Not Empty** to validate required data
4. **Don't use for error conditions** - let errors propagate naturally
