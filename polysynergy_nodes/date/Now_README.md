# Now

Returns the current date and time in a specified format.  
Supports both **formatted string output** and **UNIX timestamp**.

## **Category:** Date

## **Description**
The **Now** node provides the current UTC date and time.

It supports flexible formatting using `strftime` syntax or ISO 8601 (`"iso8601"` as shortcut).  
The output includes:
- a **formatted string**, and  
- a **UNIX timestamp** (seconds since epoch, UTC)

This node is useful for time-based comparisons, scheduling, or logging.

## **Variables**

| Name              | Type   | Input | Output | Description |
|-------------------|--------|-------|--------|-------------|
| `format`          | str    | ✅     | ❌      | Output format using Python `strftime` syntax, or `"iso8601"` for standard ISO format. |
| `timestamp_output`| int    | ❌     | ✅      | Current time as UNIX timestamp (UTC). |

## **Flow Control**

| Name         | Description |
|--------------|-------------|
| `true_path`  | The current time, formatted as requested. |
| `false_path` | Error details, if something went wrong. |

## **How It Works**
1. The node gets the current **UTC** datetime.
2. If `format = "iso8601"`, the output is like `"2025-04-07T14:30:00Z"`.
3. Otherwise, the format is applied via Python's `strftime`, e.g. `%Y-%m-%d %H:%M:%S`.
4. The result is sent to `true_path`, and the UNIX timestamp is set in `timestamp_output`.
5. If an error occurs, it is passed to `false_path`.

---

## **Example Usage**

### **Example 1: ISO Format**
#### **Input**
```text
format = "iso8601"
```

#### **Output**
- `true_path` = `"2025-04-07T14:30:00Z"`
- `timestamp_output` = `1744036200`

---

### **Example 2: Custom Format**
#### **Input**
```text
format = "%Y/%m/%d %H:%M"
```

#### **Output**
- `true_path` = `"2025/04/07 14:30"`
- `timestamp_output` = `1744036200`

---

## **Error Handling**
If an invalid format string is given:
- `false_path` will contain a dictionary with an `error` key describing the problem.
- `timestamp_output` will be set to `None`.

---

## **Use Cases**
✔ Logging current time for executions  
✔ Filtering records based on recent changes  
✔ Comparing timestamps  
✔ Scheduling logic or daily summaries

---

⏰ **With the Now Node, you can always work with the current time—formatted exactly how you need it.**
