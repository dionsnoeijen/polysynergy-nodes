# 🎯 To Node

The `To` node serves as a jump target for Jump nodes. It's a marker node that does nothing by itself but enables flow control via Jump operations.

---

## 📂 Category

**jump**

---

## ⚙️ Functionality

The `To` node is a **passive marker** that:
- Has no inputs or outputs
- Performs no operations
- Acts as a jump destination
- Must be named for Jump nodes to target it

---

## 💡 Purpose

Jump nodes require a "To" node as their destination:
```
Node A → Jump(to="TargetLabel") → To[TargetLabel] → Node B
```

Without the "To" node, Jump will fail with an error.

---

## ✅ Example Usage

### Simple Jump Target:
```
Error Handler → Process → Jump(to="Retry")
                          ↓
                       To[Retry] → API Call
```

### Multiple Jump Targets:
```
Router → Jump(to="Path1") → To[Path1] → Process A
      → Jump(to="Path2") → To[Path2] → Process B
      → Jump(to="Path3") → To[Path3] → Process C
```

---

## 🎯 Naming Convention

Give "To" nodes descriptive names that indicate their purpose:
- ✅ `To[RetryAPI]`
- ✅ `To[ErrorHandler]`
- ✅ `To[StartProcess]`
- ❌ `To[Node1]`
- ❌ `To[X]`

---

## 🔄 Common Patterns

### Retry Loop:
```
To[Retry] → API Call → Success?
               ↓ Fail
           Jump(to="Retry", max_retries=3)
```

### Error Recovery:
```
Risky Operation → Error? → Jump(to="ErrorHandler")
                  ↓ Success
               Continue Flow
                  ↓
            To[ErrorHandler] → Log Error → Cleanup
```

### State Machine:
```
To[StateA] → Process → Jump(to="StateB")
To[StateB] → Evaluate → Jump(to="StateC" or "StateA")
To[StateC] → Finalize → End
```

---

## ⚠️ Notes

- **No Execution**: The `To` node itself does nothing
- **Required for Jumps**: Jump nodes will fail without a matching "To" node
- **Node Type Check**: Jump validates target is a "To" node type
- **Disabled by Default**: Cannot be manually disabled (has_enabled_switch=False)
- **Name Matching**: Jump finds "To" nodes by their configured name
