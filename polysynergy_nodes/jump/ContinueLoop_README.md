# 🔁 Continue Loop Node

The `Continue Loop` node is part of the `flow` category and is meant to be used **inside a `List Loop`** structure.

---

## 🧠 Purpose

This node is used to **skip the remainder of the current loop iteration** and continue with the next item.

---

## 🔄 Usage

Place this node inside a `List Loop`. When it is triggered during an iteration, the loop will immediately **skip to the next item**, skipping any remaining logic for the current item.

---

## 🧪 Example

Use this together with a condition node:

- Looping over items
- If a certain value should be skipped
- Connect the condition to `Continue Loop` to skip processing

---

## 🧩 Compatibility

✅ Only effective inside loop structures that support `continue_loop()`, like `List Loop`.

---

## 📌 Notes

- This node **does not produce any output**.
- It only influences the flow within the current iteration of a loop.