
# 📝 Note Node

The `Note` node is part of the **note** category and allows users to add and display textual information within the workflow.

---

## ✅ Functionality

This node is designed to display notes as part of the workflow, primarily for visual purposes. It allows users to add textual information that can be formatted as rich text, which is displayed directly within the user interface. The node itself does not process data or provide any functional output.

---

## 🔌 Inputs

| Name    | Type    | Required | Description                                     |
|---------|---------|----------|-------------------------------------------------|
| note    | string  | Yes      | The text value to be displayed as a note. Can be plain text or formatted as rich text. |

---

## 🔀 Outputs

This node does not produce any output values. It is purely for visual purposes and is used to display information to the user.

---

## 💡 Example

### Input:
```json
{
  "note": "This is an informational note within the workflow."
}
```

### Output:
No output is generated from this node, as it only serves to display the note text visually within the workflow.

---

## ⚠️ Notes

- The `note` input can accept both plain text and rich text formatted input.
- This node is used purely for user interface purposes and does not affect the flow of the workflow.
