# 📦 KeyValue - Set Collection Node

The `KeyValue - Set Collection` node stores a key-value pair within a named collection for organized data storage. Collections provide namespace isolation for related data.

---

## 📂 Category

**persistent**

---

## ⚙️ Inputs

| Name        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| collection  | str    | ✅        | Collection name (e.g. 'user_settings')   |
| key         | str    | ✅        | The key within the collection            |
| value       | str    | ✅        | The value to store                       |

---

## 🔌 Outputs

| Name        | Type      | Description                                 |
|-------------|-----------|---------------------------------------------|
| true_path   | str       | The stored value                            |
| false_path  | dict      | Error information if storage fails          |

---

## ✅ Examples

### Store in User Settings Collection:
```json
{
  "collection": "user_settings",
  "key": "notification_enabled",
  "value": "true"
}
```
**Output:** `"true"`

### Store API Credentials:
```json
{
  "collection": "api_credentials",
  "key": "github_token",
  "value": "ghp_xxxxxxxxxxxx"
}
```
**Output:** `"ghp_xxxxxxxxxxxx"`

---

## 📚 Collections vs Simple Key-Value

| Feature | Simple Key-Value | Collection-based |
|---------|------------------|------------------|
| **Organization** | Flat namespace | Grouped by collection |
| **Use Case** | Global settings | Related data sets |
| **Isolation** | None | Per-collection |
| **Example** | `theme: "dark"` | `user_prefs.theme: "dark"` |

---

## 🔒 Security Features

- **Tenant Isolation**: Data scoped to current tenant and project
- **Collection Namespace**: Prevents key collisions between collections
- **Placeholder Support**: All fields support dynamic values

---

## 💡 Use Cases

- **Organized Storage**: Group related settings (e.g. 'email_config', 'api_keys')
- **Multi-tenant Data**: Separate data by user, session, or context
- **Feature Modules**: Store module-specific configuration
- **API Integration**: Store credentials per service

---

## ⚠️ Notes

- Collection names should be descriptive (e.g. 'google_drive_files', not 'gdf')
- All parameters support placeholder replacement
- Overwrites existing values with same collection + key combination
- Collections are created automatically on first use
