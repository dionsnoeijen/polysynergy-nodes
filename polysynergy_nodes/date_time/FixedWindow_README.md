# Fixed Time Window Node

The **Fixed Time Window** node generates a time window **that looks back in time** based on the current time or a provided reference time.  
It creates consistent, fixed intervals which are useful for time-based processing like logs, events, or polling APIs.

## **Category:** Date

## **Description**
This node calculates a **fixed time window** ending at the most recent aligned interval (e.g. 15:40, 16:00, etc.) and going back by a specified duration.  
Unlike forward-looking implementations, this version ensures **you don't miss events** that occurred just before "now".

## **Variables**

| Name           | Type   | Input | Output | Description |
|----------------|--------|-------|--------|-------------|
| `reference_time` | str  | ✅     | ❌      | Optional ISO 8601 reference time (defaults to current UTC time). |
| `unit`         | str    | ✅     | ❌      | Time unit for interval: `seconds`, `minutes`, `hours`. |
| `interval`     | int    | ✅     | ❌      | Interval length in the selected unit. |
| `format`       | str    | ✅     | ❌      | Format for output timestamps. Defaults to `"iso8601"`. |
| `window_start` | str    | ❌     | ✅      | Start of the time window. |
| `window_end`   | str    | ❌     | ✅      | End of the time window. |

## **Flow Control**
- `false_path` (bool or dict) – Triggered if the input is invalid or unsupported.

## **How It Works**
1. Takes current UTC time or the given `reference_time`.
2. Rounds down to the latest aligned time for the interval (e.g. to 15:40 if now is 15:43).
3. Computes:
   - `window_end = floored`
   - `window_start = window_end - interval`
4. Outputs formatted timestamps.

### ✅ This node always **looks backward in time**, ensuring no future data is included.

## **Example**

If current time is `2025-04-21T15:43:00Z` and:
- `unit = "minutes"`
- `interval = 20`

The node produces:
- `window_start = 2025-04-21T15:20:00Z`
- `window_end = 2025-04-21T15:40:00Z`

## **Use Cases**
✔ Time-windowed polling  
✔ Batching data updates  
✔ Segmenting events by time  
✔ Avoiding gaps in time-based pipelines

---

🕒 Consistent time windows make it easier to reason about what data you're including — and what je níét per ongeluk mist.