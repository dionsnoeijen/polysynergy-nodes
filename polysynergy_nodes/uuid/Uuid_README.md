# 🎲 UUID v4 Node

The `UUID v4` node generates a random UUID v4, providing universally unique identifiers for entities, sessions, or any unique identification needs.

---

## 📂 Category

**uuid**

---

## ⚙️ Inputs

No inputs required - generates UUID on each execution

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | Random UUID v4                              |
| false_path  | dict      | Error if generation fails                   |

---

## ✅ Examples

### Generate Unique ID:
**No inputs needed**

**Output:** `"f47ac10b-58cc-4372-a567-0e02b2c3d479"` (random)

**Next execution:** `"c9bf9e57-1685-4c89-bafb-ff5af830be8a"` (different)

---

## 🎲 Randomness

- **Unique**: Each execution generates a new random UUID
- **Collision Probability**: ~0% (2^122 possible values)
- **Standard**: RFC 4122 compliant
- **Format**: 8-4-4-4-12 hexadecimal pattern

---

## 💡 Use Cases

- **Entity IDs**: Unique identifiers for database records
- **Session Tokens**: Session management identifiers
- **Request IDs**: Track API requests uniquely
- **File Names**: Generate unique temporary filenames
- **Transaction IDs**: Track unique transactions

---

## 🎯 Common Patterns

### Create User:
```
UUID v4 → Store as user_id → Create User Record
```

### Session Management:
```
Login → UUID v4 → Store Session → Return Token
```

### Request Tracking:
```
HTTP Request → UUID v4 → Attach to Logs → Track Request
```

### Unique Filenames:
```
UUID v4 → Append Extension → Save File
```

---

## 🔄 Comparison: UUID v4 vs Deterministic UUID

| Feature | UUID v4 (this node) | UUID v5 (Deterministic) |
|---------|---------------------|-------------------------|
| **Generation** | Random | Hash-based |
| **Reproducible** | ❌ Always different | ✅ Same for same input |
| **Use Case** | Unique IDs | Content-based IDs |
| **Performance** | Slightly faster | Slightly slower |

---

## ⚠️ Notes

- **Random**: Different UUID on every execution
- **Stateless**: No inputs required
- **Thread-safe**: Safe for concurrent use
- **Standard Format**: Lowercase hexadecimal with hyphens
- **For deterministic UUIDs**, use "Deterministic UUID" node instead
