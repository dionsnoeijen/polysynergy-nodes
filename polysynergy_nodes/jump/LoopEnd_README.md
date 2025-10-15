# 🏁 Loop End Node

The `Loop End` node marks the end of a loop and collects results from all loop iterations. It aggregates outputs and continues the flow after the loop completes.

---

## 📂 Category

**flow**

---

## ⚙️ Inputs

| Name   | Type   | Required | Description                              |
|--------|--------|----------|------------------------------------------|
| to     | str    | ❌        | Optional jump target after loop completion |

---

## 🔌 Outputs

| Name        | Type                    | Description                              |
|-------------|-------------------------|------------------------------------------|
| true_path   | bool \| list \| str \| int \| float \| dict | Collected results from loop |

---

## 🔀 Result Collection

The Loop End node intelligently collects results:

### Single Source:
If one node connects to Loop End:
```
Loop → Process → Loop End
```
**Output:** Single value from Process node

### Multiple Sources:
If multiple nodes connect to Loop End:
```
Loop → Process A → Loop End
     → Process B ↗
```
**Output:** Array of values `[result_a, result_b]`

### No Sources:
If no nodes connect:
**Output:** `True` (boolean)

---

## ✅ Example Usage

### Basic Loop Collection:
```
Loop(repeats=5)
  ↓
Calculate(counter * 2)
  ↓
Loop End

Output: [2, 4, 6, 8, 10]
```

### List Processing:
```
List Loop(items=[1,2,3,4,5])
  ↓
Transform(item → item ** 2)
  ↓
Loop End

Output: [1, 4, 9, 16, 25]
```

### Multiple Results Per Iteration:
```
Loop(repeats=3)
  ↓  ↘
  A   B
  ↓   ↓
Loop End

Output: [[a1, b1], [a2, b2], [a3, b3]]
```

---

## 🎯 Loop Patterns

### Accumulation Pattern:
```
Loop → Process → Loop End → Continue with results
```

### Filter Pattern:
```
List Loop → Filter → Loop End → Get filtered items
```

### Transform Pattern:
```
List Loop → Transform → Loop End → Get transformed items
```

### Validation Pattern:
```
Loop → Validate → Loop End → Get validation results
```

---

## 🔄 Integration with Loop Nodes

Works with:
- **Loop**: Fixed iteration loops
- **List Loop**: List-based iteration
- **Break Loop**: Early loop exit support
- **Continue Loop**: Skip iteration support

---

## 💡 Use Cases

- **Data Collection**: Gather results from all loop iterations
- **Batch Processing**: Collect processed batch results
- **Aggregation**: Accumulate values across iterations
- **Transformation**: Collect transformed data

---

## ⚠️ Notes

- **Result Aggregation**: Automatically collects from driving connections
- **Type Flexibility**: Output type depends on collected results
- **Loop Awareness**: Coordinates with loop control nodes
- **Optional `to` Parameter**: Can jump to another node after completion
- **Empty Default**: Returns `True` if no results to collect
