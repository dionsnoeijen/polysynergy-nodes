
# ▶️ Play Node

The `Play` node is part of the **flow** category and is used to initiate a flow from a specific point, enabling the workflow to be played from that node.

---

## ✅ Functionality

This node is primarily used to start a flow from a given point in the workflow. It includes a **Play button** that can be pressed to trigger the flow execution from this node onward. The node doesn't have an output value, but it allows the user to visually control the flow with a start point.

---

## 🔌 Inputs

| Name    | Type     | Required | Description                                  |
|---------|----------|----------|----------------------------------------------|
| title   | string   | Yes      | The title or label for the node, shown to the user. |
| info    | string   | Yes      | Additional information about the node. Can be plain text or rich text formatted. |

---

## 🔀 Outputs

This node does not produce any output values. It serves as a visual marker and start point for the workflow.

---

## 💡 Example

### Input:
```json
{
  "title": "Start Flow",
  "info": "This is where the flow begins."
}
```

### Output:
No output is generated from this node, as it simply serves as the starting point in the workflow.

---

## ⚠️ Notes

- The `title` input is a simple string used as the node's label.
- The `info` input accepts both plain text and rich text formatted content.
- This node does not process data or generate output. It simply controls the flow initiation from a specific point.
- The **Play button** is visible and clickable by the user to start the flow at this node.
- This node has no enabled switch, making it always active when placed in the workflow.
