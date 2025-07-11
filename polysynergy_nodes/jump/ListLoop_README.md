# 🔁 List Loop Node

The **List Loop** node is part of the `flow` category and enables iterative execution over a list of items. It is designed for advanced control flows and integrates tightly with nodes like `Loop End`, `Break Loop`, and `Continue Loop`.

---

## ✅ Functionality

This node loops through each item in the provided list and triggers connected nodes for every iteration.  
You can interrupt the loop with a `Break Loop` node or skip to the next item using a `Continue Loop` node.  
After the loop is done, control is passed to the connected `Loop End` node, if present.

---

## 🔌 Inputs

| Name         | Type  | Required | Description                              |
|--------------|-------|----------|------------------------------------------|
| `input_list` | list  | ✅        | The list of items to loop over.          |

---

## 🔀 Outputs

| Name         | Type                      | Description                             |
|--------------|---------------------------|------------------------------------------|
| `true_path`  | bool \| list \| str \| int \| float \| dict | The current item in the loop. |
| `index`      | int                       | The current index of the loop (0-based). |

---

## ⚙️ Internal

| Property     | Description                                |
|--------------|--------------------------------------------|
| `_started`   | Ensures the loop is only started once.     |
| `_flag`      | Used for controlling `break` and `continue`.|

---

## 📌 Usage with Other Nodes

- ✅ `Break Loop`: Immediately stops the loop and triggers the `Loop End`.
- ✅ `Continue Loop`: Skips the current iteration and continues with the next.
- ✅ `Loop End`: Waits until all loop iterations finish and passes on the result(s).

---

## 🧪 Example

Input:
```json
["apple", "banana", "cherry"]
```

Output:
- `true_path`: `"apple"`, `"banana"`, `"cherry"` (on each iteration)
- `index`: `0`, `1`, `2`

---

## 🚫 Errors

If no list is provided, a `ValueError` is raised:
```
List Loop: No valid list provided
```

---

## 🧠 Tips

- This node does not return a complete result list — use `Loop End` if you want to aggregate results.