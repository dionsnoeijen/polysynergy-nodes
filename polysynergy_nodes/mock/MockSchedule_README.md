
# 🗓️ Mock Schedule Node

The `Mock Schedule` node is part of the **mock** category and is automatically placed at the beginning of a schedule flow. This node cannot be removed or used elsewhere, ensuring that every schedule flow starts with it.

---

## ✅ Functionality

This node is used to initiate a schedule flow. It has a `true_path` output that signifies whether the schedule is ready to be executed. It cannot be removed or repurposed, ensuring that the flow always begins with this node.

---

## 🔌 Inputs

This node does not take any inputs.

---

## 🔀 Outputs

| Name        | Type     | Description                                  |
|-------------|----------|----------------------------------------------|
| true_path   | bool     | This value indicates that the schedule flow is ready to proceed. |

---

## 💡 Example

### Input:
```json
{}
```

### Output via `true_path`:
```json
{
  "true_path": true
}
```

---

## ⚠️ Notes

- This node is always the first node in a schedule flow and cannot be deleted or reused for other purposes.
- The node outputs a boolean value `true_path` to indicate that the flow is ready to proceed.
- This node includes a play button (`has_play_button=True`) to allow the flow to be initiated from the schedule node.
- It does not accept any other inputs or produce any additional outputs.

---

## 🔧 Dependencies

- **PathSettings**: Defines the `true_path` output which signals when the schedule flow can proceed.
