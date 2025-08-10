# List Contains Router

Routes values based on which predefined list contains the input value.

## Description

The List Contains Router node checks if an input value exists within any of several predefined lists and routes the flow to the corresponding list's output connection. This enables category-based routing where items are classified by list membership.

## Inputs

- **Value**: The value to check for existence in lists (required)
- **Lists**: Dictionary of named lists to check against (configured via input connections)

## Outputs

Dynamic output connections based on list names:

- **List outputs**: Each list name creates a corresponding output connection
- **default**: Fallback route for values not found in any list

## Paths

- **No Match**: Triggered when value is not found in any list and no default exists

## Behavior

1. Checks if the input value exists in each configured list
2. Routes to the first list that contains the value
3. If value is not found in any list, uses "default" route or triggers false path
4. Kills all non-matching output connections
5. Passes the original input value through the selected route

## List Matching

- Uses Python's `in` operator for membership testing
- For unhashable types (dicts, lists), falls back to string comparison
- Exact matching - case sensitive for strings
- Supports mixed data types within lists

## Example Use Cases

- **User role routing**: Route users based on role lists
  ```
  lists = {
    "admins": ["alice", "bob", "charlie"],
    "moderators": ["david", "eve"],
    "users": ["frank", "grace", "henry"]
  }
  ```

- **Category classification**: Route products by category lists
  ```
  lists = {
    "electronics": ["laptop", "phone", "tablet"],
    "clothing": ["shirt", "pants", "shoes"],
    "books": ["novel", "textbook", "manual"]
  }
  ```

- **Permission-based routing**: Route actions based on permission lists
  ```
  lists = {
    "read_permissions": ["view_reports", "view_users"],
    "write_permissions": ["create_user", "edit_content"],
    "admin_permissions": ["delete_user", "system_config"]
  }
  ```

- **Tag-based filtering**: Route content based on tag membership
  ```
  lists = {
    "urgent_tags": ["critical", "emergency", "urgent"],
    "info_tags": ["info", "notice", "announcement"],
    "warning_tags": ["warning", "caution", "alert"]
  }
  ```

## Configuration Notes

- Lists are provided through input connections to the "Lists" parameter
- Each list should be a proper Python list/array
- Non-list values are treated as empty and won't match any input
- Empty lists won't match any input values
- The first matching list determines the routing (order matters)