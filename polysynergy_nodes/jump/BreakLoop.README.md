# ⛔ Break Loop Node

The `Break Loop` node is part of the `flow` category and is intended to be used **inside a `List Loop`** structure.

---

## 🧠 Purpose

This node is used to **immediately stop** the loop execution when a certain condition is met.

---

## 🔄 Usage

Place this node inside a `List Loop`. When it is triggered, the loop will **terminate immediately**, skipping the rest of the items.

---

## 🧪 Example

Use this in combination with a condition node:

- Inside a loop over items
- If a certain value or condition is reached
- Connect it to `Break Loop` to stop further iteration

---

## 🧩 Compatibility

✅ Works only when inside a loop that supports `break_loop()`, such as `List Loop`.

---

## 📌 Notes

- This node **does not produce any output**.
- Only affects control flow inside a loop.