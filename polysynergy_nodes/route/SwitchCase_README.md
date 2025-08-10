# Switch Case

Routes workflow execution to different paths based on input value matching.  
Essential for multi-branch conditional logic and dynamic workflow routing.

## **Category:** Conditional

## **Description**
The **Switch Case** node provides dynamic multi-path routing by matching an input value against case keys in a dock dictionary. Only the matched path continues execution while all other paths are terminated.

It supports:
- **Dictionary-based cases** - Define case keys in the dock dictionary
- **Multiple output connections** - Each case key creates an output connection
- **String matching** - Input values converted to strings for comparison
- **Default fallback** - Special "default" key for unmatched values
- **Data passthrough** - Forwards input data to the selected case

## **Variables**

| Name    | Type   | Input | Output | Description |
|---------|--------|-------|--------|-------------|
| `value` | object | ✅     | ❌      | The value to match against case keys |
| `cases` | dict   | ❌     | ✅      | Dictionary defining available cases (dock dictionary) |

## **Flow Control**

| Name           | Description |
|----------------|-------------|
| `false_path`   | Triggered when no cases match and no default exists |
| **Case Outputs** | Each case key in the dictionary creates an output connection |

## **How It Works**
1. Receives input value via `value` parameter
2. Converts value to string for comparison using `str(value)`
3. Searches case dictionary for matching keys:
   - **Exact match** - Case key exactly matches the string value
   - **Default case** - Case key "default" (fallback)
   - **No match** - Triggers `false_path` if no default exists
4. **Activates chosen path** - Allows execution to continue through matched case
5. **Kills other paths** - Terminates execution on non-selected branches
6. **Stores data** - Places input value in the matched case dictionary entry

---

## **Case Dictionary Setup**

### **Case Keys**
Define cases by adding keys to the dock dictionary:
- **String cases**: "success", "error", "pending"
- **Numeric cases**: "200", "404", "500" (numbers become strings)
- **Boolean cases**: "True", "False" (booleans become strings)
- **Default case**: "default" (special fallback key)

### **Example Workflow**
```
[API Response] → [Switch Case] → [Case: "success"] → [Success Handler]
                  Cases: {        [Case: "error"] → [Error Handler]
                    "success": …,  [Case: "default"] → [Default Handler]
                    "error": …,
                    "default": …
                  }
```

---

## **Example Usage**

### **API Response Routing**
```
Input value: "success"
Connection labels: ["success", "error", "default"]
Result: Routes to "success" path, kills "error" and "default" paths
```

### **Status Code Handling**  
```
Input value: 404
Connection labels: ["200", "404", "500", "default"]
Result: Routes to "404" path (numeric matching)
```

### **Boolean Routing**
```
Input value: true
Connection labels: ["true", "false"] 
Result: Routes to "true" path
```

### **Default Fallback**
```
Input value: "unknown_status"
Connection labels: ["success", "error", "default"]
Result: Routes to "default" path (no exact match found)
```

---

## **Matching Rules**

1. **Case-insensitive** - "Success" matches "success" 
2. **Whitespace trimmed** - "  error  " matches "error"
3. **String conversion** - Number 42 matches label "42"
4. **Priority order**:
   - Exact label match (highest priority)
   - Default connection (if no exact match)
   - First connection (ultimate fallback)

---

## **Use Cases**
✔ **API response handling** - Route based on status codes  
✔ **Workflow state management** - Different paths for different states  
✔ **Error handling** - Separate paths for success/error/timeout  
✔ **User role routing** - Different flows for admin/user/guest  
✔ **Data type switching** - Handle different input formats  
✔ **Multi-environment deployment** - dev/staging/production paths

---

## **Advanced Features**

### **Data Passthrough**
- Automatically forwards data from connected input nodes
- Maintains data integrity across path transitions
- No data transformation, pure routing functionality

### **Dynamic Path Selection**
- Runtime path selection based on live data
- No pre-configuration of case values needed
- Flexible connection management

---

🔀 **Use this node when you need to route workflow execution to different paths based on dynamic input values.**