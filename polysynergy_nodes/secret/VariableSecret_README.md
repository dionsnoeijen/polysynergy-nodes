
# 🔒 Variable Secret Node

The `Variable Secret` node is part of the **hidden** category and is used to pass a predefined secret key to other parts of the flow. It outputs the `true_path` value, which contains the secret key ID. This node does not actively execute any logic, but rather serves to make secrets available within the flow.

---

## ✅ Functionality

This node is used to pass a secret key (predefined) through the flow. The `true_path` output provides the full secret key ID, which can be used in other nodes for secure operations. The secret key is handled as a hidden value and is not visible in the user interface, ensuring the security of sensitive information.

---

## 🔌 Inputs

This node does not take any inputs.

---

## 🔀 Outputs

| Name        | Type     | Description                                  |
|-------------|----------|----------------------------------------------|
| true_path   | bool, str | The secret key ID that is passed through the flow. |

---

## 💡 Example

### Input:
```json
{}
```

### Output via `true_path`:
```json
{
  "true_path": "my-secret-key-id"
}
```

---

## ⚠️ Notes

- The `Variable Secret` node is part of the **hidden** category, meaning it is not visible in the UI for user configuration.
- It outputs the secret key ID (`true_path`), which can be used in other nodes within the flow.
- This node does not perform any action but is simply used to securely pass the secret key.
- The secret key is predefined and should not be altered by the user.

---

## 🔧 Dependencies

- **PathSettings**: Defines the `true_path` output containing the secret key.
