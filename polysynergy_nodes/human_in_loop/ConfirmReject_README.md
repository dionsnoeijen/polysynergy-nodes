# ✋ Confirm/Reject Node

The `Confirm/Reject` node pauses workflow execution to await human approval or rejection, enabling human-in-the-loop decision making.

---

## 📂 Category

**human_in_loop**

---

## ⚙️ Inputs

| Name     | Type   | Required | Description                              |
|----------|--------|----------|------------------------------------------|
| message  | str    | ❌        | Message to display to human reviewer     |
| data     | any    | ❌        | Context data to present for review       |

---

## 🔌 Outputs

| Name         | Type   | Description                              |
|--------------|--------|------------------------------------------|
| confirmed    | bool   | True if approved, false if rejected      |
| response     | str    | Human's response message (if provided)   |

---

## 🔀 Flow Control

| Path        | Description                                 |
|-------------|---------------------------------------------|
| true_path   | Human confirmed/approved the action         |
| false_path  | Human rejected the action                   |

---

## ✅ Example Usage

### Approval Required:
```json
{
  "message": "Approve payment of $5,000 to vendor?",
  "data": {
    "vendor": "Acme Corp",
    "amount": 5000,
    "invoice": "INV-001"
  }
}
```

**Human Response:**
- ✅ Confirm → `true_path` triggered
- ❌ Reject → `false_path` triggered

### Data Review:
```json
{
  "message": "Review generated report before sending",
  "data": {
    "report_url": "https://example.com/report.pdf",
    "recipients": ["manager@company.com"]
  }
}
```

---

## 🔄 Workflow Patterns

### Approval Gate:
```
Process Data → Confirm/Reject → [Approved] → Continue
                             → [Rejected] → Cancel/Retry
```

### Quality Check:
```
Generate Content → Confirm/Reject → [OK] → Publish
                                  → [Not OK] → Revise
```

### Risk Mitigation:
```
High-Value Action → Confirm/Reject → [Approved] → Execute
                                   → [Rejected] → Log & Skip
```

### Multi-stage Approval:
```
Confirm/Reject (Manager) → Confirm/Reject (Director) → Final Action
```

---

## 💡 Use Cases

- **Financial Approvals**: Require human sign-off for payments
- **Content Review**: Review AI-generated content before publishing
- **Risk Management**: Human approval for high-risk operations
- **Quality Assurance**: Manual verification of automated processes
- **Compliance**: Required human oversight for regulated operations

---

## 🎯 Integration Points

### With Conditional Nodes:
```
Confirm/Reject → Conditional (if confirmed) → Path A
                                           → Path B
```

### With Notifications:
```
Confirm/Reject → [Rejected] → Send Notification → Log Event
```

### With Retry Logic:
```
Confirm/Reject → [Rejected] → Jump → Retry Process
```

---

## 🔔 User Interface

The node typically integrates with:
- **Web UI**: Button interface for confirm/reject
- **Email**: Email notifications with action links
- **Slack/Teams**: Interactive message buttons
- **Mobile App**: Push notifications with actions

---

## ⚠️ Notes

- **Blocking Operation**: Workflow pauses until human responds
- **Timeout Handling**: Should implement timeout logic in production
- **Response Tracking**: Logs who confirmed/rejected and when
- **Data Passing**: Context data helps human make informed decision
- **Security**: Should verify human identity before accepting action
