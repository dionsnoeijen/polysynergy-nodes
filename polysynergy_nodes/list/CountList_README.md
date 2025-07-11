# 🧮 Count List Node

⚠️ **Warning:** This Node uses falsey values (`0`) as a valid `true_path` output. To preserve consistency with other nodes, this implementation diverts `true_path` when the list has length > 0 and `false_path` when the list is empty.

---

## Description

The **Count List** node counts the number of items in a list and routes based on whether the list is empty.

---

## Inputs

| Name       | Type | Required | Description            |
|------------|------|----------|------------------------|
| List       | list | ✅        | The list to count      |

---

## Outputs

| Path         | Type | Description                                         |
|--------------|------|-----------------------------------------------------|
| `true_path`  | int  | The length of the list, triggered when length > 0   |
| `false_path` | bool | Always `True`, triggered when the list is empty     |

---

## Example

If `input_list = [1, 2, 3]`, then:
- `true_path` = `3`
- `false_path` is not triggered

If `input_list = []`, then:
- `false_path` = `True`
- `true_path` is not triggered

---

## Use Case

Use this node to count how many items are in a list, and branch logic depending on whether the list is empty.

