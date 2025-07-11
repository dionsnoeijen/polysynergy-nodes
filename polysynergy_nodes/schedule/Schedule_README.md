
# 🗓️ Schedule Node

The `Schedule` node is part of the **schedule** category and is used to represent a scheduled task in the system. It contains properties related to the task's schedule, such as the cron expression, start and end times, and its active state. This node does not perform any action by itself but provides the necessary data for scheduling tasks in a flow.

---

## ✅ Functionality

This node is used to define a scheduled task. It includes a cron expression for defining the schedule, along with start and end times for the task. The node also tracks whether the schedule is currently active and outputs a `true_path` that can be used to trigger the scheduled task.

---

## 🔌 Inputs

This node does not take any inputs.

---

## 🔀 Outputs

| Name            | Type        | Description                                     |
|-----------------|-------------|-------------------------------------------------|
| schedule_name   | string      | The name of the schedule.                       |
| cron_expression | string      | The cron expression that defines the schedule.  |
| start_time      | datetime    | The start time for the scheduled task.          |
| end_time        | datetime    | The end time for the scheduled task.            |
| is_active       | bool        | A boolean indicating if the schedule is active. |
| true_path       | bool        | A value that can be used to trigger the task flow. |

---

## 💡 Example

### Input (Automatically configured based on the schedule configuration):
```json
{
  "schedule_name": "Daily Backup",
  "cron_expression": "0 0 * * *",
  "start_time": "2025-01-01T00:00:00",
  "end_time": "2025-01-01T23:59:59",
  "is_active": true
}
```

### Output via `true_path`:
```json
{
  "true_path": true
}
```

---

## ⚠️ Notes

- This node defines the properties for a scheduled task, including the cron expression, start time, and end time.
- The node outputs a `true_path` value to trigger the flow when the scheduled time arrives.
- The schedule is represented by the `cron_expression` and is configured according to the specific time intervals defined by the cron syntax.
- This node does not actively perform the task, but rather defines when and how the task is triggered.

---

## 🔧 Dependencies

- **PathSettings**: Defines the `true_path` output that triggers the scheduled task flow.
- **datetime**: Used for managing the start and end times of the schedule.
- **cron expression**: Used for defining the scheduling frequency and timing.
