# Property Router

Routes objects based on property values using dot notation paths to different output connections.

## Description

The Property Router node extracts a property value from an input object using a dot notation path and routes the flow based on that property's value. This enables object-based routing where decisions are made based on nested object properties.

## Inputs

- **Object**: The object to extract property value from (required)
- **Property Path**: Dot notation path to the property (required, e.g., 'status', 'user.role', 'config.settings.theme')

## Outputs

Dynamic output connections based on property values:

- **Property value outputs**: Each possible property value creates a corresponding output
- **default**: Fallback route for missing properties or unmatched values

## Paths

- **No Match**: Triggered when property doesn't exist or no route matches and no default exists

## Property Path Format

- **Simple property**: `status` (accesses `obj.status`)
- **Nested property**: `user.role` (accesses `obj.user.role`)
- **Deep nesting**: `config.settings.theme` (accesses `obj.config.settings.theme`)

## Behavior

1. Extracts property value from input object using the specified path
2. If property doesn't exist, uses "default" route or triggers false path
3. Converts property value to string for route matching
4. Routes to matching property value output
5. If no route matches the property value, uses "default" route or triggers false path
6. Kills all non-matching output connections
7. Passes the original input object through the selected route

## Example Use Cases

- **User role-based routing**: Route users based on their role property
  ```json
  // Input: {"user": {"role": "admin", "name": "John"}}
  // Property Path: "user.role"
  // Routes to "admin" output
  ```

- **Order status processing**: Route orders based on status
  ```json
  // Input: {"order": {"status": "pending", "items": [...]}}
  // Property Path: "order.status"  
  // Routes to "pending" output
  ```

- **Configuration-based routing**: Route based on app settings
  ```json
  // Input: {"config": {"theme": "dark", "language": "en"}}
  // Property Path: "config.theme"
  // Routes to "dark" output
  ```

- **API response routing**: Route API responses based on result codes
  ```json
  // Input: {"response": {"code": 200, "data": {...}}}
  // Property Path: "response.code"
  // Routes to "200" output
  ```

- **Nested object classification**: Route based on deeply nested properties
  ```json
  // Input: {"metadata": {"user": {"preferences": {"notifications": "enabled"}}}}
  // Property Path: "metadata.user.preferences.notifications"
  // Routes to "enabled" output
  ```

## Property Extraction

- Only works with dictionary/object inputs
- Non-dictionary inputs automatically use "default" route
- Missing intermediate properties result in "default" route or false path
- Property values are converted to strings for route matching
- Supports any JSON-serializable property values (strings, numbers, booleans)

## Route Matching

- Property values are converted to strings for comparison
- Numeric values: `42` becomes `"42"`
- Boolean values: `true` becomes `"True"`, `false` becomes `"False"`
- Null values: `null` becomes `"None"`
- Exact string matching (case-sensitive)