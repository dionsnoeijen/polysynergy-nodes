# 🔐 Deterministic UUID Node

The `Deterministic UUID` node generates a UUID v5 from input text, producing the same UUID for identical inputs. Perfect for creating consistent, reproducible identifiers.

---

## 📂 Category

**uuid**

---

## ⚙️ Inputs

| Name          | Type   | Required | Description                              |
|---------------|--------|----------|------------------------------------------|
| input_string  | str    | ✅        | Text to generate UUID from               |
| namespace     | str    | ❌        | UUID namespace (default: DNS)            |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | Deterministic UUID v5                       |
| false_path  | dict      | Error if generation fails                   |

---

## 🔑 Namespaces

| Namespace | Use Case                                    |
|-----------|---------------------------------------------|
| **DNS**   | Domain names (default)                      |
| **URL**   | URLs and URIs                               |
| **OID**   | ISO OID identifiers                         |
| **X500**  | X.500 Distinguished Names                   |

---

## ✅ Examples

### Generate from Email (DNS):
```json
{
  "input_string": "user@example.com",
  "namespace": "DNS"
}
```
**Output:** `"8d7e3b2a-5c4f-5a1b-9e8d-7c6b5a4e3d2c"` (always same for this input)

### Generate from URL:
```json
{
  "input_string": "https://example.com/resource/123",
  "namespace": "URL"
}
```
**Output:** Consistent UUID for this URL

### Generate Resource ID:
```json
{
  "input_string": "project:alpha:resource:42"
}
```
**Output:** Reproducible project resource identifier

---

## 🔄 Deterministic Behavior

**Same Input → Same UUID:**
```
Input: "user@example.com" (namespace: DNS)
Output 1: "8d7e3b2a-5c4f-5a1b-9e8d-7c6b5a4e3d2c"
Output 2: "8d7e3b2a-5c4f-5a1b-9e8d-7c6b5a4e3d2c"  ← Always identical
```

**Different Input → Different UUID:**
```
"user@example.com" → "8d7e3b2a-..."
"admin@example.com" → "f3a2b1c4-..."  ← Different UUID
```

---

## 💡 Use Cases

- **Idempotent Operations**: Ensure same ID for duplicate requests
- **Content-based IDs**: Generate IDs from content hashes
- **Reproducible Tests**: Consistent UUIDs in test environments
- **Deterministic Migrations**: Migrate data with consistent IDs

---

## 🎯 Comparison: UUID v4 vs UUID v5

| Feature | UUID v4 (Random) | UUID v5 (Deterministic) |
|---------|------------------|-------------------------|
| **Reproducible** | ❌ Random each time | ✅ Same for same input |
| **Collision Risk** | Very low | Virtually none (namespaced) |
| **Use Case** | Unique IDs | Content-based IDs |

---

## ⚠️ Notes

- **Deterministic**: Always produces same UUID for same input+namespace
- **UUID v5**: Uses SHA-1 hashing (standardized)
- **Namespace Matters**: Different namespaces produce different UUIDs
- **Case Sensitive**: "User" and "user" produce different UUIDs
- **Not Cryptographic**: Don't use for security purposes
