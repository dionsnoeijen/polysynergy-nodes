# Loop

✅ **Fixed:** This node has been completely rewritten to work properly with async execution and flow control.

A numeric loop node that executes a workflow section for a specified number of iterations.

## **Category:** Flow Control

## **Description**
The **Loop** node executes a section of a workflow a specified number of times. Unlike the List Loop which iterates over items in a list, this loop runs for a fixed number of repetitions.

It properly integrates with the PolySynergy flow system, supporting node resurrection, break/continue functionality, and loop end coordination.

### **Key Features:**
- **Async Execution:** Non-blocking loop operations for better performance
- **Break/Continue Support:** Can exit early or skip iterations
- **Node Resurrection:** Properly resets nodes for each iteration
- **Loop End Integration:** Works seamlessly with Loop End nodes
- **Counter Output:** Provides current iteration counter (1-based)
- **Error Handling:** Validates repeat count and handles edge cases

---

## **Variables**

### **Input Variables**

| Name      | Type | Description |
|-----------|------|-------------|
| `repeats` | int  | Number of times to repeat the loop (default: 1) |

### **Output Variables**

| Name      | Type | Description |
|-----------|------|-------------|
| `counter` | int  | Current iteration number (1-based) |

---

## **Flow Control**

| Path        | Condition | Description |
|-------------|-----------|-------------|
| `true_path` | Always    | Contains the current counter value for each iteration |

---

## **How It Works**

1. **Initialization**: Sets up loop parameters and finds nodes in the loop
2. **Iteration Loop**: Executes the specified number of times
3. **Node Management**: Resurrects nodes in the loop for each iteration
4. **Counter Updates**: Tracks current iteration (1-based counting)
5. **Break/Continue**: Supports early exit or iteration skipping
6. **Loop End**: Coordinates with Loop End node when present

### **Loop Execution Flow**
```
Start Loop → Set Counter → Resurrect Nodes → Execute Loop Body → Check Flags → Next Iteration → Loop End
     ↓             ↓            ↓                  ↓              ↓              ↓           ↓
   repeats=3    counter=1    Reset nodes       Run workflow   Break/Continue?   counter=2   Final result
```

---

## **Example Usage**

### **Basic 3-Iteration Loop**
```yaml
Loop:
  repeats: 3

# Output on each iteration:
# Iteration 1: counter = 1, true_path = 1
# Iteration 2: counter = 2, true_path = 2  
# Iteration 3: counter = 3, true_path = 3
```

### **Loop with Processing**
```yaml
# Process data 5 times with counter
Loop:
  repeats: 5
  ↓
Data Processor:
  iteration: {counter}  # Gets 1, 2, 3, 4, 5
  ↓
Loop End
```

### **Loop with Break Condition**
```yaml
Loop:
  repeats: 10
  ↓
Check Condition:
  value: {some_input}
  ↓
Break Loop:     # Exits early if condition met
  condition: {value > threshold}
  ↓
Loop End
```

---

## **Loop Control Nodes**

### **Break Loop**
Exits the loop immediately when called:
```yaml
Loop → Process Data → Break Loop (if condition) → Loop End
```

### **Continue Loop**  
Skips to the next iteration:
```yaml
Loop → Validate Data → Continue Loop (if invalid) → Process Data → Loop End
```

### **Loop End**
Collects results and manages loop completion:
```yaml
Loop → Multiple Nodes → Loop End (collects all results)
```

---

## **Integration Patterns**

### **Counter-Based Processing**
```yaml
# Use counter for indexed operations
Loop:
  repeats: 100
  ↓
Array Access:
  index: {counter - 1}  # Convert to 0-based indexing
  ↓
Process Item
```

### **Batch Processing**
```yaml
# Process in batches
Loop:
  repeats: 10
  ↓
Batch Processor:
  batch_number: {counter}
  batch_size: 100
  ↓
Loop End
```

### **Retry Logic**
```yaml
# Retry with counter limit
Loop:
  repeats: 3
  ↓
Try Operation → Success? → Break Loop
      ↓             ↓
   Handle Error   Loop End
```

---

## **Best Practices**

### **Loop Design**
- **Reasonable Limits**: Keep repeat counts reasonable to avoid performance issues
- **Break Conditions**: Always provide break conditions for potentially infinite processes
- **Counter Usage**: Use counter output for indexed operations or progress tracking
- **Loop End**: Always use Loop End nodes to properly collect results

### **Performance Considerations**
- **Node Count**: Be mindful of the number of nodes in the loop body
- **Resource Usage**: Consider memory and processing requirements for high iteration counts
- **Async Benefits**: The async implementation prevents blocking other workflows

### **Error Handling**
- **Validation**: The loop validates that repeats > 0
- **Graceful Degradation**: Handle errors within the loop body appropriately
- **Resource Cleanup**: Loop End nodes help manage resource cleanup

---

## **Differences from List Loop**

| Aspect | Loop | List Loop |
|--------|------|-----------|
| **Iteration Source** | Fixed number (repeats) | List items |
| **Counter** | 1-based iteration number | 0-based list index |
| **Output** | Counter value | Current list item |
| **Use Case** | Fixed repetitions | Data processing |
| **Performance** | Predictable iteration count | Depends on list size |

### **When to Use Each**

#### **Use Loop When:**
- Need to repeat an operation a specific number of times
- Implementing retry logic with limits
- Batch processing with fixed batch counts
- Counter-based operations or indexing

#### **Use List Loop When:**
- Processing items from a list or array
- Data transformation workflows
- Dynamic iteration based on data size
- Need access to actual data items

---

## **Troubleshooting**

### **Common Issues**

#### **Loop Not Executing**
- **Symptom**: Loop body never runs
- **Cause**: `repeats` set to 0 or negative number
- **Resolution**: Ensure `repeats > 0`

#### **Infinite Loop Behavior**
- **Symptom**: Loop seems to run forever
- **Cause**: Very high repeat count or break conditions not working
- **Resolution**: Check repeat value and break logic

#### **Counter Not Updating**
- **Symptom**: Counter stays at same value
- **Cause**: Node resurrection issues or flow problems
- **Resolution**: Verify loop structure and node connections

#### **Break/Continue Not Working**
- **Symptom**: Break or continue commands ignored
- **Cause**: Timing of flag setting or missing nodes
- **Resolution**: Ensure break/continue nodes are properly connected in loop body

---

## **Technical Implementation**

### **Async Architecture**
- Uses `async def execute()` for non-blocking operations
- Properly awaits flow execution calls
- Supports concurrent workflow execution

### **Node Management**
- Automatically detects nodes within the loop
- Resurrects nodes before each iteration
- Manages node state across iterations

### **Flag System**
- `_flag` property tracks break/continue commands
- Flags checked after each iteration execution
- Automatic flag cleanup after processing

---

🔄 **Use this node for fixed-count repetition workflows with proper async support and loop control.**