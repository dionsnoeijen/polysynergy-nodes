
# 🎲 Random Path Node

The `Random Path` node is part of the **random** category and is used to randomly select one of the outgoing paths from a node and execute it. The node marks the unchosen paths as "killer" to effectively disable them, and the chosen path is executed, passing the relevant data through the flow.

---

## ✅ Functionality

This node randomly selects one of the outgoing connections (`out_connections`) and sets it as the active path. All other connections are marked as "killer" to indicate that they should not be followed. The selected path's `true_path` value is then used to continue the workflow.

---

## 🔌 Inputs

| Name            | Type     | Required | Description                                        |
|-----------------|----------|----------|----------------------------------------------------|
| out_connections | list     | Yes      | A list of outgoing connections from this node. These paths will be randomly selected. |
| in_connections  | list     | No       | A list of incoming connections to the node (optional). Used to set the `true_path` from a previous node. |

---

## 🔀 Outputs

| Name        | Type             | Description                                    |
|-------------|------------------|------------------------------------------------|
| true_path   | bool, int, float, str, list, dict | The path that was selected, or the path value that was passed from an incoming connection. |
| false_path  | dict             | Error information if failure occurs           |

---

## 💡 Example

### Input:
```json
{
  "out_connections": ["path1", "path2", "path3"]
}
```

### Output via `true_path`:
```json
{
  "true_path": "path1"
}
```

---

## ⚠️ Notes

- If there are no outgoing connections (`out_connections` is empty), an error will be output via `false_path`.
- If there are incoming connections, the `true_path` from the source node will be used. If no `true_path` is found, it defaults to `True`.
- All unchosen outgoing paths are marked as "killer" using the `make_killer` method on the connections.
- This node does not generate any data itself but simply controls the flow of execution based on a random selection.
- **Async Execution**: This node uses asynchronous execution for consistency with the framework.
- **Error Handling**: All errors are properly formatted using `NodeError.format()` for consistent error reporting.

---

## 🔧 Dependencies

- `random` (for generating random selections)
- `Connection` (for managing node connections)
